<script lang="ts">
	import { onMount } from 'svelte';

	import { Button } from 'components-pixi';
	import { OnHotkey } from 'components-shared';
	import { Rectangle, Sprite, Text } from 'pixi-svelte';
	import { stateBet, stateBetDerived, stateConfig, stateModal, stateSound } from 'state-shared';

	import { getContext } from '../game/context';

	const context = getContext();
	const BET_AMOUNT_OPTIONS = [0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 3, 5, 10, 20, 50, 100, 200, 300];
	const MIN_BET = BET_AMOUNT_OPTIONS[0];
	const MAX_BET = BET_AMOUNT_OPTIONS[BET_AMOUNT_OPTIONS.length - 1];
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
	const smallHitSize = $derived(smallButtonSize * 1.2);
	const spinButtonSize = $derived(panelWidth * 0.170);
	const spinHitSize = $derived(spinButtonSize * 1.08);
	const betHitWidth = $derived(panelWidth * 0.115);
	const betHitHeight = $derived(panelHeight * 0.22);
	const textStyle = $derived({
		fontFamily: 'Georgia',
		fontSize: panelWidth * 0.018,
		fontWeight: '700',
		fill: 0xffe6a2,
		align: 'center',
	});
	const betTextStyle = $derived({
		fontFamily: 'Georgia',
		fontSize: panelWidth * 0.022,
		fontWeight: '800',
		fill: 0xffe6a2,
		align: 'center',
	});
	const BLEND_MODE = 'screen' as const;

	let stopDisabled = $state(false);

	const formatMoney = (value: number) =>
		`$${Number(value || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

	const activeBetModeType = () => stateBetDerived.activeBetMode()?.type ?? null;
	const canPayForBet = () => stateBet.balanceAmount <= 0 || stateBet.betAmount <= stateBet.balanceAmount;

	onMount(() => {
		stateConfig.betAmountOptions = BET_AMOUNT_OPTIONS;
		stateConfig.betMenuOptions = BET_AMOUNT_OPTIONS;
		if (stateBet.betAmount < MIN_BET || stateBet.betAmount > MAX_BET) stateBet.betAmount = MIN_BET;
	});

	const spinDisabled = $derived.by(() => {
		if (context.stateXstateDerived.isIdle()) return !canPayForBet();
		if (stopDisabled) return true;
		if (stateBet.isTurbo && !stateBetDerived.hasAutoBetCounter()) return true;
		return false;
	});
	const autoDisabled = $derived.by(() => {
		if (stateBet.isSpaceHold) return true;
		if (!context.stateXstateDerived.isIdle() && !stateBetDerived.hasAutoBetCounter()) return true;
		if (!canPayForBet()) return true;
		return false;
	});
	const buyDisabled = $derived(!context.stateXstateDerived.isIdle());
	const speedDisabled = $derived(stateBet.isSpaceHold);
	const decreaseDisabled = $derived(stateBet.betAmount <= MIN_BET);
	const increaseDisabled = $derived(stateBet.betAmount >= MAX_BET);

	const pressGeneral = () => context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
	const pressBetSound = () => context.eventEmitter.broadcast({ type: 'soundPressBet' });

	const pressInfo = () => {
		pressGeneral();
		stateModal.modal = { name: 'gameRules' };
	};

	const pressSpeed = () => {
		pressGeneral();
		stateBetDerived.updateIsTurbo(!stateBet.isTurbo, { persistent: true });
	};

	const pressVolume = () => {
		pressGeneral();
		stateSound.volumeValueMaster = stateSound.volumeValueMaster === 0 ? 50 : 0;
	};

	const pressAuto = () => {
		pressGeneral();
		if (stateBetDerived.hasAutoBetCounter()) {
			stateBet.autoSpinsCounter = 0;
		} else {
			stateModal.modal = { name: 'autoSpin' };
		}
	};

	const pressBuy = () => {
		pressGeneral();
		if (activeBetModeType() === 'activate') {
			stateBet.activeBetModeKey = 'BASE';
		} else {
			stateModal.modal = { name: 'buyBonus' };
		}
	};

	const pressSpin = () => {
		pressBetSound();
		if (context.stateXstateDerived.isIdle()) {
			if (activeBetModeType() === 'buy') stateBet.activeBetModeKey = 'BASE';
			context.eventEmitter.broadcast({ type: 'bet' });
		} else if (!stopDisabled) {
			if (stateBetDerived.hasAutoBetCounter()) stateBet.autoSpinsCounter = 0;
			context.eventEmitter.broadcast({ type: 'stopButtonClick' });
		}
	};

	const pressDecrease = () => {
		pressGeneral();
		const nextSmaller = [...BET_AMOUNT_OPTIONS].sort((a, b) => b - a).find((option) => option < stateBet.betAmount);
		stateBet.betAmount = nextSmaller || MIN_BET;
	};

	const pressIncrease = () => {
		pressGeneral();
		const nextBigger = [...BET_AMOUNT_OPTIONS].sort((a, b) => a - b).find((option) => option > stateBet.betAmount);
		stateBet.betAmount = nextBigger || MAX_BET;
	};

	context.eventEmitter.subscribeOnMount({
		stopButtonClick: () => {
			stopDisabled = true;
			stateBetDerived.updateIsTurbo(true, { persistent: false });
		},
		stopButtonEnable: () => {
			stopDisabled = false;
			stateBetDerived.updateIsTurbo(false, { persistent: false });
		},
	});
</script>

<Sprite key="inheritanceUiPanel" anchor={0.5} x={panelX} y={panelY} width={panelWidth} height={panelHeight} blendMode={BLEND_MODE} zIndex={20} />
<OnHotkey hotkey="Space" disabled={spinDisabled} onpress={pressSpin} />

<Text text={formatMoney(stateBet.balanceAmount)} anchor={0.5} x={uiX(0.891)} y={uiY(0.462)} style={textStyle} zIndex={24} />
<Text text={formatMoney(stateBet.betAmount)} anchor={0.5} x={uiX(0.500)} y={uiY(0.735)} style={betTextStyle} zIndex={24} />

<Button x={uiX(0.108)} y={uiY(0.462)} anchor={0.5} sizes={{ width: smallHitSize, height: smallHitSize }} onpress={pressInfo}>
	{#snippet children({ center, hovered, pressed })}
		<Sprite key="buttonInfo" {...center} anchor={0.5} width={smallButtonSize} height={smallButtonSize} alpha={pressed ? 0.82 : hovered ? 1 : 0.95} blendMode={BLEND_MODE} zIndex={22} />
	{/snippet}
</Button>

<Button x={uiX(0.218)} y={uiY(0.462)} anchor={0.5} sizes={{ width: smallHitSize, height: smallHitSize }} onpress={pressSpeed} disabled={speedDisabled}>
	{#snippet children({ center, hovered, pressed })}
		<Sprite key={stateBet.isTurbo ? 'buttonSpeedActive' : 'buttonSpeed'} {...center} anchor={0.5} width={smallButtonSize} height={smallButtonSize} alpha={speedDisabled ? 0.45 : pressed ? 0.82 : hovered || stateBet.isTurbo ? 1 : 0.95} blendMode={BLEND_MODE} zIndex={22} />
	{/snippet}
</Button>

<Button x={uiX(0.329)} y={uiY(0.462)} anchor={0.5} sizes={{ width: smallHitSize, height: smallHitSize }} onpress={pressVolume}>
	{#snippet children({ center, hovered, pressed })}
		<Sprite key="buttonVolume" {...center} anchor={0.5} width={smallButtonSize} height={smallButtonSize} alpha={stateSound.volumeValueMaster === 0 ? 0.5 : pressed ? 0.82 : hovered ? 1 : 0.95} blendMode={BLEND_MODE} zIndex={22} />
	{/snippet}
</Button>

<Button x={uiX(0.500)} y={uiY(0.398)} anchor={0.5} sizes={{ width: spinHitSize, height: spinHitSize }} onpress={pressSpin} disabled={spinDisabled}>
	{#snippet children({ center, hovered, pressed })}
		<Sprite key="buttonSpin" {...center} anchor={0.5} width={spinButtonSize} height={spinButtonSize} alpha={spinDisabled ? 0.48 : pressed ? 0.82 : hovered ? 1 : 0.98} blendMode={BLEND_MODE} zIndex={22} />
	{/snippet}
</Button>

<Button x={uiX(0.671)} y={uiY(0.462)} anchor={0.5} sizes={{ width: smallHitSize, height: smallHitSize }} onpress={pressAuto} disabled={autoDisabled}>
	{#snippet children({ center, hovered, pressed })}
		<Sprite key="buttonAuto" {...center} anchor={0.5} width={smallButtonSize} height={smallButtonSize} alpha={autoDisabled ? 0.45 : pressed ? 0.82 : hovered || stateBetDerived.hasAutoBetCounter() ? 1 : 0.95} blendMode={BLEND_MODE} zIndex={22} />
	{/snippet}
</Button>

<Button x={uiX(0.780)} y={uiY(0.462)} anchor={0.5} sizes={{ width: smallHitSize, height: smallHitSize }} onpress={pressBuy} disabled={buyDisabled}>
	{#snippet children({ center, hovered, pressed })}
		<Sprite key="buttonBuy" {...center} anchor={0.5} width={smallButtonSize} height={smallButtonSize} alpha={buyDisabled ? 0.45 : pressed ? 0.82 : hovered || activeBetModeType() === 'activate' ? 1 : 0.95} blendMode={BLEND_MODE} zIndex={22} />
	{/snippet}
</Button>

<Button x={uiX(0.430)} y={uiY(0.712)} anchor={0.5} sizes={{ width: betHitWidth, height: betHitHeight }} onpress={pressDecrease} disabled={decreaseDisabled}>
	{#snippet children({ center })}
		<Rectangle {...center} anchor={0.5} width={betHitWidth} height={betHitHeight} backgroundColor={0xffffff} backgroundAlpha={0.01} zIndex={24} />
	{/snippet}
</Button>

<Button x={uiX(0.570)} y={uiY(0.712)} anchor={0.5} sizes={{ width: betHitWidth, height: betHitHeight }} onpress={pressIncrease} disabled={increaseDisabled}>
	{#snippet children({ center })}
		<Rectangle {...center} anchor={0.5} width={betHitWidth} height={betHitHeight} backgroundColor={0xffffff} backgroundAlpha={0.01} zIndex={24} />
	{/snippet}
</Button>
