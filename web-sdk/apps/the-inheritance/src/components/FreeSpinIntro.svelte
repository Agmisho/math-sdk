<script lang="ts" module>
	export type EmitterEventFreeSpinIntro =
		| { type: 'freeSpinIntroShow' }
		| { type: 'freeSpinIntroHide' }
		| { type: 'freeSpinIntroUpdate'; totalFreeSpins: number };
</script>

<script lang="ts">
	import { cubicOut } from 'svelte/easing';
	import { Tween } from 'svelte/motion';
	import { CanvasSizeRectangle } from 'components-layout';
	import { FadeContainer } from 'components-pixi';
	import { Container, Rectangle, Sprite, Text } from 'pixi-svelte';
	import { waitForResolve } from 'utils-shared/wait';

	import { getContext } from '../game/context';
	import PressToContinue from './PressToContinue.svelte';

	const context = getContext();
	const panelAlpha = new Tween(0);
	const panelScale = new Tween(0.92);
	const frame = $derived(context.stateGameDerived.frameLayout());
	const panelWidth = $derived(frame.width * 0.68);
	const panelHeight = $derived(frame.height * 0.56);

	let show = $state(false);
	let freeSpinsFromEvent = $state(0);
	let oncomplete = $state(() => {});

	context.eventEmitter.subscribeOnMount({
		freeSpinIntroShow: () => (show = true),
		freeSpinIntroHide: () => (show = false),
		freeSpinIntroUpdate: async (emitterEvent) => {
			freeSpinsFromEvent = emitterEvent.totalFreeSpins;
			panelAlpha.set(0, { duration: 0 });
			panelScale.set(0.92, { duration: 0 });
			await Promise.all([
				panelAlpha.set(1, { duration: 420, easing: cubicOut }),
				panelScale.set(1, { duration: 520, easing: cubicOut }),
			]);
			await waitForResolve((resolve) => (oncomplete = resolve));
		},
	});
</script>

<FadeContainer {show}>
	<CanvasSizeRectangle backgroundColor={0x010604} backgroundAlpha={0.82} />

	<Container
		x={frame.x}
		y={frame.y}
		alpha={panelAlpha.current}
		scale={panelScale.current}
		zIndex={95}
	>
		<Rectangle
			anchor={0.5}
			width={panelWidth}
			height={panelHeight}
			borderRadius={panelWidth * 0.02}
			backgroundColor={0x04170f}
			backgroundAlpha={0.98}
			borderColor={0xd7b45f}
			borderWidth={Math.max(3, panelWidth * 0.006)}
			borderAlpha={0.96}
		/>
		<Rectangle
			anchor={0.5}
			width={panelWidth * 0.94}
			height={panelHeight * 0.88}
			borderRadius={panelWidth * 0.014}
			backgroundColor={0x0b3a25}
			backgroundAlpha={0.34}
			borderColor={0x2d8b59}
			borderWidth={Math.max(2, panelWidth * 0.0025)}
			borderAlpha={0.72}
		/>
		<Text
			text="VAULT UNLOCKED"
			anchor={0.5}
			y={-panelHeight * 0.34}
			style={{
				fontFamily: 'Georgia',
				fontSize: panelWidth * 0.052,
				fontWeight: '800',
				fill: 0xffe6a2,
				stroke: { color: 0x1a0d04, width: 6 },
				letterSpacing: 2,
			}}
		/>
		<Sprite
			key="S"
			anchor={0.5}
			x={-panelWidth * 0.22}
			y={panelHeight * 0.03}
			width={panelHeight * 0.45}
			height={panelHeight * 0.45}
		/>
		<Text
			text={String(freeSpinsFromEvent)}
			anchor={0.5}
			x={panelWidth * 0.12}
			y={-panelHeight * 0.02}
			style={{
				fontFamily: 'Georgia',
				fontSize: panelWidth * 0.16,
				fontWeight: '800',
				fill: 0xffd972,
				stroke: { color: 0x1a0d04, width: 8 },
			}}
		/>
		<Text
			text="FREE SPINS"
			anchor={0.5}
			x={panelWidth * 0.12}
			y={panelHeight * 0.2}
			style={{
				fontFamily: 'Georgia',
				fontSize: panelWidth * 0.052,
				fontWeight: '800',
				fill: 0xffefb1,
				stroke: { color: 0x1a0d04, width: 5 },
				letterSpacing: 2,
			}}
		/>
	</Container>

	<PressToContinue onpress={() => oncomplete()} />
</FadeContainer>
