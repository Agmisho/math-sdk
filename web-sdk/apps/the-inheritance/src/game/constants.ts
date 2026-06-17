import type { RawSymbol, SymbolState } from './types';

export const SYMBOL_SIZE = 145;
export const REEL_SPACING = 165;

export const REEL_PADDING = 0.5;

const sym = (name: RawSymbol['name']) => ({ name });

// Initial board includes one padded symbol above and below the 4 visible rows.
export const INITIAL_BOARD: RawSymbol[][] = [
	[sym('L1'), sym('H1'), sym('H3'), sym('L2'), sym('H4'), sym('S')],
	[sym('H2'), sym('L2'), sym('H4'), sym('L3'), sym('H1'), sym('M2')],
	[sym('L3'), sym('H3'), sym('S'), sym('M5'), sym('H4'), sym('L2')],
	[sym('L4'), sym('H4'), sym('L2'), sym('H2'), sym('S'), sym('H1')],
	[sym('H5'), sym('L5'), sym('H1'), sym('L3'), sym('H4'), sym('M2')],
];

export const BOARD_DIMENSIONS = { x: INITIAL_BOARD.length, y: INITIAL_BOARD[0].length - 2 };

export const BOARD_SIZES = {
	width: SYMBOL_SIZE + REEL_SPACING * (BOARD_DIMENSIONS.x - 1),
	height: SYMBOL_SIZE * BOARD_DIMENSIONS.y,
};

export const BACKGROUND_RATIO = 1672 / 941;
export const PORTRAIT_BACKGROUND_RATIO = 1672 / 941;
const PORTRAIT_RATIO = 800 / 1422;
const LANDSCAPE_RATIO = 1672 / 941;
const DESKTOP_RATIO = 1672 / 941;

const DESKTOP_HEIGHT = 941;
const LANDSCAPE_HEIGHT = 941;
const PORTRAIT_HEIGHT = 1422;
export const DESKTOP_MAIN_SIZES = { width: DESKTOP_HEIGHT * DESKTOP_RATIO, height: DESKTOP_HEIGHT };
export const LANDSCAPE_MAIN_SIZES = {
	width: LANDSCAPE_HEIGHT * LANDSCAPE_RATIO,
	height: LANDSCAPE_HEIGHT,
};
export const PORTRAIT_MAIN_SIZES = {
	width: PORTRAIT_HEIGHT * PORTRAIT_RATIO,
	height: PORTRAIT_HEIGHT,
};

export const HIGH_SYMBOLS = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'];

export const INITIAL_SYMBOL_STATE: SymbolState = 'static';

const SPIN_OPTIONS_SHARED = {
	reelBounceBackSpeed: 0.15,
	reelSpinSpeedBeforeBounce: 4,
	reelPaddingMultiplierNormal: 1.2,
	reelPaddingMultiplierAnticipated: 10,
	reelSpinDelay: 145,
};

export const SPIN_OPTIONS_DEFAULT = {
	...SPIN_OPTIONS_SHARED,
	reelPreSpinSpeed: 2,
	reelSpinSpeed: 3,
	reelBounceSizeMulti: 0.3,
};

export const SPIN_OPTIONS_FAST = {
	...SPIN_OPTIONS_SHARED,
	reelPreSpinSpeed: 5,
	reelSpinSpeed: 5,
	reelBounceSizeMulti: 0.05,
};

export const MOTION_BLUR_VELOCITY = 31;

export const zIndexes = {
	background: {
		backdrop: -3,
		normal: -2,
		feature: -1,
	},
};
