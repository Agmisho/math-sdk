<script lang="ts" module>
	export type EmitterEventBoardFrame = { type: 'boardFrameGlowShow' } | { type: 'boardFrameGlowHide' };
</script>

<script lang="ts">
	import { Rectangle, Sprite, Text } from 'pixi-svelte';
	import { getContext } from '../game/context';

	const context = getContext();
	const frame = () => context.stateGameDerived.frameLayout();
	const frameX = () => frame().x;
	const frameY = () => frame().y;
	const frameWidth = () => frame().width;
	const frameHeight = () => frame().height;
	const imageX = (ratio: number) => frameX() + frameWidth() * (ratio - 0.5);
	const imageY = (ratio: number) => frameY() + frameHeight() * (ratio - 0.5);
	const counterStyle = () => ({ fontFamily: 'Georgia', fontSize: frameWidth() * 0.020, fontWeight: '800', fill: 0xffe6a2, align: 'center' });
</script>

<Sprite key="inheritanceFrame" anchor={0.5} x={frameX()} y={frameY()} width={frameWidth()} height={frameHeight()} />

<Rectangle anchor={0.5} x={imageX(0.069)} y={imageY(0.578)} width={frameWidth() * 0.102} height={frameHeight() * 0.075} backgroundColor={0x04150c} backgroundAlpha={1} zIndex={24} />

<Text text={`${context.stateGame.keyCounter}`} anchor={0.5} x={imageX(0.069)} y={imageY(0.578)} style={counterStyle()} zIndex={25} />