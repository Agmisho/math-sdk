import { API_AMOUNT_MULTIPLIER, BOOK_AMOUNT_MULTIPLIER } from 'constants-shared/bet';
import { rgsFetcher } from 'rgs-fetcher';

export * from './types';

const mockReel = (names: string[]) => names.map((name) => ({ name }));
let mockBalanceAmount = 1000 * API_AMOUNT_MULTIPLIER;
let mockSpinIndex = 0;
let mockLegacyEligibleSpinIndex = 0;
let mockLegacyKeyCount = 0;
const BONUS_BUY_COST_MULTIPLIER = 100;
const BONUS_BUY_FREE_SPINS = 10;
const SCATTER_BOOST_COST_MULTIPLIER = 2;
const LEGACY_KEY_TARGET = 10;
const LEGACY_KEY_SYMBOL = 'H4';
const VAULT_SCATTER_SYMBOL = 'S';
const VISIBLE_ROWS = 5;
const TOP_PADDING_ROWS = 1;

const MULTIPLIER_SYMBOL_VALUES: Record<string, number> = {
	M2: 2,
	M5: 5,
	M10: 10,
	M20: 20,
	M100: 100,
};

const PAYTABLE: Record<string, Record<number, number>> = {
	W: { 5: 20 },
	H1: { 3: 0.5, 4: 2.5, 5: 5 },
	H2: { 3: 0.5, 4: 2.5, 5: 5 },
	H3: { 3: 1, 4: 5, 5: 10 },
	H4: { 3: 1, 4: 5, 5: 10 },
	H5: { 3: 2, 4: 1, 5: 20 },
	H6: { 3: 2, 4: 1, 5: 20 },
	H7: { 3: 3, 4: 6, 5: 15 },
	H8: { 3: 2, 4: 5, 5: 12 },
	H9: { 3: 1.5, 4: 4, 5: 10 },
	L1: { 3: 0.1, 4: 0.5, 5: 1 },
	L2: { 3: 0.1, 4: 0.5, 5: 1 },
	L3: { 3: 0.1, 4: 0.5, 5: 1 },
	L4: { 3: 0.1, 4: 0.5, 5: 1 },
	L5: { 3: 0.1, 4: 0.5, 5: 1 },
	L6: { 3: 0.1, 4: 0.4, 5: 1.5 },
};

const PAYLINES = [
	[0, 0, 0, 0, 0],
	[1, 1, 1, 1, 1],
	[2, 2, 2, 2, 2],
	[3, 3, 3, 3, 3],
	[4, 4, 4, 4, 4],
	[0, 1, 2, 3, 4],
	[4, 3, 2, 1, 0],
	[0, 1, 0, 1, 0],
	[1, 0, 1, 0, 1],
	[1, 2, 1, 2, 1],
	[2, 1, 2, 1, 2],
	[2, 3, 2, 3, 2],
	[3, 2, 3, 2, 3],
	[3, 4, 3, 4, 3],
	[4, 3, 4, 3, 4],
] as const;

type MockSymbol = {
	name: string;
	scatter?: boolean;
	wild?: boolean;
	multiplier?: number;
};

type MockBoard = MockSymbol[][];

const decorateSymbol = ({ name }: { name: string }): MockSymbol => ({
	name,
	...(name === 'S' ? { scatter: true } : {}),
	...(name === 'W' ? { wild: true } : {}),
	...(MULTIPLIER_SYMBOL_VALUES[name] ? { multiplier: MULTIPLIER_SYMBOL_VALUES[name] } : {}),
});

const decorateBoard = (board: { name: string }[][]): MockBoard =>
	board.map((reel) => reel.map((symbol) => decorateSymbol(symbol)));

const withoutLegacyKeys = (board: { name: string }[][]) =>
	board.map((reel) =>
		reel.map((symbol) => ({ name: symbol.name === LEGACY_KEY_SYMBOL ? 'H3' : symbol.name })),
	);

const createRareLegacyKeyBoard = (board: { name: string }[][], spinIndex: number) => {
	const result = withoutLegacyKeys(board);
	if (spinIndex % 40 !== 39) return result;

	const reelIndex = Math.floor(spinIndex / 40) % result.length;
	const rowIndex = TOP_PADDING_ROWS + Math.floor(spinIndex / 200) % VISIBLE_ROWS;
	result[reelIndex][rowIndex] = { name: LEGACY_KEY_SYMBOL };
	return result;
};

