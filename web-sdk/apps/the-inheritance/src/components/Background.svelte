<script lang="ts">
	import { Rectangle, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const backgroundProps = $derived(context.stateLayoutDerived.normalBackgroundLayout({ scale: 1 }));
</script>

<Rectangle {...context.stateLayoutDerived.canvasSizes()} backgroundColor={0x000000} zIndex={-3} />

<Sprite key="inheritanceBackground" {...backgroundProps} zIndex={-2} />
