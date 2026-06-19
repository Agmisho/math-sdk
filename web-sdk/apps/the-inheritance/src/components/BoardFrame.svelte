<script lang="ts" module>
	export type EmitterEventBoardFrame =
		| { type: 'boardFrameGlowShow' }
		| { type: 'boardFrameGlowHide' };
</script>

<script lang="ts">
	import { Sprite, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const board = () => context.stateGameDerived.boardLayout();
	const keyCounterX = () => board().x - board().frameWidth * 0.412;
	const keyCounterY = () => board().y + board().frameHeight * 0.11;
	const keyCounterStyle = () => ({
		fontFamily: 'Georgia',
		fontSize: board().frameWidth * 0.023,
		fontWeight: '800',
		fill: 0xffe6a2,
		align: 'center',
	});
</script>

<Sprite
	key="inheritanceFrame"
	anchor={0.5}
	x={board().x}
	y={board().y}
	width={board().frameWidth}
	height={board().frameHeight}
/>

<Text
	text={`${context.stateGame.keyCounter}`}
	anchor={0.5}
	x={keyCounterX()}
	y={keyCounterY()}
	style={keyCounterStyle()}
	zIndex={25}
/>
