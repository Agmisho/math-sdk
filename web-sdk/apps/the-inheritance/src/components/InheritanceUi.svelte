<script lang="ts">
	import { Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const UI_RATIO = 1672 / 941;
	const panelWidth = $derived(Math.min(canvas.width * 0.66, canvas.height * 0.32 * UI_RATIO));
	const panelHeight = $derived(panelWidth / UI_RATIO);
	const panelX = $derived(canvas.width / 2);
	const panelY = $derived(canvas.height - panelHeight * 0.02);
	const uiX = (ratioX: number) => panelX + panelWidth * (ratioX - 0.5);
	const uiY = (ratioY: number) => panelY + panelHeight * (ratioY - 0.5);
	const smallButtonSize = $derived(panelWidth * 0.052);
	const spinButtonSize = $derived(panelWidth * 0.115);
</script>

<Sprite key="inheritanceUiPanel" anchor={0.5} x={panelX} y={panelY} width={panelWidth} height={panelHeight} zIndex={20} />
<Sprite key="buttonInfo" anchor={0.5} x={uiX(0.145)} y={uiY(0.370)} width={smallButtonSize} height={smallButtonSize} zIndex={22} />
<Sprite key="buttonSpeed" anchor={0.5} x={uiX(0.237)} y={uiY(0.370)} width={smallButtonSize} height={smallButtonSize} zIndex={22} />
<Sprite key="buttonVolume" anchor={0.5} x={uiX(0.329)} y={uiY(0.370)} width={smallButtonSize} height={smallButtonSize} zIndex={22} />
<Sprite key="buttonSpin" anchor={0.5} x={uiX(0.500)} y={uiY(0.325)} width={spinButtonSize} height={spinButtonSize} zIndex={22} />
<Sprite key="buttonAuto" anchor={0.5} x={uiX(0.671)} y={uiY(0.370)} width={smallButtonSize} height={smallButtonSize} zIndex={22} />
<Sprite key="buttonBuy" anchor={0.5} x={uiX(0.763)} y={uiY(0.370)} width={smallButtonSize} height={smallButtonSize} zIndex={22} />
