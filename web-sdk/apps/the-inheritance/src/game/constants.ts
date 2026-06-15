import type { RawSymbol, SymbolState } from './types';

export const SYMBOL_SIZE = 145;
export const REEL_SPACING = 145;

export const REEL_PADDING = 0.5;

const sym = (name: RawSymbol['name']) => ({ name });

// Initial board includes one padded symbol above and below the 5 visible rows.
export const INITIAL_BOARD: RawSymbol[][] = [
	[sym('L1'), sym('H1'), sym('H3'), sym('L2'), sym('H4'), sym('S'), sym('L3')],
	[sym('H2'), sym('L2'), sym('H4'), sym('L3'), sym('H1'), sym('M2'), sym('L6')],
	[sym('L3'), sym('H3'), sym('S'), sym('M5'), sym('H4'), sym('L2'), sym('H1')],
	[sym('L4'), sym('H4'), sym('L2'), sym('H2'), sym('S'), sym('H1'), sym('L5')],
	[sym('H5'), sym('L5'), sym('H1'), sym('L3'), sym('H4'), sym('M2'), sym('S')],
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

const explosion = {
	type: 'spine',
	assetKey: 'explosion',
	animationName: 'explosion',
	sizeRatios: { width: 1, height: 1 },
};

const symbolSprite = (assetKey: RawSymbol['name'], width = 0.82, height = 0.82) => ({
	type: 'sprite',
	assetKey,
	sizeRatios: { width, height },
});

const symbolInfo = (assetKey: RawSymbol['name'], width = 0.82, height = 0.82) => {
	const sprite = symbolSprite(assetKey, width, height);
	return {
		explosion,
		win: sprite,
		postWinStatic: sprite,
		static: sprite,
		spin: sprite,
		land: sprite,
	};
};

export const SYMBOL_INFO_MAP = {
	S: symbolInfo('S', 0.9, 0.9),
	W: symbolInfo('W', 0.9, 0.9),
	M2: symbolInfo('M2', 0.86, 0.86),
	M5: symbolInfo('M5', 0.86, 0.86),
	M10: symbolInfo('M10', 0.86, 0.86),
	M20: symbolInfo('M20', 0.86, 0.86),
	M100: symbolInfo('M100', 0.86, 0.86),
	H1: symbolInfo('H1'),
	H2: symbolInfo('H2'),
	H3: symbolInfo('H3'),
	H4: symbolInfo('H4'),
	H5: symbolInfo('H5'),
	H6: symbolInfo('H6'),
	H7: symbolInfo('H7'),
	H8: symbolInfo('H8'),
	H9: symbolInfo('H9'),
	L1: symbolInfo('L1'),
	L2: symbolInfo('L2'),
	L3: symbolInfo('L3'),
	L4: symbolInfo('L4'),
	L5: symbolInfo('L5'),
	L6: symbolInfo('L6'),
} as const;

export const SCATTER_LAND_SOUND_MAP = {
	1: 'sfx_scatter_stop_1',
	2: 'sfx_scatter_stop_2',
	3: 'sfx_scatter_stop_3',
	4: 'sfx_scatter_stop_4',
	5: 'sfx_scatter_stop_5',
} as const;
