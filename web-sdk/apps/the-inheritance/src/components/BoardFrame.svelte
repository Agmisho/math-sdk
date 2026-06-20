<script lang="ts" module>
	export type EmitterEventBoardFrame =
		| { type: 'boardFrameGlowShow' }
		| { type: 'boardFrameGlowHide' };
</script>

<script lang="ts">
	import { Rectangle, Sprite, Text } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const board = () => context.stateGameDerived.boardLayout();
	const frameX = () => board().frameX ?? board().x;
	const frameDisplayWidth = () => board().frameWidth;
	const frameDisplayHeight = () => board().frameHeight;
	const imageX = (ratioX: number) => frameX() + frameDisplayWidth() * (ratioX - 0.5);
	const imageY = (ratioY: number) => board().y + frameDisplayHeight() * (ratioY - 0.5);
	const keyCounterStyle = () => ({
		fontFamily: 'Georgia',
		fontSize: frameDisplayWidth() * 0.020,
		fontWeight: '800',
		fill: 0xffe6a2,
		align: 'center',
	});
</script>

<Sprite
	key="inheritanceFrame"
	anchor={0.5}
	x={frameX()}
	y={board().y}
	width={frameDisplayWidth()}
	height={frameDisplayHeight()}
/>

<Rectangle
	anchor={0.5}
	x={imageX(0.107)}
	y={imageY(0.624)}
	width={frameDisplayWidth() * 0.070}
	height={frameDisplayHeight() * 0.040}
	backgroundColor={0x04150c}
	backgroundAlpha={0.98}
	zIndex={24}
/>

<Text
	text={`${context.stateGame.keyCounter}`}
	anchor={0.5}
	x={imageX(0.107)}
	y={imageY(0.624)}
	style={keyCounterStyle()}
	zIndex={25}
/>