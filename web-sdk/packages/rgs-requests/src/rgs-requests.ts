import { API_AMOUNT_MULTIPLIER, BOOK_AMOUNT_MULTIPLIER } from 'constants-shared/bet';
import { rgsFetcher } from 'rgs-fetcher';

export * from './types';

const mockReel = (names: string[]) => names.map((name) => ({ name }));
let mockBalanceAmount = 1000 * API_AMOUNT_MULTIPLIER;
let mockSpinIndex = 0;

const mockBoards = [
	[
		mockReel(['L1', 'H1', 'H3', 'L2', 'H4', 'S', 'L3']),
		mockReel(['H2', 'L2', 'H4', 'L3', 'H1', 'M2', 'L6']),
		mockReel(['L3', 'H3', 'S', 'M5', 'H4', 'L2', 'H5']),
		mockReel(['L4', 'H4', 'L2', 'H2', 'S', 'H1', 'M10']),
		mockReel(['H5', 'L5', 'H1', 'L3', 'H4', 'M2', 'S']),
	],
	[
		mockReel(['H3', 'L2', 'H4', 'S', 'L3', 'H5', 'L4']),
		mockReel(['H4', 'L3', 'H1', 'M2', 'L6', 'H2', 'S']),
		mockReel(['S', 'M5', 'H4', 'L2', 'H5', 'W', 'L1']),
		mockReel(['L2', 'H2', 'S', 'H1', 'M10', 'L5', 'H3']),
		mockReel(['H1', 'L3', 'H4', 'M2', 'S', 'L6', 'H2']),
	],
	[
		mockReel(['L1', 'H1', 'H1', 'H1', 'L2', 'H4', 'S']),
		mockReel(['H2', 'L3', 'H1', 'H4', 'L3', 'H1', 'M2']),
		mockReel(['L3', 'M5', 'H1', 'S', 'M5', 'H4', 'L2']),
		mockReel(['L4', 'H2', 'H1', 'L2', 'H2', 'S', 'H1']),
		mockReel(['H5', 'L5', 'H1', 'H1', 'L3', 'H4', 'M2']),
	],
	[
		mockReel(['H4', 'H4', 'L2', 'H4', 'S', 'L3', 'H5']),
		mockReel(['L2', 'H4', 'H4', 'L3', 'H1', 'M2', 'L6']),
		mockReel(['L3', 'H3', 'H4', 'M5', 'H4', 'L2', 'H5']),
		mockReel(['L4', 'H4', 'H4', 'H2', 'S', 'H1', 'M10']),
		mockReel(['H5', 'L5', 'H4', 'L3', 'H4', 'M2', 'S']),
	],
];

const createMockPlayResponse = (options: { currency: string; amount: number; mode: string }) => {
	const spinIndex = mockSpinIndex;
	const board = mockBoards[spinIndex % mockBoards.length];
	const isWin = spinIndex % 3 === 2 || spinIndex % 5 === 4;
	const winMultipliers = [2.5, 4, 7.5, 12];
	const winMultiplier = isWin ? winMultipliers[Math.floor(spinIndex / 3) % winMultipliers.length] : 0;
	const betApiAmount = Math.round(options.amount * API_AMOUNT_MULTIPLIER);
	const payoutAmount = options.amount * winMultiplier;
	const payoutApiAmount = Math.round(payoutAmount * API_AMOUNT_MULTIPLIER);
	const payoutBookAmount = Math.round(payoutAmount * BOOK_AMOUNT_MULTIPLIER);
	mockSpinIndex += 1;
	mockBalanceAmount = Math.max(0, mockBalanceAmount - betApiAmount + payoutApiAmount);

	const state = [
		{
			index: 0,
			type: 'reveal',
			gameType: 'basegame',
			paddingPositions: [0, 0, 0, 0, 0],
			anticipation: [0, 0, 0, 0, 0],
			board,
		},
	];

	if (isWin) {
		state.push(
			{
				index: 1,
				type: 'winInfo',
				totalWin: payoutBookAmount,
				wins: [
					{
						symbol: spinIndex % 5 === 4 ? 'H4' : 'H1',
						kind: 5,
						win: payoutBookAmount,
						positions: [
							{ reel: 0, row: 2 },
							{ reel: 1, row: 2 },
							{ reel: 2, row: 2 },
							{ reel: 3, row: 2 },
							{ reel: 4, row: 2 },
						],
						meta: {
							lineIndex: 3,
							multiplier: winMultiplier,
							winWithoutMult: payoutBookAmount,
							globalMult: 1,
							lineMultiplier: winMultiplier,
						},
					},
				],
			},
			{ index: 2, type: 'setTotalWin', amount: payoutBookAmount },
			{ index: 3, type: 'setWin', amount: payoutBookAmount, winLevel: winMultiplier >= 7.5 ? 4 : 3 },
			{ index: 4, type: 'finalWin', amount: payoutBookAmount },
		);
	}

	return {
		status: { statusCode: 'SUCCESS', statusMessage: 'Mock play response' },
		balance: { amount: mockBalanceAmount, currency: options.currency },
		round: {
			roundID: Date.now(),
			amount: betApiAmount,
			payout: payoutAmount,
			payoutMultiplier: winMultiplier,
			active: false,
			mode: options.mode,
			event: '0',
			state,
		},
	};
};

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
			balance: { amount: mockBalanceAmount, currency: 'USD' },
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
	if (!options.rgsUrl) return createMockPlayResponse(options);

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
