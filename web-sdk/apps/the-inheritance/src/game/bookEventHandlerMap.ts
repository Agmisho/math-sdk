import _ from 'lodash';

import { recordBookEvent, checkIsMultipleRevealEvents, type BookEventHandlerMap } from 'utils-book';
import { stateBet, stateUi } from 'state-shared';
import { sequence } from 'utils-shared/sequence';

import { eventEmitter } from './eventEmitter';
import { playBookEvent } from './utils';
import { winLevelMap, type WinLevel, type WinLevelData } from './winLevelMap';
import { LEGACY_KEY_TARGET, stateGame, stateGameDerived } from './stateGame.svelte';
import { stateInheritanceUi } from './stateInheritanceUi.svelte';
import type { BookEvent, BookEventOfType, BookEventContext } from './typesBookEvent';
import type { Position, RawSymbol } from './types';
import config from './config';

const winLevelSoundsPlay = ({ winLevelData }: { winLevelData: WinLevelData }) => {
	if (winLevelData?.alias === 'max') eventEmitter.broadcastAsync({ type: 'uiHide' });
	if (winLevelData?.sound?.sfx) {
		eventEmitter.broadcast({ type: 'soundOnce', name: winLevelData.sound.sfx });
	}
	if (winLevelData?.sound?.bgm) {
		eventEmitter.broadcast({ type: 'soundMusic', name: winLevelData.sound.bgm });
	}
	if (winLevelData?.type === 'big') {
		eventEmitter.broadcast({ type: 'soundLoop', name: 'sfx_bigwin_coinloop' });
	}
};

const winLevelSoundsStop = () => {
	eventEmitter.broadcast({ type: 'soundStop', name: 'sfx_bigwin_coinloop' });
	if (stateBet.activeBetModeKey === 'SUPERSPIN' || stateGame.gameType === 'freegame') {
		// check if SUPERSPIN, when finishing a bet.
		eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_freespin' });
	} else {
		eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_main' });
	}
	eventEmitter.broadcastAsync({ type: 'uiShow' });
};

const animateSymbols = async ({ positions }: { positions: Position[] }) => {
	eventEmitter.broadcast({ type: 'boardShow' });
	await eventEmitter.broadcastAsync({
		type: 'boardWithAnimateSymbols',
		symbolPositions: positions,
	});
};

const uniquePositions = (positions: Position[]) => {
	const seen = new Set<string>();
	return positions.filter((position) => {
		const key = `${position.reel}:${position.row}`;
		if (seen.has(key)) return false;
		seen.add(key);
		return true;
	});
};

const getPaylineDisplayPositions = (lineIndex: number): Position[] => {
	const payline = config.paylines[String(lineIndex) as keyof typeof config.paylines];
	if (!payline) return [];
	return payline.map((row, reel) => ({ reel, row: row + 1 }));
};

const settleVaultReelBoard = (bookEvent: BookEventOfType<'vaultReelResolved'>) => {
	const board = stateGameDerived.boardRaw().map((reel) => reel.map((symbol) => ({ ...symbol }))) as RawSymbol[][];
	const wildSymbol = { name: bookEvent.wildSymbolId, wild: true } as RawSymbol;

	for (const position of bookEvent.transformedDisplayPositions) {
		if (!board[position.reel]?.[position.row]) continue;
		board[position.reel][position.row] = { ...wildSymbol };
	}

	eventEmitter.broadcast({ type: 'boardSettle', board });
};

const normalizeLegacyKeyTarget = (target: number) =>
	Number.isFinite(target) && target > 0 ? Math.floor(target) : LEGACY_KEY_TARGET;
const normalizeLegacyKeyCount = (collected: number, target: number) => Math.max(0, Math.min(target, collected));

