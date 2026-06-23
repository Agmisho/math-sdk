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
import { stateInheritanceUi } from './stateInheritanceUi.svelte';
import { SYMBOL_ROLE_KEY, SYMBOL_ROLE_VAULT_TRIGGER, SYMBOL_ROLE_WILD, symbolHasRole } from './symbolRoles';
import type { BookEventOfType } from './typesBookEvent';

const FRAME_IMAGE_SIZES = { width: 1358, height: 804 } as const;
const FRAME_RATIO = FRAME_IMAGE_SIZES.width / FRAME_IMAGE_SIZES.height;
const FRAME_PLAYABLE_GRID = { left: 226, top: 44, width: 1079, height: 713 } as const;
const FRAME_GROUP_LEFT_SHIFT = 0.08;
export const LEGACY_KEY_TARGET = 20;
export const BONUS_BUY_FREE_SPINS = 10;
export type SpinMode = 'base' | 'boot' | 'bought' | 'free';

const frameImageRatioX = (value: number) => value / FRAME_IMAGE_SIZES.width;
const frameImageRatioY = (value: number) => value / FRAME_IMAGE_SIZES.height;

const onSymbolLand = ({ rawSymbol }: { rawSymbol: RawSymbol }) => {
	if (symbolHasRole(rawSymbol.name, SYMBOL_ROLE_VAULT_TRIGGER)) {
		eventEmitter.broadcast({ type: 'soundScatterCounterIncrease' });
		eventEmitter.broadcast({ type: 'soundOnce', name: SCATTER_LAND_SOUND_MAP[scatterLandIndex()] });
	}
	if (symbolHasRole(rawSymbol.name, SYMBOL_ROLE_WILD)) eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
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
	spinMode: 'boot' as SpinMode,
	freeSpinsRemaining: 0,
	freeSpinsAwarded: 0,
	freeSpinsTotalWin: 0,
	isBonusBuy: false,
	multiplierBoard: [] as (MultiplierSymbol | undefined)[][],
	scatterCounter: 0,
	keyCounter: 0,
	countedLegacyKeyBoardSignatures: [] as string[],
	legacyFeatureUnlockedShown: false,
	vaultReelResolutions: [] as BookEventOfType<'vaultReelResolved'>[],
});

const frameLayout = () => {
	const canvas = stateLayoutDerived.canvasSizes();
	const isPortrait = canvas.height > canvas.width * 1.05;
	const width = Math.min(
		canvas.width * (isPortrait ? 0.86 : 0.64),
		canvas.height * (isPortrait ? 0.47 : 0.58) * FRAME_RATIO,
	);
	const height = width / FRAME_RATIO;
	const x = canvas.width * 0.5 - width * FRAME_GROUP_LEFT_SHIFT;
	const y = canvas.height * (isPortrait ? 0.13 : 0.08) + height / 2;
	const grid = {
		x: x + width * (frameImageRatioX(FRAME_PLAYABLE_GRID.left) - 0.5),
		y: y + height * (frameImageRatioY(FRAME_PLAYABLE_GRID.top) - 0.5),
		width: width * frameImageRatioX(FRAME_PLAYABLE_GRID.width),
		height: height * frameImageRatioY(FRAME_PLAYABLE_GRID.height),
	};

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

const visibleBoard = (settledBoard: RawSymbol[][]) =>
	settledBoard.map((reel) => reel.slice(0, BOARD_DIMENSIONS.y));

const legacyKeyBoardSignature = (settledBoard: RawSymbol[][]) =>
	visibleBoard(settledBoard)
		.map((reel) => reel.map((rawSymbol) => rawSymbol.name).join(','))
		.join('|');

const countLegacyKeys = (settledBoard: RawSymbol[][]) =>
	settledBoard.reduce(
		(total, reel) =>
			total + reel.slice(0, BOARD_DIMENSIONS.y).filter((rawSymbol) => symbolHasRole(rawSymbol.name, SYMBOL_ROLE_KEY)).length,
		0,
	);

const collectLegacyKeys = ({ board, gameType, betMode }: { board: RawSymbol[][]; gameType: GameType; betMode: string }) => {
	if (gameType !== 'basegame' || betMode.toUpperCase() === 'BONUS') return;

	const boardSignature = legacyKeyBoardSignature(board);
	if (!boardSignature || stateGame.countedLegacyKeyBoardSignatures.includes(boardSignature)) return;

	const keysOnBoard = countLegacyKeys(board);
	if (keysOnBoard <= 0) return;

	stateGame.countedLegacyKeyBoardSignatures.push(boardSignature);

	const previousKeyCounter = stateGame.keyCounter;
	stateGame.keyCounter = Math.min(LEGACY_KEY_TARGET, stateGame.keyCounter + keysOnBoard);

	if (
		previousKeyCounter < LEGACY_KEY_TARGET &&
		stateGame.keyCounter >= LEGACY_KEY_TARGET &&
		!stateGame.legacyFeatureUnlockedShown
	) {
		stateGame.legacyFeatureUnlockedShown = true;
		stateInheritanceUi.modal = 'legacyFeatureUnlocked';
	}
};

const startBonusBuy = () => {
	stateGame.spinMode = 'bought';
	stateGame.freeSpinsAwarded = BONUS_BUY_FREE_SPINS;
	stateGame.freeSpinsRemaining = BONUS_BUY_FREE_SPINS;
	stateGame.freeSpinsTotalWin = 0;
	stateGame.isBonusBuy = true;
};

const startBaseSpin = () => {
	stateGame.spinMode = 'base';
	stateGame.freeSpinsRemaining = 0;
	stateGame.freeSpinsAwarded = 0;
	stateGame.freeSpinsTotalWin = 0;
	stateGame.isBonusBuy = false;
};

const scatterLandIndex = () => {
	if (stateGame.scatterCounter > 5) return 5;
	if (stateGame.scatterCounter < 1) return 1;
	return stateGame.scatterCounter as 1 | 2 | 3 | 4 | 5;
};

const { enhanceBoard } = createEnhanceBoard();
const enhancedBoard = enhanceBoard({ board: stateGame.board });
export const { getWinLevelDataByWinLevelAlias } = createGetWinLevelDataByWinLevelAlias({ winLevelMap });

export const stateGameDerived = { onSymbolLand, frameLayout, boardLayout, boardRaw, scatterLandIndex, enhancedBoard, collectLegacyKeys, startBonusBuy, startBaseSpin, getWinLevelDataByWinLevelAlias };
