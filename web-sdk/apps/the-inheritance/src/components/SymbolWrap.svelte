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
	let wasWinning = false;
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
		graphics.fill({ color: 0x062a1a, alpha: alpha * 0.42 });
		graphics.stroke({ width: 6, color: 0x1f7b4c, alpha: alpha * 0.82 });
		graphics.circle(0, 0, SYMBOL_SIZE * 0.34);
		graphics.stroke({ width: 2, color: 0xffe6a2, alpha: alpha * 0.62 });
	};

	$effect(() => {
		const winning = Boolean(props.winning);
		if (winning === wasWinning) return;
		wasWinning = winning;

		if (winning) {
			void popScale
				.set(1.1, { duration: 160, easing: cubicOut })
				.then(() => popScale.set(1.03, { duration: 420, easing: sineInOut }));
			void glowAlpha
				.set(0.85, { duration: 160, easing: cubicOut })
				.then(() => glowAlpha.set(0.28, { duration: 420, easing: sineInOut }));
			return;
		}

		void popScale.set(1, { duration: 160, easing: sineInOut });
		void glowAlpha.set(0, { duration: 160, easing: sineInOut });
	});
</script>

{#if props.debug || (show && inFrame)}
	<Container x={props.x} y={props.y} scale={popScale.current}>
		{#if props.winning && glowAlpha.current > 0}
			<Graphics draw={drawGlow} />
		{/if}
		{@render props.children()}
	</Container>
{/if}
