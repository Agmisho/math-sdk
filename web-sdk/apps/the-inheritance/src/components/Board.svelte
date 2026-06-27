<script lang="ts" module>
	import type { RawSymbol, Position } from '../game/types';

	export type EmitterEventBoard =
		| { type: 'boardSettle'; board: RawSymbol[][] }
		| { type: 'boardShow' }
		| { type: 'boardHide' }
		| { type: 'boardClearWinLine' }
		| {
				type: 'boardHighlightWinLine';
				linePositions: Position[];
				symbolPositions: Position[];
		  }
		| {
				type: 'boardWithAnimateSymbols';
				symbolPositions: Position[];
		  };
</script>

<script lang="ts">
	import { cubicOut, sineOut } from 'svelte/easing';
	import { Tween } from 'svelte/motion';
	import { waitForTimeout } from 'utils-shared/wait';
	import { BoardContext } from 'components-shared';
	import { Rectangle } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import BoardContainer from './BoardContainer.svelte';
	import BoardMask from './BoardMask.svelte';
	import BoardBase from './BoardBase.svelte';
	import WinLineOverlay from './WinLineOverlay.svelte';

	const context = getContext();

	let show = $state(true);
	let activeWinLinePositions = $state<Position[]>([]);
	let activeWinningPositions = $state<Position[]>([]);
	const winLineProgress = new Tween(0);
	const winLineAlpha = new Tween(0);
	const WIN_SYMBOL_PRESENTATION_MS = 780;
	const boardLayout = $derived(context.stateGameDerived.boardLayout());

	const canStopByBoardClick = $derived(!context.stateXstateDerived.isIdle());

	const completeSpin = () => {
		if (!canStopByBoardClick) return;
		context.stateGameDerived.enhancedBoard.stop();
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

	const clearWinLine = () => {
		activeWinLinePositions = [];
		activeWinningPositions = [];
		winLineProgress.set(0, { duration: 0 });
		winLineAlpha.set(0, { duration: 0 });
	};

	context.eventEmitter.subscribeOnMount({
		stopButtonClick: () => context.stateGameDerived.enhancedBoard.stop(),
		boardSettle: ({ board }) => context.stateGameDerived.enhancedBoard.settle(board),
		boardShow: () => (show = true),
		boardHide: () => (show = false),
		boardClearWinLine: clearWinLine,
		boardHighlightWinLine: async ({ linePositions, symbolPositions }) => {
			const positions = uniquePositions(linePositions);
			if (positions.length < 2) return;

			activeWinLinePositions = positions;
			activeWinningPositions = uniquePositions(symbolPositions);
			winLineProgress.set(0, { duration: 0 });
			winLineAlpha.set(1, { duration: 0 });
			await winLineProgress.set(1, { duration: 520, easing: cubicOut });
			await waitForTimeout(520);
			await winLineAlpha.set(0, { duration: 260, easing: sineOut });
			activeWinLinePositions = [];
			activeWinningPositions = [];
		},
		boardWithAnimateSymbols: async ({ symbolPositions }) => {
			const winningSymbols = uniquePositions(symbolPositions).flatMap((position) => {
				const reelSymbol =
					context.stateGame.board[position.reel]?.reelState.symbols[position.row];
				return reelSymbol ? [reelSymbol] : [];
			});

			winningSymbols.forEach((reelSymbol) => (reelSymbol.symbolState = 'win'));
			await waitForTimeout(WIN_SYMBOL_PRESENTATION_MS);
			winningSymbols.forEach((reelSymbol) => {
				if (reelSymbol.symbolState === 'win') reelSymbol.symbolState = 'postWinStatic';
			});
		},
	});

	context.stateGameDerived.enhancedBoard.readyToSpinEffect();
</script>

{#if show}
	<BoardContext animate={false}>
		<BoardContainer>
			<BoardMask />
			<BoardBase />
		</BoardContainer>
	</BoardContext>

	<BoardContext animate={true}>
		<BoardContainer>
			<BoardBase />
			{#if activeWinLinePositions.length > 1}
				<WinLineOverlay
					positions={activeWinLinePositions}
					winningPositions={activeWinningPositions}
					progress={winLineProgress.current}
					alpha={winLineAlpha.current}
				/>
			{/if}
			{#if canStopByBoardClick}
				<Rectangle
					x={boardLayout.width / 2}
					y={boardLayout.height / 2}
					anchor={0.5}
					width={boardLayout.width}
					height={boardLayout.height}
					backgroundColor={0x000000}
					backgroundAlpha={0.001}
					eventMode="static"
					cursor="pointer"
					onpointerdown={completeSpin}
					zIndex={80}
				/>
			{/if}
		</BoardContainer>
	</BoardContext>
{/if}
