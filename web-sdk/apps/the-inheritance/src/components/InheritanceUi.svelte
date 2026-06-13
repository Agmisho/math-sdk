<script lang="ts">
	import { Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const UI_RATIO = 1672 / 941;
	const panelWidth = $derived(canvas.width * 0.66);
	const panelHeight = $derived(panelWidth / UI_RATIO);
	const panelX = $derived(canvas.width / 2);
	const panelY = $derived(canvas.height - panelHeight * 0.02);
	const uiX = (ratioX: number) => panelX + panelWidth * (ratioX - 0.5);
	const uiY = (ratioY: number) => panelY + panelHeight * (ratioY - 0.5);
	const buttonSize = $derived(panelWidth * 0.058);
	const spinSize = $derived(panelWidth * 0.128);
</script>

<Sprite key="inheritanceUiPanel" anchor={0.5} x={panelX} y={panelY} width={panelWidth} height={panelHeight} zIndex={20} />

<Sprite key="buttonInfo" anchor={0.5} x={uiX(0.142)} y={uiY(0.370)} width={buttonSize} height={buttonSize} zIndex={22} />
<Sprite key="buttonSpeed" anchor={0.5} x={uiX(0.236)} y={uiY(0.370)} width={buttonSize} height={buttonSize} zIndex={22} />
<Sprite key="buttonVolume" anchor={0.5} x={uiX(0.329)} y={uiY(0.370)} width={buttonSize} height={buttonSize} zIndex={22} />
<Sprite key="buttonSpin" anchor={0.5} x={uiX(0.500)} y={uiY(0.325)} width={spinSize} height={spinSize} zIndex={22} />
<Sprite key="buttonAuto" anchor={0.5} x={uiX(0.671)} y={uiY(0.370)} width={buttonSize} height={buttonSize} zIndex={22} />
<Sprite key="buttonBuy" anchor={0.5} x={uiX(0.765)} y={uiY(0.370)} width={buttonSize} height={buttonSize} zIndex={22} />
