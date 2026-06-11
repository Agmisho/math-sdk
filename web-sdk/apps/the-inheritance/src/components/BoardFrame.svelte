<script lang="ts" module>
	export type EmitterEventBoardFrame =
		| { type: 'boardFrameGlowShow' }
		| { type: 'boardFrameGlowHide' };
</script>

<script lang="ts">
	import { Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const POSITION_ADJUSTMENT = 1.0;
	const SPRITE_SCALE = { width: 1.28, height: 1.18 };
</script>

<Sprite
	key="inheritanceFrame"
	anchor={0.5}
	x={context.stateGameDerived.boardLayout().x * POSITION_ADJUSTMENT}
	y={context.stateGameDerived.boardLayout().y * POSITION_ADJUSTMENT}
	width={context.stateGameDerived.boardLayout().width * SPRITE_SCALE.width}
	height={context.stateGameDerived.boardLayout().height * SPRITE_SCALE.height}
/>
