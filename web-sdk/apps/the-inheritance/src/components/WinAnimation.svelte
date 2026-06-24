<script lang="ts">
	import type { Snippet } from 'svelte';
	import { onMount } from 'svelte';
	import { sineInOut } from 'svelte/easing';
	import { Tween } from 'svelte/motion';
	import { Container, Rectangle, Sprite, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';

	type Props = {
		animationMap: {
			intro:
				| 'big_win_intro'
				| 'epic_win_intro'
				| 'max_win_intro'
				| 'mega_win_intro'
				| 'super_win_intro';
			idle: 'big_win_idle' | 'epic_win_idle' | 'max_win_idle' | 'mega_win_idle' | 'super_win_idle';
			outro: 'big_win_exit' | 'epic_win_exit' | 'max_win_exit' | 'mega_win_exit' | 'super_win_exit';
		};
		children: Snippet;
	};

	const props: Props = $props();
	const context = getContext();
	const glow = new Tween(0.35);
	const frame = $derived(context.stateGameDerived.frameLayout());
	const panelWidth = $derived(frame.grid.width * 0.82);
	const panelHeight = $derived(frame.grid.height * 0.72);

	const titleMap = {
		big_win_intro: 'GRAND INHERITANCE',
		super_win_intro: 'ESTATE FORTUNE',
		mega_win_intro: 'VAULT FORTUNE',
		epic_win_intro: 'LEGACY FORTUNE',
		max_win_intro: 'THE INHERITANCE',
	} as const;

	const title = $derived(titleMap[props.animationMap.intro]);

	onMount(() => {
		let cancelled = false;
		const animate = async () => {
			while (!cancelled) {
				await glow.set(0.82, { duration: 850, easing: sineInOut });
				if (cancelled) break;
				await glow.set(0.35, { duration: 850, easing: sineInOut });
			}
		};
		void animate();
		return () => {
			cancelled = true;
		};
	});
</script>

<Container x={frame.x} y={frame.y} zIndex={90}>
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
		width={panelWidth * 0.95}
		height={panelHeight * 0.88}
		borderRadius={panelWidth * 0.012}
		backgroundColor={0x0a3a25}
		backgroundAlpha={0.38 + glow.current * 0.08}
		borderColor={0x3aa66c}
		borderWidth={Math.max(2, panelWidth * 0.0025)}
		borderAlpha={0.52 + glow.current * 0.36}
	/>
	<Rectangle
		anchor={0.5}
		width={panelWidth * 0.72}
		height={panelHeight * 0.015}
		y={-panelHeight * 0.24}
		backgroundColor={0xd8b45d}
		backgroundAlpha={0.45 + glow.current * 0.35}
	/>
	<Sprite
		key="H4"
		anchor={0.5}
		x={-panelWidth * 0.34}
		y={-panelHeight * 0.3}
		width={panelHeight * 0.2}
		height={panelHeight * 0.2}
		rotation={-0.34}
		alpha={0.78 + glow.current * 0.22}
	/>
	<Sprite
		key="S"
		anchor={0.5}
		x={panelWidth * 0.34}
		y={-panelHeight * 0.3}
		width={panelHeight * 0.19}
		height={panelHeight * 0.19}
		alpha={0.78 + glow.current * 0.22}
	/>
	<Text
		text={title}
		anchor={0.5}
		y={-panelHeight * 0.34}
		style={{
			fontFamily: 'Georgia',
			fontSize: Math.min(panelWidth * 0.058, panelHeight * 0.12),
			fontWeight: '800',
			fill: 0xffe6a2,
			stroke: { color: 0x170c04, width: 7 },
			letterSpacing: 2,
		}}
	/>
	<Text
		text="YOU WON"
		anchor={0.5}
		y={-panelHeight * 0.12}
		style={{
			fontFamily: 'Georgia',
			fontSize: panelWidth * 0.032,
			fontWeight: '700',
			fill: 0x8be3ad,
			stroke: { color: 0x06140d, width: 4 },
			letterSpacing: 2,
		}}
	/>
	<Container y={panelHeight * 0.08}>
		{@render props.children()}
	</Container>
	<Text
		text="A FORTUNE REVEALED"
		anchor={0.5}
		y={panelHeight * 0.34}
		style={{
			fontFamily: 'Georgia',
			fontSize: panelWidth * 0.025,
			fontWeight: '700',
			fill: 0xe8cc83,
			stroke: { color: 0x170c04, width: 4 },
			letterSpacing: 2,
		}}
	/>
</Container>