const toBookAmount = (amount: number) => Math.round(amount * BOOK_AMOUNT_MULTIPLIER);

const normalizeMode = (mode: string) => {
	const key = mode.toLowerCase();
	if (key === 'bonus') return 'bonus';
	if (key === 'scatter_boost' || key === 'scatterboost' || key === 'scatter-boost') return 'scatter_boost';
	return 'base';
};

const getModeCostMultiplier = (mode: string) => {
	const normalizedMode = normalizeMode(mode);
	if (normalizedMode === 'bonus') return BONUS_BUY_COST_MULTIPLIER;
	if (normalizedMode === 'scatter_boost') return SCATTER_BOOST_COST_MULTIPLIER;
	return 1;
};

const getWinLevel = (winMultiplier: number) => {
	if (winMultiplier < 0.1) return 1;
	if (winMultiplier < 1) return 2;
	if (winMultiplier < 2) return 3;
	if (winMultiplier < 5) return 4;
	if (winMultiplier < 15) return 5;
	if (winMultiplier < 30) return 6;
	if (winMultiplier < 50) return 7;
	if (winMultiplier < 100) return 8;
	if (winMultiplier < 5000) return 9;
	return 10;
};

const getEndFeatureWinLevel = (winMultiplier: number) => {
	if (winMultiplier < 1) return 1;
	if (winMultiplier < 5) return 2;
	if (winMultiplier < 10) return 3;
	if (winMultiplier < 20) return 4;
	if (winMultiplier < 50) return 5;
	if (winMultiplier < 100) return 6;
	if (winMultiplier < 500) return 7;
	if (winMultiplier < 2000) return 8;
	if (winMultiplier < 5000) return 9;
	return 10;
};

const getVisibleSymbols = (reel: MockSymbol[]) =>
	reel.slice(TOP_PADDING_ROWS, TOP_PADDING_ROWS + VISIBLE_ROWS);

const getGlobalMultiplier = (board: MockBoard) =>
	Math.max(
		1,
		...board.flatMap((reel) =>
			getVisibleSymbols(reel).map((symbol) => MULTIPLIER_SYMBOL_VALUES[symbol.name] || 1),
		),
	);

const getVisiblePositions = (board: MockBoard, symbolName: string) =>
	board.flatMap((reel, reelIndex) =>
		getVisibleSymbols(reel).flatMap((symbol, rowIndex) =>
			symbol.name === symbolName
				? [{ reel: reelIndex, row: rowIndex + TOP_PADDING_ROWS }]
				: [],
		),
	);

const calculateMansionLevel = (collected: number) => {
	if (collected >= 10) return 5;
	if (collected >= 8) return 4;
	if (collected >= 5) return 3;
	if (collected >= 3) return 2;
	return 1;
};

const calculateDisplayMultiplier = (collected: number) => {
	if (collected >= 10) return 10;
	if (collected >= 9) return 7;
	if (collected >= 7) return 5;
	if (collected >= 5) return 4;
	if (collected >= 3) return 3;
	if (collected >= 1) return 2;
	return 1;
};

const createCollectionUpdateEvent = ({
	index,
	board,
	gameType,
	mode,
}: {
	index: number;
	board: MockBoard;
	gameType: 'basegame' | 'freegame';
	mode: string;
}) => {
	const positions = gameType === 'basegame' && normalizeMode(mode) !== 'bonus' ? getVisiblePositions(board, LEGACY_KEY_SYMBOL) : [];
	if (positions.length > 0) mockLegacyKeyCount = Math.min(LEGACY_KEY_TARGET, mockLegacyKeyCount + positions.length);

	return {
		index,
		type: 'collectionUpdate',
		collected: mockLegacyKeyCount,
		target: LEGACY_KEY_TARGET,
		mansionLevel: calculateMansionLevel(mockLegacyKeyCount),
		displayMultiplier: calculateDisplayMultiplier(mockLegacyKeyCount),
		positions,
		gameType,
	};
};

const createCollectionResetEvent = (index: number) => {
	mockLegacyKeyCount = 0;
	return {
		index,
		type: 'collectionUpdate',
		collected: mockLegacyKeyCount,
		target: LEGACY_KEY_TARGET,
		mansionLevel: calculateMansionLevel(mockLegacyKeyCount),
		displayMultiplier: calculateDisplayMultiplier(mockLegacyKeyCount),
		positions: [],
		gameType: 'basegame',
	};
};

