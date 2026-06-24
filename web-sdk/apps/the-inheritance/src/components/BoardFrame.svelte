<script lang="ts" module>
	export type EmitterEventBoardFrame = { type: 'boardFrameGlowShow' } | { type: 'boardFrameGlowHide' };
</script>

<script lang="ts">
	import { Rectangle, Sprite, Text } from 'pixi-svelte';
	import { getContext } from '../game/context';

	const context = getContext();
	const COUNTER_X_RATIO = 0.069;
	const COUNTER_Y_RATIO = 0.576;
	const COUNTER_MASK_WIDTH_RATIO = 0.090;
	const COUNTER_MASK_HEIGHT_RATIO = 0.060;
	const frame = () => context.stateGameDerived.frameLayout();
	const frameX = () => frame().x;
	const frameY = () => frame().y;
	const frameWidth = () => frame().width;
	const frameHeight = () => frame().height;
	const imageX = (ratio: number) => frameX() + frameWidth() * (ratio - 0.5);
	const imageY = (ratio: number) => frameY() + frameHeight() * (ratio - 0.5);
	const counterStyle = () => ({
		fontFamily: 'Georgia',
		fontSize: frameWidth() * 0.014,
		fontWeight: '800',
		fill: 0xffe6a2,
		align: 'center',
		stroke: { color: 0x201106, width: 3 },
	});
	const keyProgress = () => `${Math.min(context.stateGame.keyCounter, context.stateGame.keyTarget)} / ${context.stateGame.keyTarget}`;
</script>

<Sprite key="inheritanceFrame" anchor={0.5} x={frameX()} y={frameY()} width={frameWidth()} height={frameHeight()} />

<Rectangle
	anchor={0.5}
	x={imageX(COUNTER_X_RATIO)}
	y={imageY(COUNTER_Y_RATIO)}
	width={frameWidth() * COUNTER_MASK_WIDTH_RATIO}
	height={frameHeight() * COUNTER_MASK_HEIGHT_RATIO}
	backgroundColor={0x04150c}
	backgroundAlpha={1}
	zIndex={24}
/>

<Text
	text={keyProgress()}
	anchor={0.5}
	x={imageX(COUNTER_X_RATIO)}
	y={imageY(COUNTER_Y_RATIO)}
	style={counterStyle()}
	zIndex={25}
/>
