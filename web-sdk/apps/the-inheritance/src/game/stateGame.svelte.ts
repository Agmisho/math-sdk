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

const FRAME_RATIO = 1358 / 804;
const GRID_WIDTH = 0.784;
const GRID_HEIGHT = 0.709;
const GRID_CENTER_X = 0.559;
const GRID_CENTER_Y = 0.496;

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

const boardLayout = () => {
	const canvas = stateLayoutDerived.canvasSizes();
	const isPortrait = canvas.height > canvas.width * 1.05;
	const frameWidth = Math.min(canvas.width * (isPortrait ? 0.86 : 0.64), canvas.height * (isPortrait ? 0.47 : 0.58) * FRAME_RATIO);
	const frameHeight = frameWidth / FRAME_RATIO;
	const frameX = canvas.width * 0.5;
	const frameY = canvas.height * (isPortrait ? 0.13 : 0.08) + frameHeight / 2;
	const scale = Math.min((frameWidth * GRID_WIDTH) / BOARD_SIZES.width, (frameHeight * GRID_HEIGHT) / BOARD_SIZES.height);

	return {
		x: frameX + frameWidth * (GRID_CENTER_X - 0.5),
		y: frameY + frameHeight * (GRID_CENTER_Y - 0.5),
		frameX,
		frameY,
		anchor: { x: 0.5, y: 0.5 },
		pivot: { x: BOARD_SIZES.width / 2, y: BOARD_SIZES.height / 2 },
		scale,
		frameWidth,
		frameHeight,
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

export const stateGameDerived = { onSymbolLand, boardLayout, boardRaw, scatterLandIndex, enhancedBoard, getWinLevelDataByWinLevelAlias };