const evaluateBoardWins = (board: MockBoard) => {
	const globalMultiplier = getGlobalMultiplier(board);

	const wins = PAYLINES.flatMap((line, lineIndex) => {
		const names = line.map(
			(row, reel) => board[reel]?.[row + TOP_PADDING_ROWS]?.name || '',
		);
		const targetSymbol = names.find((name) => name !== 'W') || 'W';
		const symbolPaytable = PAYTABLE[targetSymbol];
		if (!symbolPaytable) return [];

		let count = 0;
		for (const name of names) {
			if (name === targetSymbol || name === 'W') {
				count += 1;
			} else {
				break;
			}
		}

		const winWithoutMult = symbolPaytable[count];
		if (!winWithoutMult) return [];

		const winMultiplier = winWithoutMult * globalMultiplier;
		return [
			{
				symbol: targetSymbol,
				kind: count,
				win: toBookAmount(winMultiplier),
				positions: line
					.slice(0, count)
					.map((row, reel) => ({ reel, row: row + TOP_PADDING_ROWS })),
				meta: {
					lineIndex: lineIndex + 1,
					multiplier: globalMultiplier,
					winWithoutMult: toBookAmount(winWithoutMult),
					globalMult: globalMultiplier,
					lineMultiplier: globalMultiplier,
				},
			},
		];
	});

	const totalWinMultiplier = wins.reduce((total, win) => total + win.win / BOOK_AMOUNT_MULTIPLIER, 0);
	return { wins, totalWinMultiplier, totalWinBookAmount: toBookAmount(totalWinMultiplier) };
};

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

const mockBonusTriggerBoard = mockReel(['S', 'H4', 'L1', 'L2', 'H3', 'L5', 'L6']);
const mockBonusBoards = [
	[
		mockReel(['L1', 'L5', 'H3', 'L2', 'H4', 'S', 'L3']),
		mockReel(['L1', 'L2', 'H4', 'L3', 'H1', 'M2', 'L6']),
		mockReel(['L1', 'H3', 'L2', 'M5', 'H4', 'L2', 'H5']),
		mockReel(['L4', 'H4', 'L2', 'H2', 'H6', 'H1', 'M10']),
		mockReel(['H5', 'L5', 'H1', 'L3', 'H4', 'M2', 'S']),
	],
	[
		mockReel(['H3', 'L2', 'H4', 'S', 'L3', 'H5', 'L4']),
		mockReel(['L2', 'L3', 'H1', 'M2', 'L6', 'H2', 'S']),
		mockReel(['L2', 'M5', 'H4', 'L2', 'H5', 'W', 'L1']),
		mockReel(['L2', 'H2', 'H6', 'H1', 'M10', 'L5', 'H3']),
		mockReel(['H1', 'L3', 'H4', 'M2', 'S', 'L6', 'H2']),
	],
	[
		mockReel(['H4', 'H1', 'H3', 'L2', 'L4', 'S', 'L3']),
		mockReel(['H4', 'L2', 'H1', 'L3', 'H1', 'M2', 'L6']),
		mockReel(['H4', 'H3', 'L2', 'M5', 'H4', 'L2', 'H5']),
		mockReel(['L4', 'H4', 'L2', 'H2', 'H6', 'H1', 'M10']),
		mockReel(['H5', 'L5', 'H1', 'L3', 'H4', 'M2', 'S']),
	],
	[
		mockReel(['L3', 'H1', 'H3', 'L2', 'H4', 'S', 'L3']),
		mockReel(['L4', 'L2', 'H4', 'L3', 'H1', 'M2', 'L6']),
		mockReel(['L5', 'H3', 'L2', 'M5', 'H4', 'L2', 'H5']),
		mockReel(['H6', 'H4', 'L2', 'H2', 'H6', 'H1', 'M10']),
		mockReel(['H5', 'L5', 'H1', 'L3', 'H4', 'M2', 'S']),
	],
	[
		mockReel(['L5', 'H1', 'L1', 'L2', 'H4', 'S', 'L3']),
		mockReel(['L5', 'L2', 'H4', 'L3', 'H1', 'M2', 'L6']),
		mockReel(['L5', 'H3', 'L2', 'M5', 'H4', 'L2', 'H5']),
		mockReel(['L4', 'H4', 'L2', 'H2', 'H6', 'H1', 'M10']),
		mockReel(['H5', 'L5', 'H1', 'L3', 'H4', 'M2', 'S']),
	],
	[
		mockReel(['H2', 'H1', 'L1', 'L2', 'H4', 'S', 'L3']),
		mockReel(['H2', 'L2', 'H4', 'L3', 'H1', 'M2', 'L6']),
		mockReel(['L3', 'H3', 'L2', 'M5', 'H4', 'L2', 'H5']),
		mockReel(['L4', 'H4', 'L2', 'H2', 'H6', 'H1', 'M10']),
		mockReel(['H5', 'L5', 'H1', 'L3', 'H4', 'M2', 'S']),
	],
	[
		mockReel(['L1', 'H1', 'H3', 'L2', 'H4', 'S', 'L3']),
		mockReel(['H2', 'L2', 'H4', 'L3', 'H1', 'M2', 'L6']),
		mockReel(['L3', 'H3', 'L2', 'M5', 'H4', 'L2', 'H5']),
		mockReel(['L4', 'H4', 'L2', 'H2', 'H6', 'H1', 'M10']),
		mockReel(['H5', 'L5', 'H1', 'L3', 'H4', 'M2', 'S']),
	],
	[
		mockReel(['L4', 'H1', 'H3', 'L2', 'H4', 'S', 'L3']),
		mockReel(['L4', 'L2', 'H4', 'L3', 'H1', 'M2', 'L6']),
		mockReel(['L4', 'H3', 'L2', 'M5', 'H4', 'L2', 'H5']),
		mockReel(['L4', 'H4', 'L2', 'H2', 'H6', 'H1', 'M10']),
		mockReel(['H5', 'L5', 'H1', 'L3', 'H4', 'M2', 'S']),
	],
	[
		mockReel(['H1', 'H1', 'H3', 'L2', 'H4', 'S', 'L3']),
		mockReel(['H1', 'L2', 'H4', 'L3', 'H1', 'M2', 'L6']),
		mockReel(['L3', 'H3', 'L2', 'M5', 'H4', 'L2', 'H5']),
		mockReel(['L4', 'H4', 'L2', 'H2', 'H6', 'H1', 'M10']),
		mockReel(['H5', 'L5', 'H1', 'L3', 'H4', 'M2', 'S']),
	],
	[
		mockReel(['L6', 'H1', 'H3', 'L2', 'H4', 'S', 'L3']),
		mockReel(['L6', 'L2', 'H4', 'L3', 'H1', 'M2', 'L6']),
		mockReel(['L6', 'H3', 'L2', 'M5', 'H4', 'L2', 'H5']),
		mockReel(['L4', 'H4', 'L2', 'H2', 'H6', 'H1', 'M10']),
		mockReel(['H5', 'L5', 'H1', 'L3', 'H4', 'M2', 'S']),
	],
];

