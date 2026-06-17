<script lang="ts">
	import { Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const UI_RATIO = 1672 / 941;
	const isPortrait = $derived(canvas.height > canvas.width * 1.05);
	const boardLayout = $derived(context.stateGameDerived.boardLayout());
	const panelWidth = $derived(Math.min(canvas.width * (isPortrait ? 0.90 : 0.68), canvas.height * 0.40 * UI_RATIO));
	const panelHeight = $derived(panelWidth / UI_RATIO);
	const panelX = $derived(canvas.width / 2);
	const panelY = $derived(boardLayout.y + boardLayout.frameHeight / 2 + panelHeight * 0.36);
	const uiX = (ratioX: number) => panelX + panelWidth * (ratioX - 0.5);
	const uiY = (ratioY: number) => panelY + panelHeight * (ratioY - 0.5);
	const smallButtonSize = $derived(panelWidth * 0.084);
	const spinButtonSize = $derived(panelWidth * 0.170);
	const BLEND_MODE = 'screen' as const;
</script>

<Sprite key="inheritanceUiPanel" anchor={0.5} x={panelX} y={panelY} width={panelWidth} height={panelHeight} blendMode={BLEND_MODE} zIndex={20} />

<Sprite key="buttonInfo" anchor={0.5} x={uiX(0.108)} y={uiY(0.462)} width={smallButtonSize} height={smallButtonSize} blendMode={BLEND_MODE} zIndex={22} />
<Sprite key="buttonSpeed" anchor={0.5} x={uiX(0.218)} y={uiY(0.462)} width={smallButtonSize} height={smallButtonSize} blendMode={BLEND_MODE} zIndex={22} />
<Sprite key="buttonVolume" anchor={0.5} x={uiX(0.329)} y={uiY(0.462)} width={smallButtonSize} height={smallButtonSize} blendMode={BLEND_MODE} zIndex={22} />
<Sprite key="buttonSpin" anchor={0.5} x={uiX(0.500)} y={uiY(0.398)} width={spinButtonSize} height={spinButtonSize} blendMode={BLEND_MODE} zIndex={22} />
<Sprite key="buttonAuto" anchor={0.5} x={uiX(0.671)} y={uiY(0.462)} width={smallButtonSize} height={smallButtonSize} blendMode={BLEND_MODE} zIndex={22} />
<Sprite key="buttonBuy" anchor={0.5} x={uiX(0.780)} y={uiY(0.462)} width={smallButtonSize} height={smallButtonSize} blendMode={BLEND_MODE} zIndex={22} />
