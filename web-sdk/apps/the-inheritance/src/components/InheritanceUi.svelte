<script lang="ts">
	import { Sprite, Text, REM } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const panelY = $derived(canvas.height - 88);
	const labelStyle = {
		fontFamily: 'proxima-nova',
		fontSize: REM * 1.35,
		fontWeight: '700',
		align: 'center',
		fill: 0xffffff,
		stroke: { color: 0x000000, width: 4 },
	};
	const smallStyle = {
		fontFamily: 'proxima-nova',
		fontSize: REM * 1.0,
		fontWeight: '700',
		align: 'center',
		fill: 0xffffff,
		stroke: { color: 0x000000, width: 3 },
	};
</script>

<Sprite
	key="inheritanceUiPanel"
	anchor={0.5}
	x={canvas.width / 2}
	y={panelY}
	width={canvas.width * 0.86}
	height={canvas.height * 0.22}
	zIndex={20}
/>

<Text anchor={0.5} x={canvas.width * 0.30} y={panelY - 20} text={'BALANCE\n0.00'} style={labelStyle} zIndex={21} />
<Text anchor={0.5} x={canvas.width * 0.50} y={panelY - 20} text={'WIN\n0.00'} style={labelStyle} zIndex={21} />
<Text anchor={0.5} x={canvas.width * 0.70} y={panelY - 20} text={'BET\n1.00'} style={labelStyle} zIndex={21} />
<Text anchor={0.5} x={canvas.width * 0.40} y={panelY + 42} text={'KEYS 0/10'} style={smallStyle} zIndex={21} />
<Text anchor={0.5} x={canvas.width * 0.60} y={panelY + 42} text={'MULTIPLIER x1'} style={smallStyle} zIndex={21} />

<Sprite key="buttonInfo" anchor={0.5} x={canvas.width * 0.20} y={panelY + 42} width={74} height={74} zIndex={22} />
<Sprite key="buttonBuy" anchor={0.5} x={canvas.width * 0.27} y={panelY + 42} width={86} height={86} zIndex={22} />
<Sprite key="buttonSpeed" anchor={0.5} x={canvas.width * 0.47} y={panelY + 42} width={78} height={78} zIndex={22} />
<Sprite key="buttonAuto" anchor={0.5} x={canvas.width * 0.53} y={panelY + 42} width={86} height={86} zIndex={22} />
<Sprite key="buttonSpin" anchor={0.5} x={canvas.width * 0.76} y={panelY + 42} width={106} height={106} zIndex={22} />
<Sprite key="buttonVolume" anchor={0.5} x={canvas.width * 0.84} y={panelY + 42} width={74} height={74} zIndex={22} />