const pushEvaluatedBoardEvents = ({
	state,
	board,
	startIndex,
	cumulativeWinMultiplier,
}: {
	state: any[];
	board: MockBoard;
	startIndex: number;
	cumulativeWinMultiplier: number;
}) => {
	const { wins, totalWinMultiplier, totalWinBookAmount } = evaluateBoardWins(board);
	const nextCumulativeWinMultiplier = cumulativeWinMultiplier + totalWinMultiplier;
	const nextCumulativeBookAmount = toBookAmount(nextCumulativeWinMultiplier);
	let index = startIndex;

	if (wins.length > 0) {
		state.push({
			index: index++,
			type: 'winInfo',
			totalWin: totalWinBookAmount,
			wins,
		});
		state.push({
			index: index++,
			type: 'setWin',
			amount: totalWinBookAmount,
			winLevel: getWinLevel(totalWinMultiplier),
		});
	}

	state.push({
		index: index++,
		type: 'setTotalWin',
		amount: nextCumulativeBookAmount,
	});

	return { index, cumulativeWinMultiplier: nextCumulativeWinMultiplier };
};

const createMockPlayResponse = (options: { currency: string; amount: number; mode: string }) => {
	const normalizedMode = normalizeMode(options.mode);
	const costMultiplier = getModeCostMultiplier(options.mode);
	const costAmount = options.amount * costMultiplier;
	const costApiAmount = Math.round(costAmount * API_AMOUNT_MULTIPLIER);
	if (mockBalanceAmount < costApiAmount) {
		return {
			error: 'INSUFFICIENT_BALANCE',
			message: `Insufficient balance for ${normalizedMode} bet.`,
		};
	}

	if (normalizedMode === 'bonus') return createMockBonusBuyResponse(options, costApiAmount);

	const spinIndex = mockSpinIndex;
	const legacySpinIndex = mockLegacyEligibleSpinIndex;
	const board = decorateBoard(createRareLegacyKeyBoard(mockBoards[spinIndex % mockBoards.length], legacySpinIndex));
	const legacyCreditAvailable = mockLegacyKeyCount >= LEGACY_KEY_TARGET;
	const { wins, totalWinMultiplier, totalWinBookAmount } = evaluateBoardWins(board);
	let cumulativeWinMultiplier = totalWinMultiplier;
	let cumulativeWinBookAmount = totalWinBookAmount;
	let index = 0;

	const state: any[] = [
		{
			index: index++,
			type: 'reveal',
			gameType: 'basegame',
			paddingPositions: [0, 0, 0, 0, 0],
			anticipation: [0, 0, 0, 0, 0],
			board,
		},
	];
	state.push(createCollectionUpdateEvent({ index: index++, board, gameType: 'basegame', mode: normalizedMode }));

	if (wins.length > 0) {
		state.push({
			index: index++,
			type: 'winInfo',
			totalWin: totalWinBookAmount,
			wins,
		});
		state.push({ index: index++, type: 'setWin', amount: totalWinBookAmount, winLevel: getWinLevel(totalWinMultiplier) });
	}
	state.push({ index: index++, type: 'setTotalWin', amount: totalWinBookAmount });

	const naturalScatterPositions = getVisiblePositions(board, VAULT_SCATTER_SYMBOL);
	const usesLegacyScatterCredit = legacyCreditAvailable && naturalScatterPositions.length === 2;
	if (usesLegacyScatterCredit) {
		state.push({
			index: index++,
			type: 'legacyScatterCredit',
			collected: LEGACY_KEY_TARGET,
			target: LEGACY_KEY_TARGET,
			virtualScatters: 1,
			naturalScatters: naturalScatterPositions.length,
			effectiveScatters: naturalScatterPositions.length + 1,
			used: true,
			gameType: 'basegame',
		});
		state.push({
			index: index++,
			type: 'freeSpinTrigger',
			totalFs: 8,
			positions: naturalScatterPositions,
		});
		state.push(createCollectionResetEvent(index++));

		for (let freeSpinIndex = 0; freeSpinIndex < 8; freeSpinIndex += 1) {
			const freeSpinBoard = decorateBoard(
				withoutLegacyKeys(mockBonusBoards[(spinIndex + freeSpinIndex) % mockBonusBoards.length]),
			);
			state.push({
				index: index++,
				type: 'updateFreeSpin',
				amount: freeSpinIndex,
				total: 8,
			});
			state.push({
				index: index++,
				type: 'reveal',
				gameType: 'freegame',
				paddingPositions: [0, 0, 0, 0, 0],
				anticipation: [0, 0, 0, 0, 0],
				board: freeSpinBoard,
			});
			state.push(createCollectionUpdateEvent({ index: index++, board: freeSpinBoard, gameType: 'freegame', mode: normalizedMode }));
			const evaluated = pushEvaluatedBoardEvents({
				state,
				board: freeSpinBoard,
				startIndex: index,
				cumulativeWinMultiplier,
			});
			index = evaluated.index;
			cumulativeWinMultiplier = evaluated.cumulativeWinMultiplier;
			cumulativeWinBookAmount = toBookAmount(cumulativeWinMultiplier);
		}

		state.push({
			index: index++,
			type: 'freeSpinEnd',
			amount: cumulativeWinBookAmount,
			winLevel: getEndFeatureWinLevel(cumulativeWinMultiplier),
		});
	}

	state.push({ index: index++, type: 'finalWin', amount: cumulativeWinBookAmount });

	const payoutAmount = options.amount * cumulativeWinMultiplier;
	const payoutApiAmount = Math.round(payoutAmount * API_AMOUNT_MULTIPLIER);
	mockSpinIndex += 1;
	mockLegacyEligibleSpinIndex += 1;
	mockBalanceAmount = Math.max(0, mockBalanceAmount - costApiAmount + payoutApiAmount);

	return {
		status: { statusCode: 'SUCCESS', statusMessage: 'Mock play response' },
		balance: { amount: mockBalanceAmount, currency: options.currency },
		round: {
			roundID: Date.now(),
			amount: costApiAmount,
			payout: payoutAmount,
			payoutMultiplier: cumulativeWinMultiplier,
			active: false,
			mode: options.mode,
			event: '0',
			state,
		},
	};
};