export const bookEventHandlerMap: BookEventHandlerMap<BookEvent, BookEventContext> = {
	reveal: async (bookEvent: BookEventOfType<'reveal'>, { bookEvents }: BookEventContext) => {
		eventEmitter.broadcast({ type: 'globalMultiplierUpdate', multiplier: 1 });
		eventEmitter.broadcast({ type: 'globalMultiplierHide' });
		const isBonusGame = checkIsMultipleRevealEvents({ bookEvents });
		if (isBonusGame) {
			eventEmitter.broadcast({ type: 'stopButtonEnable' });
			recordBookEvent({ bookEvent });
		}

		stateGame.gameType = bookEvent.gameType;
		if (bookEvent.gameType === 'freegame') {
			stateGame.spinMode = 'free';
		} else if (!stateGame.isBonusBuy) {
			stateGame.spinMode = 'base';
		}
		await stateGameDerived.enhancedBoard.spin({
			revealEvent: bookEvent,
			paddingBoard: config.paddingReels[bookEvent.gameType],
		});
		if (bookEvent.gameType === 'freegame') {
			stateGame.freeSpinsRemaining = Math.max(stateGame.freeSpinsRemaining - 1, 0);
		}
		eventEmitter.broadcast({ type: 'soundScatterCounterClear' });
	},
	winInfo: async (bookEvent: BookEventOfType<'winInfo'>) => {
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_winlevel_small' });
		await sequence(bookEvent.wins, async (win) => {
			await Promise.all([
				eventEmitter.broadcastAsync({
					type: 'boardHighlightWinLine',
					linePositions: getPaylineDisplayPositions(win.meta.lineIndex),
					symbolPositions: win.positions,
				}),
				animateSymbols({ positions: win.positions }),
			]);
		});
	},
	setTotalWin: async (bookEvent: BookEventOfType<'setTotalWin'>) => {
		stateBet.winBookEventAmount = bookEvent.amount;
		if (stateGame.spinMode === 'free') stateGame.freeSpinsTotalWin = bookEvent.amount;
	},
	freeSpinTrigger: async (bookEvent: BookEventOfType<'freeSpinTrigger'>) => {
		const totalFreeSpins = stateGame.isBonusBuy ? stateGame.freeSpinsAwarded || bookEvent.totalFs : bookEvent.totalFs;
		stateGame.freeSpinsAwarded = totalFreeSpins;
		stateGame.freeSpinsRemaining = totalFreeSpins;
		stateGame.freeSpinsTotalWin = 0;

		// animate scatters
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_scatter_win_v2' });
		await animateSymbols({ positions: bookEvent.positions });
		// show free spin intro
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_superfreespin' });
		await eventEmitter.broadcastAsync({ type: 'uiHide' });
		await eventEmitter.broadcastAsync({ type: 'transition' });
		eventEmitter.broadcast({ type: 'freeSpinIntroShow' });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'jng_intro_fs' });
		eventEmitter.broadcast({ type: 'soundMusic', name: 'bgm_freespin' });
		await eventEmitter.broadcastAsync({
			type: 'freeSpinIntroUpdate',
			totalFreeSpins,
		});
		stateGame.gameType = 'freegame';
		stateGame.spinMode = 'free';
		eventEmitter.broadcast({ type: 'freeSpinIntroHide' });
		eventEmitter.broadcast({ type: 'boardFrameGlowShow' });
		eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
		stateUi.freeSpinCounterShow = true;
		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: undefined,
			total: totalFreeSpins,
		});
		stateUi.freeSpinCounterTotal = totalFreeSpins;
		await eventEmitter.broadcastAsync({ type: 'uiShow' });
		await eventEmitter.broadcastAsync({ type: 'drawerButtonShow' });
		eventEmitter.broadcast({ type: 'drawerFold' });
	},
	freeSpinRetrigger: async (bookEvent: BookEventOfType<'freeSpinRetrigger'>) => {
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_scatter_win_v2' });
		await animateSymbols({ positions: bookEvent.positions });
		stateGame.freeSpinsAwarded = bookEvent.totalFs;
		stateGame.freeSpinsRemaining = Math.max(bookEvent.totalFs - (stateUi.freeSpinCounterCurrent || 0), 0);
		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: stateUi.freeSpinCounterCurrent,
			total: bookEvent.totalFs,
		});
		stateUi.freeSpinCounterTotal = bookEvent.totalFs;
	},
	updateFreeSpin: async (bookEvent: BookEventOfType<'updateFreeSpin'>) => {
		stateGame.spinMode = 'free';
		stateGame.freeSpinsAwarded = bookEvent.total;
		stateGame.freeSpinsRemaining = Math.max(bookEvent.total - bookEvent.amount, 0);
		eventEmitter.broadcast({ type: 'freeSpinCounterShow' });
		stateUi.freeSpinCounterShow = true;
		eventEmitter.broadcast({
			type: 'freeSpinCounterUpdate',
			current: bookEvent.amount + 1,
			total: bookEvent.total,
		});
		stateUi.freeSpinCounterCurrent = bookEvent.amount + 1;
		stateUi.freeSpinCounterTotal = bookEvent.total;
	},
	freeSpinEnd: async (bookEvent: BookEventOfType<'freeSpinEnd'>) => {
		const winLevelData = winLevelMap[bookEvent.winLevel as WinLevel];
		const wasBonusBuy = stateGame.isBonusBuy;

		stateGame.freeSpinsRemaining = 0;
		stateGame.freeSpinsTotalWin = bookEvent.amount;

		await eventEmitter.broadcastAsync({ type: 'uiHide' });
		stateGame.gameType = 'basegame';
		eventEmitter.broadcast({ type: 'boardFrameGlowHide' });
		eventEmitter.broadcast({ type: 'freeSpinOutroShow' });
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_youwon_panel' });
		winLevelSoundsPlay({ winLevelData });
		await eventEmitter.broadcastAsync({
			type: 'freeSpinOutroCountUp',
			amount: bookEvent.amount,
			winLevelData,
		});
		winLevelSoundsStop();
		eventEmitter.broadcast({ type: 'freeSpinOutroHide' });
		eventEmitter.broadcast({ type: 'freeSpinCounterHide' });
		stateUi.freeSpinCounterShow = false;
		await eventEmitter.broadcastAsync({ type: 'transition' });
		await eventEmitter.broadcastAsync({ type: 'uiShow' });
		await eventEmitter.broadcastAsync({ type: 'drawerUnfold' });
		eventEmitter.broadcast({ type: 'drawerButtonHide' });
		stateGame.spinMode = 'base';
		stateGame.isBonusBuy = false;
		if (wasBonusBuy) stateBet.activeBetModeKey = 'BASE';
	},
	setWin: async (bookEvent: BookEventOfType<'setWin'>) => {
		const winLevelData = winLevelMap[bookEvent.winLevel as WinLevel];

		eventEmitter.broadcast({ type: 'winShow' });
		winLevelSoundsPlay({ winLevelData });
		await eventEmitter.broadcastAsync({
			type: 'winUpdate',
			amount: bookEvent.amount,
			winLevelData,
		});
		winLevelSoundsStop();
	},
	finalWin: async () => {
		// Do nothing
	},
	collectionUpdate: async (bookEvent: BookEventOfType<'collectionUpdate'>, { bookEvents }: BookEventContext) => {
		const target = normalizeLegacyKeyTarget(bookEvent.target);
		const previousCount = stateGame.keyCounter;
		const nextCount = normalizeLegacyKeyCount(bookEvent.collected, target);
		const legacyCreditUsed = bookEvents.some(
			(event) => event.type === 'legacyScatterCredit' && event.used,
		);

		stateGame.keyTarget = target;
		stateGame.keyCounter = nextCount;
		eventEmitter.broadcast({
			type: 'collectionUpdate',
			collected: nextCount,
			target,
			positions: bookEvent.positions,
			gameType: bookEvent.gameType,
		});

		if (!legacyCreditUsed && previousCount < target && nextCount >= target) {
			stateInheritanceUi.modal = 'legacyFeatureUnlocked';
		}
	},
	legacyScatterCredit: async (bookEvent: BookEventOfType<'legacyScatterCredit'>) => {
		stateGame.keyTarget = normalizeLegacyKeyTarget(bookEvent.target);
		eventEmitter.broadcast({
			type: 'legacyScatterCredit',
			used: bookEvent.used,
			collected: normalizeLegacyKeyCount(bookEvent.collected, stateGame.keyTarget),
			target: stateGame.keyTarget,
		});
	},
	multiplierUpdate: async (bookEvent: BookEventOfType<'multiplierUpdate'>) => {
		const multiplier = Math.max(1, bookEvent.appliedMultiplier || bookEvent.multiplier || 1);
		if (multiplier > 1) {
			eventEmitter.broadcast({ type: 'globalMultiplierShow' });
			eventEmitter.broadcast({ type: 'globalMultiplierUpdate', multiplier });
		} else {
			eventEmitter.broadcast({ type: 'globalMultiplierHide' });
		}
	},
	vaultReelResolved: async (bookEvent: BookEventOfType<'vaultReelResolved'>) => {
		stateGame.vaultReelResolutions.push(bookEvent);
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_multiplier_landing' });
		settleVaultReelBoard(bookEvent);
		await animateSymbols({
			positions: uniquePositions([
				bookEvent.sourceKeyDisplayPosition,
				...bookEvent.transformedDisplayPositions,
				...bookEvent.affectedPaylines.flatMap((line) => line.displayPositions),
			]),
		});
	},
	// customised
	createBonusSnapshot: async (bookEvent: BookEventOfType<'createBonusSnapshot'>) => {
		const { bookEvents } = bookEvent;

		function findLastBookEvent<T>(type: T) {
			return _.findLast(bookEvents, (bookEvent) => bookEvent.type === type) as
				| BookEventOfType<T>
				| undefined;
		}

		const lastFreeSpinTriggerEvent = findLastBookEvent('freeSpinTrigger' as const);
		const lastUpdateFreeSpinEvent = findLastBookEvent('updateFreeSpin' as const);
		const lastSetTotalWinEvent = findLastBookEvent('setTotalWin' as const);
		const lastUpdateGlobalMultEvent = findLastBookEvent('updateGlobalMult' as const);

		if (lastFreeSpinTriggerEvent) await playBookEvent(lastFreeSpinTriggerEvent, { bookEvents });
		if (lastUpdateFreeSpinEvent) playBookEvent(lastUpdateFreeSpinEvent, { bookEvents });
		if (lastSetTotalWinEvent) playBookEvent(lastSetTotalWinEvent, { bookEvents });
		if (lastUpdateGlobalMultEvent) playBookEvent(lastUpdateGlobalMultEvent, { bookEvents });
	},
};
