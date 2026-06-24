<script lang="ts" module>
	import type { WinLevelData } from '../game/winLevelMap';

	export type EmitterEventWin =
		| { type: 'winShow' }
		| { type: 'winClear' }
		| { type: 'winHide' }
		| { type: 'winUpdate'; amount: number; winLevelData: WinLevelData };
</script>

<script lang="ts">
	import { Container, Text } from 'pixi-svelte';
	import { FadeContainer, WinCountUpProvider } from 'components-pixi';
	import { waitForResolve, waitForTimeout } from 'utils-shared/wait';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';
	import { CanvasSizeRectangle } from 'components-layout';
	import { OnMount } from 'components-shared';

	import WinCoins from './WinCoins.svelte';
	import WinAnimation from './WinAnimation.svelte';
	import PressToContinue from './PressToContinue.svelte';
	import { getContext } from '../game/context';

	const context = getContext();
	const WIN_HORIZONTAL_OFFSET_RATIO = 0.014;

	let show = $state(false);
	let amount = $state(0);
	let winLevelData = $state<WinLevelData>();
	let countUpFinished = $state(false);
	let oncomplete = $state(() => {});
	let onCountUpComplete = $state(() => {});

	const winTextLayout = $derived.by(() => {
		const boardLayout = context.stateGameDerived.boardLayout();
		const panel = context.stateGameDerived.uiPanelLayout();
		const panelHeight = panel.height;
		const panelX = panel.x;
		const panelY = panel.y;
		const frameBottom = boardLayout.frameY + boardLayout.frameHeight / 2;
		const uiTop = panelY - panelHeight / 2;
		const availableGap = Math.max(uiTop - frameBottom, panelHeight * 0.12);

		return {
			x: (boardLayout.frameX + panelX) / 2 + boardLayout.frameWidth * WIN_HORIZONTAL_OFFSET_RATIO,
			y: frameBottom + availableGap * 0.88,
			gap: availableGap,
		};
	});

	const winTextStyle = $derived({
		fontFamily: 'Georgia',
		fontSize: Math.max(
			winLevelData?.type === 'big' ? 34 : 24,
			Math.min(winTextLayout.gap * (winLevelData?.type === 'big' ? 0.62 : 0.48), winLevelData?.type === 'big' ? 58 : 40),
		),
		fontWeight: '900',
		fill: 0xffe6a2,
		align: 'center',
	});

	context.eventEmitter.subscribeOnMount({
		winShow: () => (show = true),
		winHide: () => (countUpFinished = true),
		winClear: () => {
			show = false;
			amount = 0;
			winLevelData = undefined;
			countUpFinished = false;
			oncomplete = () => {};
		},
		winUpdate: async (emitterEvent) => {
			amount = emitterEvent.amount;
			winLevelData = emitterEvent.winLevelData;
			countUpFinished = false;
			const presentationComplete = waitForResolve((resolve) => (oncomplete = resolve));
			const fallbackMs = Math.max(emitterEvent.winLevelData.presentDuration + 1000, 2500);
			await Promise.race([presentationComplete, waitForTimeout(fallbackMs)]);
			oncomplete = () => {};
			countUpFinished = true;
		},
	});
</script>

<FadeContainer {show}>
	{#if winLevelData}
		{@const isBigWin = winLevelData.type === 'big'}
		{@const duration = winLevelData.presentDuration}
		<WinCountUpProvider {amount} {duration} oncomplete={() => onCountUpComplete()}>
			{#snippet children({ countUpAmount, startCountUp, finishCountUp, countUpCompleted })}
				{#if isBigWin && !countUpFinished}
					<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.5} />
				{/if}

				<OnMount
					onmount={async () => {
						await startCountUp();
						await waitForTimeout(300);
						countUpFinished = true;
						oncomplete();
					}}
				/>

				<Container
					x={winTextLayout.x}
					y={winTextLayout.y}
				>
					{#if winLevelData?.animation && !countUpFinished}
						<WinAnimation animationMap={winLevelData.animation}>
							<Text
								anchor={0.5}
								text={bookEventAmountToCurrencyString(countUpAmount)}
								style={winTextStyle}
							/>
						</WinAnimation>
					{:else}
						<Text
							anchor={0.5}
							text={bookEventAmountToCurrencyString(countUpAmount)}
							style={winTextStyle}
						/>
					{/if}
				</Container>

				{#if !countUpFinished}
					<WinCoins emit={!countUpCompleted} levelAlias={winLevelData?.alias} />
					<PressToContinue onpress={() => (countUpCompleted ? oncomplete() : finishCountUp())} />
				{/if}
			{/snippet}
		</WinCountUpProvider>
	{/if}
</FadeContainer>
