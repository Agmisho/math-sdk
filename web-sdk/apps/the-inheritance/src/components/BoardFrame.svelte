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
	const board = () => context.stateGameDerived.boardLayout();
</script>

<Sprite
	key="inheritanceFrame"
	anchor={0.5}
	x={board().x}
	y={board().y}
	width={board().frameWidth}
	height={board().frameHeight}
	alpha={0.96}
	blendMode={BLEND_MODE}
/>
