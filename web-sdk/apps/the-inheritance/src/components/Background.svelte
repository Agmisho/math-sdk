<script lang="ts">
	import { Rectangle, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
</script>

<Rectangle {...context.stateLayoutDerived.canvasSizes()} backgroundColor={0x000000} zIndex={-3} />

<Sprite
	key="inheritanceBackground"
	anchor={0.5}
	x={context.stateLayoutDerived.canvasSizes().width / 2}
	y={context.stateLayoutDerived.canvasSizes().height / 2}
	width={context.stateLayoutDerived.canvasSizes().width}
	height={context.stateLayoutDerived.canvasSizes().height}
	zIndex={-2}
/>
