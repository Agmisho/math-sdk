<script lang="ts" module>
	import type { RawSymbol, Position } from '../game/types';

	export type EmitterEventBoard =
		| { type: 'boardSettle'; board: RawSymbol[][] }
		| { type: 'boardShow' }
		| { type: 'boardHide' }
		| { type: 'boardClearWinLine' }
		| {
				type: 'boardHighlightWinLine';
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
	import { waitForResolve, waitForTimeout } from 'utils-shared/wait';
	import { BoardContext } from 'components-shared';

	import { getContext } from '../game/context';
	import BoardContainer from './BoardContainer.svelte';
	import BoardMask from './BoardMask.svelte';
	import BoardBase from './BoardBase.svelte';
	import WinLineOverlay from './WinLineOverlay.svelte';

	const context = getContext();

	let show = $state(true);
	let activeWinLinePositions = $state<Position[]>([]);
	const winLineProgress = new Tween(0);
	const winLineAlpha = new Tween(0);

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
		winLineProgress.set(0, { duration: 0 });
		winLineAlpha.set(0, { duration: 0 });
	};

	context.eventEmitter.subscribeOnMount({
		stopButtonClick: () => context.stateGameDerived.enhancedBoard.stop(),
		boardSettle: ({ board }) => context.stateGameDerived.enhancedBoard.settle(board),
		boardShow: () => (show = true),
		boardHide: () => (show = false),
		boardClearWinLine: clearWinLine,
		boardHighlightWinLine: async ({ symbolPositions }) => {
			const positions = uniquePositions(symbolPositions);
			if (positions.length < 2) return;

			activeWinLinePositions = positions;
			winLineProgress.set(0, { duration: 0 });
			winLineAlpha.set(1, { duration: 0 });
			await winLineProgress.set(1, { duration: 520, easing: cubicOut });
			await waitForTimeout(520);
			await winLineAlpha.set(0, { duration: 260, easing: sineOut });
			activeWinLinePositions = [];
		},
		boardWithAnimateSymbols: async ({ symbolPositions }) => {
			const getPromises = () =>
				symbolPositions.map(async (position) => {
					const reelSymbol = context.stateGame.board[position.reel].reelState.symbols[position.row];
					reelSymbol.symbolState = 'win';
					await waitForResolve((resolve) => (reelSymbol.oncomplete = resolve));
					reelSymbol.symbolState = 'postWinStatic';
				});

			await Promise.all(getPromises());
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
					progress={winLineProgress.current}
					alpha={winLineAlpha.current}
				/>
			{/if}
		</BoardContainer>
	</BoardContext>
{/if}
