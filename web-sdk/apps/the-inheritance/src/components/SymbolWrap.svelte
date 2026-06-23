<script lang="ts">
	import type { Snippet } from 'svelte';

	import { cubicOut, sineInOut } from 'svelte/easing';
	import { Tween } from 'svelte/motion';
	import { Container, Graphics } from 'pixi-svelte';
	import { getContextBoard } from 'components-shared';

	import { SYMBOL_SIZE, BOARD_DIMENSIONS } from '../game/constants';

	type Props = {
		debug?: boolean;
		x: number;
		y: number;
		animating: boolean;
		winning?: boolean;
		children: Snippet;
	};

	const props: Props = $props();
	const boardContext = getContextBoard();
	const popScale = new Tween(1);
	const glowAlpha = new Tween(0);
	const liftY = new Tween(0);
	let wasWinning = false;
	let animationGeneration = 0;
	const show = $derived(
		(boardContext.animate && props.animating) || (!boardContext.animate && !props.animating),
	);
	const top = 0;
	const bottom = SYMBOL_SIZE * BOARD_DIMENSIONS.y;
	const inFrame = $derived(props.y >= top && props.y <= bottom);

	const drawGlow = (graphics: any) => {
		const alpha = glowAlpha.current;
		if (!props.winning || alpha <= 0) return;

		graphics.circle(0, 0, SYMBOL_SIZE * 0.45);
		graphics.fill({ color: 0x032014, alpha: alpha * 0.5 });
		graphics.stroke({ width: 7, color: 0x17643e, alpha: alpha * 0.86 });
		graphics.circle(0, 0, SYMBOL_SIZE * 0.34);
		graphics.stroke({ width: 2, color: 0xffe6a2, alpha: alpha * 0.62 });
		graphics.ellipse(0, SYMBOL_SIZE * 0.32, SYMBOL_SIZE * 0.34, SYMBOL_SIZE * 0.1);
		graphics.fill({ color: 0x00160d, alpha: alpha * 0.42 });
	};

	const playWinningEffect = async (generation: number) => {
		await Promise.all([
			popScale.set(1.12, { duration: 140, easing: cubicOut }),
			glowAlpha.set(0.88, { duration: 140, easing: cubicOut }),
			liftY.set(-SYMBOL_SIZE * 0.055, { duration: 140, easing: cubicOut }),
		]);
		if (generation !== animationGeneration) return;

		await Promise.all([
			popScale.set(1.045, { duration: 180, easing: sineInOut }),
			glowAlpha.set(0.34, { duration: 180, easing: sineInOut }),
			liftY.set(-SYMBOL_SIZE * 0.035, { duration: 180, easing: sineInOut }),
		]);
		if (generation !== animationGeneration) return;

		await Promise.all([
			popScale.set(1.075, { duration: 180, easing: sineInOut }),
			glowAlpha.set(0.7, { duration: 180, easing: sineInOut }),
			liftY.set(-SYMBOL_SIZE * 0.045, { duration: 180, easing: sineInOut }),
		]);
		if (generation !== animationGeneration) return;

		await Promise.all([
			popScale.set(1.035, { duration: 180, easing: sineInOut }),
			glowAlpha.set(0.24, { duration: 180, easing: sineInOut }),
			liftY.set(-SYMBOL_SIZE * 0.025, { duration: 180, easing: sineInOut }),
		]);
	};

	$effect(() => {
		const winning = Boolean(props.winning);
		if (winning === wasWinning) return;
		wasWinning = winning;
		animationGeneration += 1;
		const generation = animationGeneration;

		if (winning) {
			void playWinningEffect(generation);
			return;
		}

		void popScale.set(1, { duration: 160, easing: sineInOut });
		void glowAlpha.set(0, { duration: 160, easing: sineInOut });
		void liftY.set(0, { duration: 160, easing: sineInOut });
	});
</script>

{#if props.debug || (show && inFrame)}
	<Container x={props.x} y={props.y + liftY.current} scale={popScale.current}>
		{#if props.winning && glowAlpha.current > 0}
			<Graphics draw={drawGlow} />
		{/if}
		{@render props.children()}
	</Container>
{/if}
