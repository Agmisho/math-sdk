<script lang="ts" module>
	export type EmitterEventBoardFrame =
		| { type: 'boardFrameGlowShow' }
		| { type: 'boardFrameGlowHide' };
</script>

<script lang="ts">
	import { Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
</script>

<Sprite
	key="inheritanceFrame"
	anchor={0.5}
	x={context.stateGameDerived.boardLayout().x}
	y={context.stateGameDerived.boardLayout().y}
	width={context.stateGameDerived.boardLayout().frameWidth}
	height={context.stateGameDerived.boardLayout().frameHeight}
/>
