<script lang="ts" module>
	export type EmitterEventBoardFrame =
		| { type: 'boardFrameGlowShow' }
		| { type: 'boardFrameGlowHide' };
</script>

<script lang="ts">
	import { Rectangle, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const BLEND_MODE = 'screen' as const;
	const board = () => context.stateGameDerived.boardLayout();
</script>

<Rectangle
	anchor={0.5}
	x={board().x}
	y={board().y}
	width={board().screenWidth * 1.03}
	height={board().screenHeight * 1.03}
	backgroundColor={0x02110b}
	backgroundAlpha={0.86}
	borderColor={0x9c7425}
	borderWidth={Math.max(1, board().scale * 2)}
	borderAlpha={0.5}
	borderRadius={Math.max(8, board().scale * 10)}
/>

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
