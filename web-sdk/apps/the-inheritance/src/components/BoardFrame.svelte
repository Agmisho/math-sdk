<script lang="ts" module>
	export type EmitterEventBoardFrame = { type: 'boardFrameGlowShow' } | { type: 'boardFrameGlowHide' };
</script>

<script lang="ts">
	import { Rectangle, Sprite, Text } from 'pixi-svelte';
	import { getContext } from '../game/context';
	import { LEGACY_KEY_TARGET } from '../game/stateGame.svelte';

	const context = getContext();
	const COUNTER_X_RATIO = 0.069;
	const COUNTER_Y_RATIO = 0.565;
	const COUNTER_WIDTH_RATIO = 0.082;
	const COUNTER_HEIGHT_RATIO = 0.052;
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
	const keyProgress = () => `${Math.min(context.stateGame.keyCounter, LEGACY_KEY_TARGET)} / ${LEGACY_KEY_TARGET}`;
</script>

<Sprite key="inheritanceFrame" anchor={0.5} x={frameX()} y={frameY()} width={frameWidth()} height={frameHeight()} />

<Rectangle
	anchor={0.5}
	x={imageX(COUNTER_X_RATIO)}
	y={imageY(COUNTER_Y_RATIO)}
	width={frameWidth() * COUNTER_WIDTH_RATIO}
	height={frameHeight() * COUNTER_HEIGHT_RATIO}
	backgroundColor={0x061f13}
	backgroundAlpha={0}
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
