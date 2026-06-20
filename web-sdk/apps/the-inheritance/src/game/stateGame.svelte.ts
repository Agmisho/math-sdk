import _ from 'lodash';
import type { Tween } from 'svelte/motion';
import { stateBet } from 'state-shared';
import { createEnhanceBoard, createReelForSpinning } from 'utils-slots';
import { createGetWinLevelDataByWinLevelAlias } from 'utils-shared/winLevel';
import type { GameType, RawSymbol, SymbolState } from './types';
import { stateLayoutDerived } from './stateLayout';
import { winLevelMap } from './winLevelMap';
import { eventEmitter } from './eventEmitter';
import { SYMBOL_SIZE, BOARD_SIZES, INITIAL_BOARD, BOARD_DIMENSIONS, SPIN_OPTIONS_DEFAULT, SPIN_OPTIONS_FAST, INITIAL_SYMBOL_STATE, SCATTER_LAND_SOUND_MAP } from './constants';

const FRAME_IMAGE_SIZES = { width: 1358, height: 804 } as const;
const FRAME_RATIO = FRAME_IMAGE_SIZES.width / FRAME_IMAGE_SIZES.height;
const FRAME_PLAYABLE_GRID = { left: 226, top: 44, width: 1079, height: 713 } as const;

const frameImageRatioX = (value: number) => value / FRAME_IMAGE_SIZES.width;
const frameImageRatioY = (value: number) => value / FRAME_IMAGE_SIZES.height;

const onSymbolLand = ({ rawSymbol }: { rawSymbol: RawSymbol }) => {
	if (rawSymbol.name === 'S') {
		eventEmitter.broadcast({ type: 'soundScatterCounterIncrease' });
		eventEmitter.broadcast({ type: 'soundOnce', name: SCATTER_LAND_SOUND_MAP[scatterLandIndex()] });
	}
	if (rawSymbol.name === 'H4') stateGame.keyCounter += 1;
	if (rawSymbol.name === 'W') eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
};

const board = _.range(BOARD_DIMENSIONS.x).map((reelIndex) => {
	const reel = createReelForSpinning({
		reelIndex,
		symbolHeight: SYMBOL_SIZE,
		initialSymbols: INITIAL_BOARD[reelIndex],
		initialSymbolState: INITIAL_SYMBOL_STATE,
		onReelStopping: () => eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_reel_stop_1', forcePlay: !stateBet.isTurbo }),
		onSymbolLand,
	});
	reel.reelState.spinOptions = () => reel.reelState.spinType === 'fast' ? SPIN_OPTIONS_FAST : SPIN_OPTIONS_DEFAULT;
	return reel;
});

export type Reel = (typeof board)[number];
export type ReelSymbol = Reel['reelState']['symbols'][number];

export type MultiplierSymbol = {
	initX: number;
	initY: number;
	symbolX: Tween<number>;
	symbolY: Tween<number>;
	rawSymbol: RawSymbol;
	symbolState: SymbolState;
	oncomplete: () => void;
};

export const stateGame = $state({
	board,
	gameType: 'basegame' as GameType,
	multiplierBoard: [] as (MultiplierSymbol | undefined)[][],
	scatterCounter: 0,
	keyCounter: 0,
});

const frameLayout = () => {
	const canvas = stateLayoutDerived.canvasSizes();
	const isPortrait = canvas.height > canvas.width * 1.05;
<<<<<<< HEAD
	const frameWidth = Math.min(canvas.width * (isPortrait ? 0.86 : 0.64), canvas.height * (isPortrait ? 0.47 : 0.58) * FRAME_RATIO);
	const frameHeight = frameWidth / FRAME_RATIO;
	const frameX = canvas.width * 0.5 + frameWidth * FRAME_OFFSET_X;
	const frameY = canvas.height * (isPortrait ? 0.13 : 0.08) + frameHeight / 2;
	const scale = Math.min((frameWidth * GRID_WIDTH) / BOARD_SIZES.width, (frameHeight * GRID_HEIGHT) / BOARD_SIZES.height);
=======
	const width = Math.min(
		canvas.width * (isPortrait ? 0.86 : 0.64),
		canvas.height * (isPortrait ? 0.47 : 0.58) * FRAME_RATIO,
	);
	const height = width / FRAME_RATIO;
	const x = canvas.width * 0.5;
	const y = canvas.height * (isPortrait ? 0.13 : 0.08) + height / 2;
	const grid = {
		x: x + width * (frameImageRatioX(FRAME_PLAYABLE_GRID.left) - 0.5),
		y: y + height * (frameImageRatioY(FRAME_PLAYABLE_GRID.top) - 0.5),
		width: width * frameImageRatioX(FRAME_PLAYABLE_GRID.width),
		height: height * frameImageRatioY(FRAME_PLAYABLE_GRID.height),
	};
>>>>>>> 2fa38b0 (Rebuild Frame1 reel grid coordinates)

	return {
		x,
		y,
		width,
		height,
		grid: {
			...grid,
			centerX: grid.x + grid.width / 2,
			centerY: grid.y + grid.height / 2,
		},
	};
};

const boardLayout = () => {
	const frame = frameLayout();
	const scale = Math.min(frame.grid.width / BOARD_SIZES.width, frame.grid.height / BOARD_SIZES.height);

	return {
		x: frame.grid.centerX,
		y: frame.grid.centerY,
		frameX: frame.x,
		frameY: frame.y,
		anchor: { x: 0.5, y: 0.5 },
		pivot: { x: BOARD_SIZES.width / 2, y: BOARD_SIZES.height / 2 },
		scale,
		frameWidth: frame.width,
		frameHeight: frame.height,
		gridX: frame.grid.x,
		gridY: frame.grid.y,
		gridWidth: frame.grid.width,
		gridHeight: frame.grid.height,
		screenWidth: BOARD_SIZES.width * scale,
		screenHeight: BOARD_SIZES.height * scale,
		...BOARD_SIZES,
	};
};

const boardRaw = () => board.map((reel) => reel.reelState.symbols.map((reelSymbol) => reelSymbol.rawSymbol));

const scatterLandIndex = () => {
	if (stateGame.scatterCounter > 5) return 5;
	if (stateGame.scatterCounter < 1) return 1;
	return stateGame.scatterCounter as 1 | 2 | 3 | 4 | 5;
};

const { enhanceBoard } = createEnhanceBoard();
const enhancedBoard = enhanceBoard({ board: stateGame.board });
export const { getWinLevelDataByWinLevelAlias } = createGetWinLevelDataByWinLevelAlias({ winLevelMap });

export const stateGameDerived = { onSymbolLand, frameLayout, boardLayout, boardRaw, scatterLandIndex, enhancedBoard, getWinLevelDataByWinLevelAlias };