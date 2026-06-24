<script lang="ts">
	import { onMount } from 'svelte';
	import { cubicInOut } from 'svelte/easing';
	import { Tween } from 'svelte/motion';
	import { Container, Rectangle, Sprite, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';

	type Props = {
		oncomplete: () => void;
	};

	const props: Props = $props();
	const context = getContext();
	const opacity = new Tween(0);
	const scale = new Tween(0.86);
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());

	onMount(() => {
		const animate = async () => {
			await Promise.all([
				opacity.set(1, { duration: 380, easing: cubicInOut }),
				scale.set(1, { duration: 520, easing: cubicInOut }),
			]);
			await new Promise((resolve) => setTimeout(resolve, 260));
			await opacity.set(0, { duration: 380, easing: cubicInOut });
			props.oncomplete();
		};
		void animate();
	});
</script>

<Container zIndex={90} alpha={opacity.current}>
	<Rectangle {...canvas} backgroundColor={0x010604} backgroundAlpha={0.92} />
	<Rectangle
		anchor={0.5}
		x={canvas.width * 0.5}
		y={canvas.height * 0.5}
		width={canvas.width * 0.72}
		height={canvas.height * 0.44}
		borderRadius={Math.min(canvas.width, canvas.height) * 0.018}
		backgroundColor={0x062417}
		backgroundAlpha={0.92}
		borderColor={0xd6ad58}
		borderWidth={Math.max(2, canvas.width * 0.002)}
		borderAlpha={0.9}
		scale={scale.current}
	/>
	<Sprite
		key="S"
		anchor={0.5}
		x={canvas.width * 0.5}
		y={canvas.height * 0.47}
		width={Math.min(canvas.width, canvas.height) * 0.2 * scale.current}
		height={Math.min(canvas.width, canvas.height) * 0.2 * scale.current}
	/>
	<Text
		text="THE INHERITANCE"
		anchor={0.5}
		x={canvas.width * 0.5}
		y={canvas.height * 0.65}
		style={{
			fontFamily: 'Georgia',
			fontSize: Math.min(canvas.width * 0.036, canvas.height * 0.055),
			fontWeight: '800',
			fill: 0xffe6a2,
			stroke: { color: 0x190d04, width: 6 },
			letterSpacing: 3,
		}}
	/>
</Container>
