import baseReelsCsv from '../../../../games/2_0_The_Inheritance/reels/BR0.csv?raw';
import freeReelsCsv from '../../../../games/2_0_The_Inheritance/reels/FR0.csv?raw';

const LEGACY_KEY_SYMBOL = 'H4';
const VAULT_SCATTER_SYMBOL = 'S';
const VISIBLE_ROWS = 5;
const TOP_PADDING_ROWS = 1;
const BOARD_ROWS_WITH_PADDING = VISIBLE_ROWS + 2;
const BASE_VAULT_TRIGGER_INTERVAL = 255;
const SCATTER_BOOST_VAULT_TRIGGER_INTERVAL = 236;

export const MAX_LOCAL_FREE_SPINS = 100;
export const BASE_FREE_SPIN_AWARDS: Record<number, number> = { 3: 8, 4: 12, 5: 15 };
export const FREE_SPIN_RETRIGGER_AWARDS: Record<number, number> = { 2: 3, 3: 5, 4: 8, 5: 12 };

const parseMathReels = (csv: string) => {
	const rows = csv
		.trim()
		.split(/\r?\n/)
		.map((row) => row.split(','));
	return Array.from({ length: rows[0]?.length || 0 }, (_, reelIndex) =>
		rows.map((row) => row[reelIndex]),
	);
};

const BASE_REELS = parseMathReels(baseReelsCsv);
const FREE_REELS = parseMathReels(freeReelsCsv);

const hashSpin = (spinIndex: number, reelIndex: number, salt: number) => {
	let value = (spinIndex + 1) * 0x9e3779b1;
	value ^= (reelIndex + 1) * 0x85ebca6b;
	value ^= (salt + 1) * 0xc2b2ae35;
	value ^= value >>> 16;
	value = Math.imul(value, 0x7feb352d);
	value ^= value >>> 15;
	return value >>> 0;
};

const drawMathBoard = (reels: string[][], spinIndex: number, salt = 0) =>
	reels.map((reel, reelIndex) => {
		const stop = hashSpin(spinIndex, reelIndex, salt) % reel.length;
		return Array.from({ length: BOARD_ROWS_WITH_PADDING }, (_, rowIndex) => ({
			name: reel[(stop + rowIndex - TOP_PADDING_ROWS + reel.length) % reel.length],
		}));
	});

const forceVaultTriggerBoard = (board: { name: string }[][]) => {
	const result = board.map((reel) => reel.map((symbol) => ({ ...symbol })));
	const triggerPositions = [
		{ reel: 0, row: 1 },
		{ reel: 2, row: 3 },
		{ reel: 4, row: 5 },
	];
	for (const position of triggerPositions) result[position.reel][position.row] = { name: VAULT_SCATTER_SYMBOL };
	return result;
};

export const drawBaseMathBoard = (
	mode: 'base' | 'scatter_boost',
	spinIndex: number,
	modeSpinIndex: number,
) => {
	const board = drawMathBoard(BASE_REELS, spinIndex);
	const triggerInterval =
		mode === 'scatter_boost'
			? SCATTER_BOOST_VAULT_TRIGGER_INTERVAL
			: BASE_VAULT_TRIGGER_INTERVAL;
	return modeSpinIndex % triggerInterval === triggerInterval - 1
		? forceVaultTriggerBoard(board)
		: board;
};

export const drawFreeMathBoard = (spinIndex: number, freeSpinIndex: number) =>
	drawMathBoard(FREE_REELS, spinIndex, freeSpinIndex + 1);

export const drawBonusTriggerBoard = (spinIndex: number) =>
	forceVaultTriggerBoard(drawMathBoard(BASE_REELS, spinIndex, 1000)).map((reel) =>
		reel.map((symbol) => ({
			name: symbol.name === LEGACY_KEY_SYMBOL ? 'H3' : symbol.name,
		})),
	);

export const getTriggerAward = (scatterCount: number, awards: Record<number, number>) =>
	awards[Math.min(scatterCount, 5)] || 0;
