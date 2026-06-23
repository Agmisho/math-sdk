<script lang="ts">
	import { Sprite } from 'pixi-svelte';
	import { onDestroy } from 'svelte';

	import { SYMBOL_SIZE } from '../game/constants';
	import { getSymbolInfo } from '../game/utils';
	import type { SymbolState } from '../game/types';

	type Props = {
		x?: number;
		y?: number;
		symbolInfo: ReturnType<typeof getSymbolInfo>;
		state?: SymbolState;
		oncomplete?: () => void;
	};

	const props: Props = $props();
	const SYMBOL_VISUAL_SCALE = 1;
	let completeTimer: ReturnType<typeof setTimeout> | undefined;

	const scheduleComplete = () => {
		if (completeTimer) clearTimeout(completeTimer);
		completeTimer = setTimeout(() => props.oncomplete?.(), props.state === 'win' ? 700 : 0);
	};

	$effect(() => {
		props.symbolInfo;
		props.state;
		scheduleComplete();
	});

	onDestroy(() => {
		if (completeTimer) clearTimeout(completeTimer);
	});
</script>

<Sprite
	x={props.x}
	y={props.y}
	anchor={0.5}
	key={props.symbolInfo.assetKey}
	width={SYMBOL_SIZE * SYMBOL_VISUAL_SCALE * props.symbolInfo.sizeRatios.width}
	height={SYMBOL_SIZE * SYMBOL_VISUAL_SCALE * props.symbolInfo.sizeRatios.height}
/>
