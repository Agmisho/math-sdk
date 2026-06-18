import { API_AMOUNT_MULTIPLIER } from 'constants-shared/bet';
import { rgsFetcher } from 'rgs-fetcher';

export * from './types';

const mockReel = (names: string[]) => names.map((name) => ({ name }));

const createMockPlayResponse = (options: { currency: string; amount: number; mode: string }) => ({
	status: { statusCode: 'SUCCESS', statusMessage: 'Mock play response' },
	balance: {
		amount: 1000 * API_AMOUNT_MULTIPLIER,
		currency: options.currency,
	},
	round: {
		roundID: Date.now(),
		amount: options.amount * API_AMOUNT_MULTIPLIER,
		payout: 0,
		payoutMultiplier: 0,
		active: false,
		mode: options.mode,
		event: '0',
		state: [
			{
				index: 0,
				type: 'reveal',
				gameType: 'basegame',
				paddingPositions: [0, 0, 0, 0, 0],
				anticipation: [0, 0, 0, 0, 0],
				board: [
					mockReel(['H1', 'H3', 'L2', 'H4']),
					mockReel(['L2', 'H4', 'L3', 'H1']),
					mockReel(['H3', 'L1', 'M5', 'H4']),
					mockReel(['H4', 'L2', 'H2', 'H1']),
					mockReel(['L5', 'H1', 'L3', 'H4']),
				],
			},
		],
	},
});

export const requestAuthenticate = async (options: {
	sessionID: string;
	rgsUrl: string;
	language: string;
}) => {
	const data = await rgsFetcher.post({
		rgsUrl: options.rgsUrl,
		url: '/wallet/authenticate',
		variables: {
			sessionID: options.sessionID,
			language: options.language,
		},
	});

	return data;
};

export const requestEndRound = async (options: {
	sessionID: string;
	rgsUrl: string;
}) => {
	if (!options.rgsUrl) {
		return {
			status: { statusCode: 'SUCCESS', statusMessage: 'Mock end round response' },
			balance: { amount: 1000 * API_AMOUNT_MULTIPLIER, currency: 'USD' },
		};
	}

	const data = await rgsFetcher.post({
		rgsUrl: options.rgsUrl,
		url: '/wallet/end-round',
		variables: {
			sessionID: options.sessionID,
		},
	});

	return data;
};

export const requestEndEvent = async (options: {
	sessionID: string;
	eventIndex: number;
	rgsUrl: string;
}) => {
	const data = await rgsFetcher.post({
		rgsUrl: options.rgsUrl,
		url: '/bet/event',
		variables: {
			sessionID: options.sessionID,
			event: `${options.eventIndex}`,
		},
	});

	return data;
};

export const requestBet = async (options: {
	sessionID: string;
	currency: string;
	amount: number;
	mode: string;
	rgsUrl: string;
}) => {
	if (!options.rgsUrl) {
		return createMockPlayResponse(options);
	}

	const data = await rgsFetcher.post({
		rgsUrl: options.rgsUrl,
		url: '/wallet/play',
		variables: {
			mode: options.mode,
			currency: options.currency,
			sessionID: options.sessionID,
			amount: options.amount * API_AMOUNT_MULTIPLIER,
		},
	});

	return data;
};

export const requestReplay = async (options: {
	game: string;
	version: string;
	mode: string;
	event: string;
	rgsUrl: string;
}) => {
	const data = await rgsFetcher.get({
		rgsUrl: options.rgsUrl,
		// @ts-ignore TODO: update the schema.ts
		url: `/bet/replay/${options.game}/${options.version}/${options.mode}/${options.event}`,
	});

	return data;
};
