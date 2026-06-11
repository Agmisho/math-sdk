<script lang="ts">
	import { Sprite, Text, REM } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const UI_RATIO = 1672 / 941;
	const panelWidth = $derived(canvas.width * 0.82);
	const panelHeight = $derived(panelWidth / UI_RATIO);
	const panelX = $derived(canvas.width / 2);
	const panelY = $derived(canvas.height - panelHeight * 0.38);
	const uiX = (ratioX: number) => panelX + panelWidth * (ratioX - 0.5);
	const uiY = (ratioY: number) => panelY + panelHeight * (ratioY - 0.5);
	const buttonSize = $derived(panelWidth * 0.065);
	const spinSize = $derived(panelWidth * 0.13);
	const valueStyle = {
		fontFamily: 'proxima-nova',
		fontSize: REM * 0.9,
		fontWeight: '700',
		align: 'center',
		fill: 0xffffff,
		stroke: { color: 0x000000, width: 3 },
	};
</script>

<Sprite key="inheritanceUiPanel" anchor={0.5} x={panelX} y={panelY} width={panelWidth} height={panelHeight} zIndex={20} />

<Sprite key="buttonInfo" anchor={0.5} x={uiX(0.10)} y={uiY(0.46)} width={buttonSize} height={buttonSize} zIndex={22} />
<Sprite key="buttonSpeed" anchor={0.5} x={uiX(0.21)} y={uiY(0.46)} width={buttonSize} height={buttonSize} zIndex={22} />
<Sprite key="buttonVolume" anchor={0.5} x={uiX(0.32)} y={uiY(0.46)} width={buttonSize} height={buttonSize} zIndex={22} />
<Sprite key="buttonSpin" anchor={0.5} x={uiX(0.50)} y={uiY(0.39)} width={spinSize} height={spinSize} zIndex={22} />
<Sprite key="buttonAuto" anchor={0.5} x={uiX(0.70)} y={uiY(0.46)} width={buttonSize} height={buttonSize} zIndex={22} />
<Sprite key="buttonBuy" anchor={0.5} x={uiX(0.81)} y={uiY(0.46)} width={buttonSize} height={buttonSize} zIndex={22} />

<Text anchor={0.5} x={uiX(0.91)} y={uiY(0.43)} text={'0.00'} style={valueStyle} zIndex={23} />
<Text anchor={0.5} x={uiX(0.50)} y={uiY(0.78)} text={'BET 1.00'} style={valueStyle} zIndex={23} />
<Text anchor={0.5} x={uiX(0.40)} y={uiY(0.68)} text={'KEYS 0/10'} style={valueStyle} zIndex={23} />
<Text anchor={0.5} x={uiX(0.60)} y={uiY(0.68)} text={'MULTIPLIER x1'} style={valueStyle} zIndex={23} />
