<script lang="ts">
	import { onMount } from 'svelte';
	import { sineInOut } from 'svelte/easing';
	import { Tween } from 'svelte/motion';
	import { Container, Rectangle, Sprite, Text } from 'pixi-svelte';

	import type { Reel } from '../game/stateGame.svelte';
	import { BOARD_SIZES, REEL_SPACING, SYMBOL_SIZE } from '../game/constants';
	import { getSymbolX } from '../game/utils';
	import BoardContainer from './BoardContainer.svelte';

	type Props = {
		reel: Reel;
		oncomplete: () => void;
	};

	const props: Props = $props();
	const pulse = new Tween(0.32);
	const columnWidth = REEL_SPACING * 0.82;
	const columnHeight = BOARD_SIZES.height * 0.96;
	let finishing = false;
	let cancelled = false;

	const finish = async () => {
		if (finishing) return;
		finishing = true;
		await pulse.set(0, { duration: 240, easing: sineInOut });
		props.oncomplete();
	};

	onMount(() => {
		const animate = async () => {
			while (!cancelled && !finishing) {
				await pulse.set(0.72, { duration: 520, easing: sineInOut });
				if (cancelled || finishing) break;
				await pulse.set(0.32, { duration: 520, easing: sineInOut });
			}
		};
		void animate();
		return () => (cancelled = true);
	});

	$effect(() => {
		if (props.reel.reelState.motion === 'stopped') void finish();
	});
</script>

<BoardContainer>
	<Container x={getSymbolX(props.reel.reelIndex)} y={BOARD_SIZES.height * 0.5} zIndex={30}>
		<Rectangle
			anchor={0.5}
			width={columnWidth}
			height={columnHeight}
			borderRadius={SYMBOL_SIZE * 0.08}
			backgroundColor={0x02170e}
			backgroundAlpha={0.14 + pulse.current * 0.12}
			borderColor={0xd6ad58}
			borderWidth={SYMBOL_SIZE * 0.018}
			borderAlpha={0.48 + pulse.current * 0.45}
		/>
		<Rectangle
			anchor={0.5}
			width={columnWidth * 0.9}
			height={columnHeight * 0.94}
			borderRadius={SYMBOL_SIZE * 0.06}
			backgroundColor={0x0b5d38}
			backgroundAlpha={pulse.current * 0.09}
			borderColor={0x35a86e}
			borderWidth={SYMBOL_SIZE * 0.01}
			borderAlpha={pulse.current * 0.7}
		/>
		<Sprite
			key="S"
			anchor={0.5}
			y={-columnHeight * 0.35}
			width={SYMBOL_SIZE * 0.46}
			height={SYMBOL_SIZE * 0.46}
			alpha={0.62 + pulse.current * 0.38}
		/>
		<Text
			text="VAULT"
			anchor={0.5}
			y={columnHeight * 0.36}
			alpha={0.62 + pulse.current * 0.38}
			style={{
				fontFamily: 'Georgia',
				fontSize: SYMBOL_SIZE * 0.15,
				fontWeight: '800',
				fill: 0xffe6a2,
				stroke: { color: 0x160c04, width: 5 },
				letterSpacing: 2,
			}}
		/>
	</Container>
</BoardContainer>
