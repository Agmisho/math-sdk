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
	const FRAME_DISPLAY_SCALE = 1.28;
	const frameDisplayWidth = () => board().frameWidth * FRAME_DISPLAY_SCALE;
	const frameDisplayHeight = () => board().frameHeight * FRAME_DISPLAY_SCALE;
	const imageX = (ratioX: number) => board().x + frameDisplayWidth() * (ratioX - 0.5);
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
	x={board().x}
	y={board().y}
	width={frameDisplayWidth()}
	height={frameDisplayHeight()}
	blendMode="screen"
/>

<Rectangle
	anchor={0.5}
	x={imageX(0.088)}
	y={imageY(0.587)}
	width={frameDisplayWidth() * 0.082}
	height={frameDisplayHeight() * 0.045}
	backgroundColor={0x04150c}
	backgroundAlpha={0.92}
	zIndex={24}
/>

<Text
	text={`${context.stateGame.keyCounter}`}
	anchor={0.5}
	x={imageX(0.088)}
	y={imageY(0.587)}
	style={keyCounterStyle()}
	zIndex={25}
/>
