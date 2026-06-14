<script lang="ts" module>
	export type EmitterEventBoardFrame =
		| { type: 'boardFrameGlowShow' }
		| { type: 'boardFrameGlowHide' };
</script>

<script lang="ts">
	import { Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const BLEND_MODE = 'screen' as const;
</script>

<Sprite
	key="inheritanceFrame"
	anchor={0}
	x={0}
	y={0}
	width={context.stateGameDerived.boardLayout().frameWidth}
	height={context.stateGameDerived.boardLayout().frameHeight}
	blendMode={BLEND_MODE}
/>
