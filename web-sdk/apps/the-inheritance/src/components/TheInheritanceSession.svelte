<script lang="ts">
	import { onMount } from 'svelte';

	import * as envStaticPublic from '$env/static/public';
	import { page } from '$app/state';
	import { API_AMOUNT_MULTIPLIER, MOST_USED_BET_INDEXES } from 'constants-shared/bet';
	import { requestAuthenticate, requestReplay } from 'rgs-requests';
	import { stateBet, stateConfig, stateModal, stateUi, stateUrlDerived } from 'state-shared';

	import { stateMathSession } from '../game/stateMathSession.svelte';

	const DEFAULT_EXPECTED_RTP = 97;
	const LOCAL_RGS_URL = 'http://127.0.0.1:3008';
	const SUPPORTED_RTP = [92, 93, 94, 95, 96, 97] as const;

	const replayRound = () => page.url.searchParams.get('replayRound') || '';
	const isReplayMode = () => stateUrlDerived.replay() || replayRound().length > 0;

	const requestSessionConfig = async () => {
		const response = await fetch(`${LOCAL_RGS_URL}/game/session-config`);
		if (!response.ok) throw new Error(`Local session-config failed: ${response.status}`);
		return response.json();
	};

	const requestReplayRound = async (roundID: string) => {
		const baseUrl = stateUrlDerived.rgsUrl() || LOCAL_RGS_URL;
		const response = await fetch(`${baseUrl}/bet/replay?roundID=${encodeURIComponent(roundID)}`);
		if (!response.ok) throw new Error(`Replay round ${roundID} failed: ${response.status}`);
		return response.json();
	};

	const parseExpectedRtp = () => {
		const rawValue = envStaticPublic.PUBLIC_THE_INHERITANCE_RTP;
		if (!rawValue?.trim()) return DEFAULT_EXPECTED_RTP;

		const normalized = rawValue.trim().replace('%', '');
		const numericValue = Number(normalized);
		if (!Number.isFinite(numericValue)) {
			throw new Error(`Invalid PUBLIC_THE_INHERITANCE_RTP value: ${rawValue}`);
		}

		const percentage = Math.round(numericValue <= 1 ? numericValue * 100 : numericValue);
		if (!SUPPORTED_RTP.includes(percentage as (typeof SUPPORTED_RTP)[number])) {
			throw new Error('PUBLIC_THE_INHERITANCE_RTP must be 92, 93, 94, 95, 96, or 97.');
		}
		return percentage;
	};

	const verifyLocalMathSession = async () => {
		if (stateUrlDerived.rgsUrl()) {
			stateMathSession.status = 'ready';
			return;
		}

		const sessionConfig = await requestSessionConfig();
		const expectedRtp = parseExpectedRtp();
		stateMathSession.config = sessionConfig;
		stateMathSession.expectedRtp = expectedRtp;

		if (!sessionConfig || sessionConfig.rtp !== expectedRtp) {
			throw {
				error: 'RTP_PROFILE_MISMATCH',
				message: `Local Math SDK bridge selected ${sessionConfig?.rtp ?? 'unknown'}%, but this frontend build expects ${expectedRtp}%.`,
			};
		}
	};

	const applyBalance = (balance?: { amount: number; currency: string }) => {
		if (!balance) return;
		stateBet.currency = balance.currency;
		stateBet.balanceAmount = balance.amount / API_AMOUNT_MULTIPLIER;
	};

	const applyConfig = (config?: any) => {
		if (!config) return;
		stateConfig.jurisdiction = config.jurisdiction;
		stateConfig.betAmountOptions = (config.betLevels || []).map(
			(level: number) => level / API_AMOUNT_MULTIPLIER,
		);
		stateConfig.betMenuOptions = stateConfig.betAmountOptions.filter((_, index) =>
			MOST_USED_BET_INDEXES.includes(index),
		);
	};

	const authenticate = async () => {
		const authenticateData = await requestAuthenticate({
			rgsUrl: stateUrlDerived.rgsUrl(),
			sessionID: stateUrlDerived.sessionID(),
			language: stateUrlDerived.lang(),
		});

		if (authenticateData?.error) throw authenticateData;

		applyBalance(authenticateData?.balance);
		applyConfig(authenticateData?.config);

		if (authenticateData?.round?.state) {
			// @ts-ignore The RGS round shape is narrowed by the game-specific book event type later.
			stateBet.betToResume = authenticateData.round;
		}

		if (authenticateData?.round?.amount) {
			const betAmountValue = authenticateData.round.amount / API_AMOUNT_MULTIPLIER;
			stateBet.betAmount = betAmountValue;
			stateBet.wageredBetAmount = betAmountValue;
		}

		if (authenticateData?.round?.mode) stateBet.activeBetModeKey = authenticateData.round.mode;
	};

	const replayPayload = async () => {
		const replayRoundID = replayRound();
		if (replayRoundID) {
			stateMathSession.replayRoundID = replayRoundID;
			return requestReplayRound(replayRoundID);
		}

		return requestReplay({
			rgsUrl: stateUrlDerived.rgsUrl(),
			game: stateUrlDerived.game(),
			mode: stateUrlDerived.mode(),
			version: stateUrlDerived.version(),
			event: stateUrlDerived.event(),
		});
	};

	const handleReplay = async () => {
		const data = await replayPayload();
		if (data?.error) throw data;

		const mode = data?.mode || stateUrlDerived.mode();
		const betAmount =
			Number(data?.betAmount) ||
			(stateUrlDerived.amount() / API_AMOUNT_MULTIPLIER) ||
			(data?.amount / API_AMOUNT_MULTIPLIER) ||
			0;

		stateBet.betAmount = betAmount;
		stateBet.wageredBetAmount = betAmount;
		stateBet.activeBetModeKey = mode;
		applyBalance(data?.balance);

		if (data) {
			// @ts-ignore The RGS round shape is narrowed by the game-specific book event type later.
			stateBet.betToResume = {
				...data,
				event: '0',
				active: true,
				mode,
			};
		}
	};

	onMount(async () => {
		try {
			stateMathSession.status = 'pending';
			await verifyLocalMathSession();

			if (isReplayMode()) {
				stateUi.config.mode = 'replay';
				await handleReplay();
			} else {
				stateUi.config.mode = 'default';
				await authenticate();
			}

			stateMathSession.status = 'ready';
		} catch (error) {
			console.error(error);
			stateMathSession.status = 'blocked';
			stateMathSession.error = error;
			stateModal.modal = { name: 'error', error };
		}
	});
</script>
