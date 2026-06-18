import { API_AMOUNT_MULTIPLIER, BOOK_AMOUNT_MULTIPLIER } from 'constants-shared/bet';
import { rgsFetcher } from 'rgs-fetcher';

export * from './types';

const mockReel = (names: string[]) => names.map((name) => ({ name }));
let mockBalanceAmount = 1000 * API_AMOUNT_MULTIPLIER;
let mockSpinIndex = 0;

const mockBoards = [
	[
		mockReel(['H1', 'H3', 'L2', 'H4', 'S']),
		mockReel(['L2', 'H4', 'L3', 'H1', 'M2']),
		mockReel(['H3', 'L1', 'M5', 'H4', 'L2']),
		mockReel(['H4', 'L2', 'H2', 'H1', 'S']),
		mockReel(['L5', 'H1', 'L3', 'H4', 'M2']),
	],
	[
		mockReel(['H3', 'L2', 'H4', 'S', 'L3']),
		mockReel(['H4', 'L3', 'H1', 'M2', 'L6']),
		mockReel(['S', 'M5', 'H4', 'L2', 'H5']),
		mockReel(['L2', 'H2', 'S', 'H1', 'M10']),
		mockReel(['H1', 'L3', 'H4', 'M2', 'S']),
	],
	[
		mockReel(['H1', 'H1', 'H1', 'L2', 'H4']),
		mockReel(['H2', 'H1', 'H4', 'L3', 'H1']),
		mockReel(['L3', 'H1', 'S', 'M5', 'H4']),
		mockReel(['L4', 'H1', 'L2', 'H2', 'S']),
		mockReel(['H5', 'H1', 'H1', 'L3', 'H4']),
	],
];

const createMockPlayResponse = (options: { currency: string; amount: number; mode: string }) => {
	const board = mockBoards[mockSpinIndex % mockBoards.length];
	const isWin = mockSpinIndex % 3 === 2;
	const betApiAmount = Math.round(options.amount * API_AMOUNT_MULTIPLIER);
	const payoutAmount = isWin ? options.amount * 5 : 0;
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
						symbol: 'H1',
						kind: 5,
						win: payoutBookAmount,
						positions: [
							{ reel: 0, row: 1 },
							{ reel: 1, row: 1 },
							{ reel: 2, row: 1 },
							{ reel: 3, row: 1 },
							{ reel: 4, row: 1 },
						],
						meta: {
							lineIndex: 2,
							multiplier: 1,
							winWithoutMult: payoutBookAmount,
							globalMult: 1,
							lineMultiplier: 1,
						},
					},
				],
			},
			{ index: 2, type: 'setTotalWin', amount: payoutBookAmount },
			{ index: 3, type: 'setWin', amount: payoutBookAmount, winLevel: 3 },
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
			payoutMultiplier: isWin ? 5 : 0,
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