const createMockBonusBuyResponse = (
	options: { currency: string; amount: number; mode: string },
	costApiAmount: number,
) => {
	let index = 0;
	let cumulativeWinMultiplier = 0;
	const state: any[] = [
		{
			index: index++,
			type: 'reveal',
			gameType: 'basegame',
			paddingPositions: [0, 0, 0, 0, 0],
			anticipation: [0, 0, 1, 2, 3],
			board: decorateBoard(withoutLegacyKeys([
				mockBonusTriggerBoard,
				mockReel(['H2', 'S', 'H4', 'L3', 'H1', 'M2', 'L6']),
				mockReel(['L3', 'H3', 'S', 'M5', 'H4', 'L2', 'H5']),
				mockReel(['L4', 'H4', 'L2', 'H2', 'H6', 'H1', 'M10']),
				mockReel(['H5', 'L5', 'H1', 'L3', 'H4', 'M2', 'S']),
			])),
		},
		{
			index: index++,
			type: 'setTotalWin',
			amount: 0,
		},
		{
			index: index++,
			type: 'freeSpinTrigger',
			totalFs: BONUS_BUY_FREE_SPINS,
			positions: [
				{ reel: 0, row: 0 },
				{ reel: 1, row: 1 },
				{ reel: 2, row: 2 },
				{ reel: 4, row: 4 },
			],
		},
	];

	for (let freeSpinIndex = 0; freeSpinIndex < BONUS_BUY_FREE_SPINS; freeSpinIndex += 1) {
		const board = decorateBoard(
			withoutLegacyKeys(mockBonusBoards[(mockSpinIndex + freeSpinIndex) % mockBonusBoards.length]),
		);
		state.push({
			index: index++,
			type: 'updateFreeSpin',
			amount: freeSpinIndex,
			total: BONUS_BUY_FREE_SPINS,
		});
		state.push({
			index: index++,
			type: 'reveal',
			gameType: 'freegame',
			paddingPositions: [0, 0, 0, 0, 0],
			anticipation: [0, 0, 0, 0, 0],
			board,
		});
		const evaluated = pushEvaluatedBoardEvents({
			state,
			board,
			startIndex: index,
			cumulativeWinMultiplier,
		});
		index = evaluated.index;
		cumulativeWinMultiplier = evaluated.cumulativeWinMultiplier;
	}

	const payoutAmount = options.amount * cumulativeWinMultiplier;
	const payoutApiAmount = Math.round(payoutAmount * API_AMOUNT_MULTIPLIER);
	const payoutBookAmount = toBookAmount(cumulativeWinMultiplier);
	mockSpinIndex += 1;
	mockBalanceAmount = Math.max(0, mockBalanceAmount - costApiAmount + payoutApiAmount);
	state.push({
		index: index++,
		type: 'freeSpinEnd',
		amount: payoutBookAmount,
		winLevel: getEndFeatureWinLevel(cumulativeWinMultiplier),
	});
	state.push({
		index: index++,
		type: 'finalWin',
		amount: payoutBookAmount,
	});

	return {
		status: { statusCode: 'SUCCESS', statusMessage: 'Mock bonus buy response' },
		balance: { amount: mockBalanceAmount, currency: options.currency },
		round: {
			roundID: Date.now(),
			amount: costApiAmount,
			payout: payoutAmount,
			payoutMultiplier: cumulativeWinMultiplier,
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
	if (!options.rgsUrl) {
		return {
			status: { statusCode: 'SUCCESS', statusMessage: 'Mock authenticate response' },
			balance: { amount: mockBalanceAmount, currency: 'USD' },
			config: {
				jurisdiction: {
					socialCasino: false,
					disabledFullscreen: false,
					disabledTurbo: false,
					disabledSuperTurbo: false,
					disabledAutoplay: false,
					disabledSlamstop: false,
					disabledSpacebar: false,
					disabledBuyFeature: false,
					displayNetPosition: false,
					displayRTP: false,
					displaySessionTimer: false,
					minimumRoundDuration: 0,
				},
			},
		};
	}

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
	if (!options.rgsUrl) {
		return {
			status: { statusCode: 'SUCCESS', statusMessage: 'Mock event response' },
			balance: { amount: mockBalanceAmount, currency: 'USD' },
		};
	}

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
