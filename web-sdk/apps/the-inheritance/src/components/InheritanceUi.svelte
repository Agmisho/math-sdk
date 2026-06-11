<script lang="ts">
	import { Sprite, Text, REM } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const UI_RATIO = 1672 / 941;
	const panelWidth = $derived(canvas.width * 0.82);
	const panelHeight = $derived(panelWidth / UI_RATIO);
	const panelX = $derived(canvas.width / 2);
	const panelY = $derived(canvas.height - panelHeight * 0.30);
	const uiX = (ratioX: number) => panelX + panelWidth * (ratioX - 0.5);
	const uiY = (ratioY: number) => panelY + panelHeight * (ratioY - 0.5);
	const buttonSize = $derived(panelWidth * 0.095);
	const spinSize = $derived(panelWidth * 0.17);
	const valueStyle = {
		fontFamily: 'proxima-nova',
		fontSize: REM * 0.75,
		fontWeight: '700',
		align: 'center',
		fill: 0xffffff,
		stroke: { color: 0x000000, width: 3 },
	};
</script>

<Sprite key="inheritanceUiPanel" anchor={0.5} x={panelX} y={panelY} width={panelWidth} height={panelHeight} zIndex={20} />

<Sprite key="buttonInfo" anchor={0.5} x={uiX(0.096)} y={uiY(0.462)} width={buttonSize} height={buttonSize} zIndex={22} />
<Sprite key="buttonSpeed" anchor={0.5} x={uiX(0.207)} y={uiY(0.462)} width={buttonSize} height={buttonSize} zIndex={22} />
<Sprite key="buttonVolume" anchor={0.5} x={uiX(0.315)} y={uiY(0.462)} width={buttonSize} height={buttonSize} zIndex={22} />
<Sprite key="buttonSpin" anchor={0.5} x={uiX(0.500)} y={uiY(0.385)} width={spinSize} height={spinSize} zIndex={22} />
<Sprite key="buttonAuto" anchor={0.5} x={uiX(0.686)} y={uiY(0.462)} width={buttonSize} height={buttonSize} zIndex={22} />
<Sprite key="buttonBuy" anchor={0.5} x={uiX(0.797)} y={uiY(0.462)} width={buttonSize} height={buttonSize} zIndex={22} />

<Text anchor={0.5} x={uiX(0.905)} y={uiY(0.438)} text={'0.00'} style={valueStyle} zIndex={23} />
<Text anchor={0.5} x={uiX(0.500)} y={uiY(0.785)} text={'BET 1.00'} style={valueStyle} zIndex={23} />
<Text anchor={0.5} x={uiX(0.407)} y={uiY(0.680)} text={'KEYS 0/10'} style={valueStyle} zIndex={23} />
<Text anchor={0.5} x={uiX(0.610)} y={uiY(0.680)} text={'MULTIPLIER x1'} style={valueStyle} zIndex={23} />
