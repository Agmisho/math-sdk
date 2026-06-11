import type { RawSymbol, SymbolState } from './types';

export const SYMBOL_SIZE = 120;

export const REEL_PADDING = 0.53;

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
	width: SYMBOL_SIZE * BOARD_DIMENSIONS.x,
	height: SYMBOL_SIZE * BOARD_DIMENSIONS.y,
};

export const BACKGROUND_RATIO = 2039 / 1000;
export const PORTRAIT_BACKGROUND_RATIO = 1242 / 2208;
const PORTRAIT_RATIO = 800 / 1422;
const LANDSCAPE_RATIO = 1600 / 900;
const DESKTOP_RATIO = 1422 / 800;

const DESKTOP_HEIGHT = 800;
const LANDSCAPE_HEIGHT = 900;
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

const HIGH_SYMBOL_SIZE = 0.9;
const LOW_SYMBOL_SIZE = 0.9;
const SPECIAL_SYMBOL_SIZE = 1;

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

const h1Static = { type: 'sprite', assetKey: 'h1.webp', sizeRatios: { width: 1, height: 1 } };
const h2Static = { type: 'sprite', assetKey: 'h2.webp', sizeRatios: { width: 1, height: 1 } };
const h3Static = { type: 'sprite', assetKey: 'h3.webp', sizeRatios: { width: 1, height: 1 } };
const h4Static = { type: 'sprite', assetKey: 'h4.webp', sizeRatios: { width: 1, height: 1 } };
const h5Static = { type: 'sprite', assetKey: 'h5.webp', sizeRatios: { width: 1, height: 1 } };

const l1Static = { type: 'sprite', assetKey: 'l1.webp', sizeRatios: { width: 1, height: 1 } };
const l2Static = { type: 'sprite', assetKey: 'l2.webp', sizeRatios: { width: 1, height: 1 } };
const l3Static = { type: 'sprite', assetKey: 'l3.webp', sizeRatios: { width: 1, height: 1 } };
const l4Static = { type: 'sprite', assetKey: 'l4.webp', sizeRatios: { width: 1, height: 1 } };
const l5Static = {
	type: 'spine',
	assetKey: 'M',
	animationName: 'low_multiplier_static',
	sizeRatios: { width: 0.3, height: 0.3 },
};

const sStatic = { type: 'sprite', assetKey: 's.png', sizeRatios: { width: 1.243, height: 1.243 } };
const wStatic = { type: 'sprite', assetKey: 'w.png', sizeRatios: { width: 1.12, height: 1.12 } };

const wSizeRatios = { width: 1.5 * 0.9, height: SPECIAL_SYMBOL_SIZE * 1.15 };
const sSizeRatios = { width: 2.5, height: SPECIAL_SYMBOL_SIZE * 2.3 };
const multiplierSizeRatios = { width: 0.35, height: 0.35 };

const highSymbol = (staticSymbol: typeof h1Static, assetKey: 'H1' | 'H2' | 'H3' | 'H4' | 'H5', animationName: string) => ({
	explosion,
	win: {
		type: 'spine',
		assetKey,
		animationName,
		sizeRatios: { width: 0.5 * 0.9, height: HIGH_SYMBOL_SIZE * 0.57 },
	},
	postWinStatic: staticSymbol,
	static: staticSymbol,
	spin: staticSymbol,
	land: staticSymbol,
});

const lowSymbol = (staticSymbol: typeof l1Static, assetKey: 'L1' | 'L2' | 'L3' | 'L4' | 'M', animationName: string) => ({
	explosion,
	win: {
		type: 'spine',
		assetKey,
		animationName,
		sizeRatios: { width: 0.5 * 0.75, height: LOW_SYMBOL_SIZE * 0.65 },
	},
	postWinStatic: staticSymbol,
	static: staticSymbol,
	spin: staticSymbol,
	land: staticSymbol,
});

const multiplierSymbol = (label: string) => ({
	explosion,
	win: {
		type: 'spine',
		assetKey: 'M',
		animationName: 'low_multiplier_pay',
		sizeRatios: multiplierSizeRatios,
	},
	postWinStatic: l5Static,
	static: l5Static,
	spin: l5Static,
	land: l5Static,
	label,
});

export const SYMBOL_INFO_MAP = {
	H1: highSymbol(h1Static, 'H1', 'h1'),
	H2: highSymbol(h2Static, 'H2', 'h2'),
	H3: highSymbol(h3Static, 'H3', 'h3'),
	H4: highSymbol(h4Static, 'H4', 'h4'),
	H5: highSymbol(h5Static, 'H5', 'h5'),
	// Temporary placeholder mappings until final Inheritance symbol art is added.
	H6: highSymbol(h1Static, 'H1', 'h1'),
	H7: highSymbol(h2Static, 'H2', 'h2'),
	H8: highSymbol(h3Static, 'H3', 'h3'),
	H9: highSymbol(h4Static, 'H4', 'h4'),
	L1: lowSymbol(l1Static, 'L1', 'l1'),
	L2: lowSymbol(l2Static, 'L2', 'l2'),
	L3: lowSymbol(l3Static, 'L3', 'l3'),
	L4: lowSymbol(l4Static, 'L4', 'l4'),
	L5: lowSymbol(l5Static, 'M', 'low_multiplier_pay'),
	L6: lowSymbol(l5Static, 'M', 'low_multiplier_pay'),
	M2: multiplierSymbol('2x'),
	M5: multiplierSymbol('5x'),
	M10: multiplierSymbol('10x'),
	M20: multiplierSymbol('20x'),
	M100: multiplierSymbol('100x'),
	W: {
		explosion,
		postWinStatic: {
			type: 'sprite',
			assetKey: 'explodedW.png',
			sizeRatios: { width: 0.85, height: 0.85 },
		},
		static: wStatic,
		spin: wStatic,
		win: { type: 'spine', assetKey: 'W', animationName: 'wild_dynamite', sizeRatios: wSizeRatios },
		land: {
			type: 'spine',
			assetKey: 'W',
			animationName: 'wild_dynamite_land',
			sizeRatios: wSizeRatios,
		},
	},
	S: {
		explosion,
		postWinStatic: sStatic,
		static: sStatic,
		spin: {
			type: 'spine',
			assetKey: 'S',
			animationName: 'scatter_spin',
			sizeRatios: sSizeRatios,
		},
		win: { type: 'spine', assetKey: 'S', animationName: 'scatter_win', sizeRatios: sSizeRatios },
		land: {
			type: 'spine',
			assetKey: 'S',
			animationName: 'scatter_land',
			sizeRatios: sSizeRatios,
		},
	},
} as const;

export const SCATTER_LAND_SOUND_MAP = {
	1: 'sfx_scatter_stop_1',
	2: 'sfx_scatter_stop_2',
	3: 'sfx_scatter_stop_3',
	4: 'sfx_scatter_stop_4',
	5: 'sfx_scatter_stop_5',
} as const;
