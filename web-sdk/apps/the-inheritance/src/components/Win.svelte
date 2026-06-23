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
	const UI_RATIO = 1672 / 941;
	const UI_VERTICAL_OFFSET = 0.48;
	const UI_SCALE = 0.9;
	const UI_HORIZONTAL_OFFSET = 0.012;

	let show = $state(false);
	let amount = $state(0);
	let winLevelData = $state<WinLevelData>();
	let countUpFinished = $state(false);
	let oncomplete = $state(() => {});
	let onCountUpComplete = $state(() => {});

	const winTextLayout = $derived.by(() => {
		const canvas = context.stateLayoutDerived.canvasSizes();
		const boardLayout = context.stateGameDerived.boardLayout();
		const isPortrait = canvas.height > canvas.width * 1.05;
		const basePanelWidth = Math.min(canvas.width * (isPortrait ? 0.90 : 0.68), canvas.height * 0.40 * UI_RATIO);
		const basePanelHeight = basePanelWidth / UI_RATIO;
		const panelWidth = basePanelWidth * UI_SCALE;
		const panelHeight = panelWidth / UI_RATIO;
		const panelX = canvas.width / 2 + basePanelWidth * UI_HORIZONTAL_OFFSET;
		const panelY = boardLayout.y + boardLayout.frameHeight / 2 + basePanelHeight * UI_VERTICAL_OFFSET;
		const frameBottom = boardLayout.frameY + boardLayout.frameHeight / 2;
		const uiTop = panelY - panelHeight / 2;
		const availableGap = Math.max(uiTop - frameBottom, panelHeight * 0.12);

		return {
			x: (boardLayout.frameX + panelX) / 2,
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
