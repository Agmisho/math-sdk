<script lang="ts" module>
	export type EmitterEventBoardFrame =
		| { type: 'boardFrameGlowShow' }
		| { type: 'boardFrameGlowHide' };
</script>

<script lang="ts">
	import { Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const FRAME_RATIO = 1672 / 941;
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const frameWidth = $derived(canvas.width * 0.66);
	const frameHeight = $derived(frameWidth / FRAME_RATIO);
	const frameY = $derived(frameHeight * 0.52 + 12);
</script>

<Sprite
	key="inheritanceFrame"
	anchor={0.5}
	x={canvas.width / 2}
	y={frameY}
	width={frameWidth}
	height={frameHeight}
/>
