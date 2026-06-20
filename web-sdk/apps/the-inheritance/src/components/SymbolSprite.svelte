<script lang="ts">
	import { Sprite } from 'pixi-svelte';
	import { onMount } from 'svelte';

	import { SYMBOL_SIZE } from '../game/constants';
	import { getSymbolInfo } from '../game/utils';

	type Props = {
		x?: number;
		y?: number;
		symbolInfo: ReturnType<typeof getSymbolInfo>;
		oncomplete?: () => void;
	};

	const props: Props = $props();
	const SYMBOL_VISUAL_SCALE = 1.05;

	onMount(() => props.oncomplete?.());

	$effect(() => {
		props.symbolInfo;
		props.oncomplete?.();
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