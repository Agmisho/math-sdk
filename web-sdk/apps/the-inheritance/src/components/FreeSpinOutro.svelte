<script lang="ts" module>
	import type { WinLevelData } from '../game/winLevelMap';

	export type EmitterEventFreeSpinOutro =
		| { type: 'freeSpinOutroShow' }
		| { type: 'freeSpinOutroHide' }
		| { type: 'freeSpinOutroCountUp'; amount: number; winLevelData: WinLevelData };
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { sineInOut } from 'svelte/easing';
	import { Tween } from 'svelte/motion';
	import { Container, Rectangle, Sprite, Text } from 'pixi-svelte';
	import { FadeContainer, ResponsiveText, WinCountUpProvider } from 'components-pixi';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';
	import { waitForResolve } from 'utils-shared/wait';
	import { CanvasSizeRectangle } from 'components-layout';
	import { OnMount } from 'components-shared';

	import { getContext } from '../game/context';
	import PressToContinue from './PressToContinue.svelte';

	const context = getContext();
	const glow = new Tween(0.32);
	const frame = $derived(context.stateGameDerived.frameLayout());
	const panelWidth = $derived(frame.grid.width * 0.78);
	const panelHeight = $derived(frame.grid.height * 0.7);

	let show = $state(false);
	let amount = $state(0);
	let winLevelData = $state<WinLevelData>();
	let oncomplete = $state(() => {});

	onMount(() => {
		let cancelled = false;
		const animate = async () => {
			while (!cancelled) {
				await glow.set(0.8, { duration: 900, easing: sineInOut });
				if (cancelled) break;
				await glow.set(0.32, { duration: 900, easing: sineInOut });
			}
		};
		void animate();
		return () => {
			cancelled = true;
		};
	});

	context.eventEmitter.subscribeOnMount({
		freeSpinOutroShow: () => (show = true),
		freeSpinOutroHide: async () => (show = false),
		freeSpinOutroCountUp: async (emitterEvent) => {
			amount = emitterEvent.amount;
			winLevelData = emitterEvent.winLevelData;
			await waitForResolve((resolve) => (oncomplete = resolve));
		},
	});
</script>

<FadeContainer {show}>
	{#if winLevelData}
		{@const duration = winLevelData.presentDuration}
		<WinCountUpProvider {amount} {duration}>
			{#snippet children({ countUpAmount, startCountUp, finishCountUp, countUpCompleted })}
				<OnMount onmount={() => startCountUp()} />
				<CanvasSizeRectangle backgroundColor={0x010604} backgroundAlpha={0.82} />

				<Container x={frame.x} y={frame.y} zIndex={95}>
					<Rectangle
						anchor={0.5}
						width={panelWidth}
						height={panelHeight}
						borderRadius={panelWidth * 0.018}
						backgroundColor={0x03140d}
						backgroundAlpha={0.98}
						borderColor={0xd8b45d}
						borderWidth={Math.max(3, panelWidth * 0.006)}
						borderAlpha={0.96}
					/>
					<Rectangle
						anchor={0.5}
						width={panelWidth * 0.94}
						height={panelHeight * 0.88}
						borderRadius={panelWidth * 0.012}
						backgroundColor={0x0a3a25}
						backgroundAlpha={0.36 + glow.current * 0.08}
						borderColor={0x3aa66c}
						borderWidth={Math.max(2, panelWidth * 0.0025)}
						borderAlpha={0.5 + glow.current * 0.38}
					/>
					<Sprite
						key="S"
						anchor={0.5}
						x={-panelWidth * 0.31}
						y={-panelHeight * 0.23}
						width={panelHeight * 0.26}
						height={panelHeight * 0.26}
						alpha={0.82 + glow.current * 0.18}
					/>
					<Sprite
						key="H4"
						anchor={0.5}
						x={panelWidth * 0.31}
						y={-panelHeight * 0.23}
						width={panelHeight * 0.25}
						height={panelHeight * 0.25}
						rotation={0.32}
						alpha={0.82 + glow.current * 0.18}
					/>
					<Text
						text="VAULT FORTUNE REVEALED"
						anchor={0.5}
						y={-panelHeight * 0.34}
						style={{
							fontFamily: 'Georgia',
							fontSize: Math.min(panelWidth * 0.052, panelHeight * 0.11),
							fontWeight: '800',
							fill: 0xffe6a2,
							stroke: { color: 0x170c04, width: 7 },
							letterSpacing: 2,
						}}
					/>
					<Text
						text="FREE SPINS COMPLETE"
						anchor={0.5}
						y={-panelHeight * 0.12}
						style={{
							fontFamily: 'Georgia',
							fontSize: panelWidth * 0.031,
							fontWeight: '700',
							fill: 0x8be3ad,
							stroke: { color: 0x06140d, width: 4 },
							letterSpacing: 2,
						}}
					/>
					<ResponsiveText
						anchor={0.5}
						y={panelHeight * 0.1}
						style={{
							fontFamily: 'Georgia',
							fontSize: panelWidth * 0.09,
							fontWeight: '800',
							fill: 0xffd978,
							stroke: { color: 0x170c04, width: 7 },
						}}
						text={bookEventAmountToCurrencyString(countUpAmount)}
						maxWidth={panelWidth * 0.72}
					/>
					<Text
						text="TOTAL FEATURE WIN"
						anchor={0.5}
						y={panelHeight * 0.31}
						style={{
							fontFamily: 'Georgia',
							fontSize: panelWidth * 0.027,
							fontWeight: '700',
							fill: 0xe8cc83,
							stroke: { color: 0x170c04, width: 4 },
							letterSpacing: 2,
						}}
					/>
				</Container>

				<PressToContinue
					labelYRatio={0.7}
					onpress={() => (countUpCompleted ? oncomplete() : finishCountUp())}
				/>
			{/snippet}
		</WinCountUpProvider>
	{/if}
</FadeContainer>
