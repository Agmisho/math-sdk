<script lang="ts">
	import { onMount } from 'svelte';

	import { Button } from 'components-pixi';
	import { OnHotkey } from 'components-shared';
	import { Rectangle, Sprite, Text } from 'pixi-svelte';
	import { stateBet, stateBetDerived, stateConfig, stateMeta, stateModal, stateSound, type BetModeData } from 'state-shared';

	import { getContext } from '../game/context';
	import { stateInheritanceUi } from '../game/stateInheritanceUi.svelte';
	import { stateGameDerived } from '../game/stateGame.svelte';
	import gameConfig from '../game/config';

	const context = getContext();
	const BET_AMOUNT_OPTIONS = [0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 3, 5, 10, 20, 50, 100, 200, 300];
	const MIN_BET = BET_AMOUNT_OPTIONS[0];
	const MAX_BET = BET_AMOUNT_OPTIONS[BET_AMOUNT_OPTIONS.length - 1];
	const BONUS_MODE_KEY = 'BONUS';
	const SCATTER_BOOST_MODE_KEY = 'SCATTER_BOOST';
	const BUY_BONUS_MULTIPLIER = gameConfig.betModes.bonus.cost;
	const SCATTER_BOOST_MULTIPLIER = gameConfig.betModes.scatter_boost.cost;
	const panelLayout = $derived(context.stateGameDerived.uiPanelLayout());
	const panelWidth = $derived(panelLayout.width);
	const panelHeight = $derived(panelLayout.height);
	const panelX = $derived(panelLayout.x);
	const panelY = $derived(panelLayout.y);
	const uiX = (ratioX: number) => panelX + panelWidth * (ratioX - 0.5);
	const uiY = (ratioY: number) => panelY + panelHeight * (ratioY - 0.5);
	const smallButtonSize = $derived(panelWidth * 0.084);
	const smallHitSize = $derived(smallButtonSize * 1.2);
	const spinButtonSize = $derived(panelWidth * 0.182);
	const spinHitSize = $derived(spinButtonSize * 1.08);
	const betHitWidth = $derived(panelWidth * 0.115);
	const betHitHeight = $derived(panelHeight * 0.22);
	const balanceBackgroundWidth = $derived(panelWidth * 0.086);
	const balanceBackgroundHeight = $derived(panelHeight * 0.138);
	const balanceBackgroundRadius = $derived(panelWidth * 0.008);
	const balanceTextStyle = $derived({
		fontFamily: 'Georgia',
		fontSize: panelWidth * 0.014,
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
	const betModeAssets: BetModeData['assets'] = {
		icon: '',
		volatility: '',
		button: '',
		dialogImage: '',
		dialogVolatility: '',
	};
	const inheritanceBetModeMeta: Record<string, BetModeData> = {
		BASE: {
			mode: 'BASE',
			costMultiplier: 1,
			type: 'default',
			parent: '',
			children: '',
			assets: betModeAssets,
			text: {
				title: 'Base Game',
				dialog: 'Play the base game.',
				button: 'Play',
				tickerIdle: '',
				tickerSpin: '',
			},
		},
		SCATTER_BOOST: {
			mode: SCATTER_BOOST_MODE_KEY,
			costMultiplier: SCATTER_BOOST_MULTIPLIER,
			type: 'activate',
			parent: 'BASE',
			children: '',
			assets: betModeAssets,
			text: {
				title: 'Scatter Boost',
				description: 'Increases the chance of landing a scatter/free-spin trigger.',
				dialog: `Scatter Boost costs ${SCATTER_BOOST_MULTIPLIER}x the selected bet per spin and increases the chance of landing a scatter/free-spin trigger while active.`,
				button: 'Activate',
				tickerIdle: '',
				tickerSpin: '',
			},
		},
		BONUS: {
			mode: BONUS_MODE_KEY,
			costMultiplier: BUY_BONUS_MULTIPLIER,
			type: 'buy',
			parent: 'BASE',
			children: '',
			assets: betModeAssets,
			text: {
				title: 'Buy Bonus',
				description: 'Start 10 free spins immediately.',
				dialog: 'Buy Bonus costs 100x the selected bet and starts 10 free spins immediately.',
				button: 'Buy',
				tickerIdle: '',
				tickerSpin: '',
			},
		},
	};

	let stopDisabled = $state(false);

	const formatMoney = (value: number) =>
		`$${Number(value || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

	const normalizedModeKey = () => stateBet.activeBetModeKey.toUpperCase();
	const isScatterBoostActive = () => normalizedModeKey() === SCATTER_BOOST_MODE_KEY;
	const activeBetModeType = () => {
		const activeMode = stateBetDerived.activeBetMode();
		if (activeMode?.type) return activeMode.type;
		if (isScatterBoostActive()) return 'activate';
		if (normalizedModeKey() === BONUS_MODE_KEY) return 'buy';
		return null;
	};
	const currentBetCost = () => activeBetModeType() === 'activate' ? stateBet.betAmount * SCATTER_BOOST_MULTIPLIER : stateBet.betAmount;
	const canPayForBet = () =>
		stateBet.balanceAmount > 0 &&
		currentBetCost() <= stateBet.balanceAmount;

	onMount(() => {
		stateMeta.betModeMeta = { ...stateMeta.betModeMeta, ...inheritanceBetModeMeta };
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
		stateInheritanceUi.modal = 'info';
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
			stateInheritanceUi.modal = 'buy';
		}
	};

	const pressSpin = () => {
		pressBetSound();
		if (context.stateXstateDerived.isIdle()) {
			if (activeBetModeType() === 'buy') stateBet.activeBetModeKey = 'BASE';
			stateGameDerived.startBaseSpin();
			context.eventEmitter.broadcast({ type: 'bet' });
		} else if (!stopDisabled) {
			if (stateBetDerived.hasAutoBetCounter()) stateBet.autoSpinsCounter = 0;
			context.stateGameDerived.enhancedBoard.stop();
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

<Rectangle
	anchor={0.5}
	x={uiX(0.891)}
	y={uiY(0.462)}
	width={balanceBackgroundWidth}
	height={balanceBackgroundHeight}
	borderRadius={balanceBackgroundRadius}
	backgroundColor={0x02130c}
	backgroundAlpha={0.98}
	zIndex={23}
/>
<Text text={formatMoney(stateBet.balanceAmount)} anchor={0.5} x={uiX(0.891)} y={uiY(0.462)} style={balanceTextStyle} zIndex={24} />
<Text text={formatMoney(stateBet.betAmount)} anchor={0.5} x={uiX(0.500)} y={uiY(0.721)} style={betTextStyle} zIndex={24} />

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

<Button x={uiX(0.405)} y={uiY(0.712)} anchor={0.5} sizes={{ width: betHitWidth, height: betHitHeight }} onpress={pressDecrease} disabled={decreaseDisabled}>
	{#snippet children({ center })}
		<Rectangle {...center} anchor={0.5} width={betHitWidth} height={betHitHeight} backgroundColor={0xffffff} backgroundAlpha={0.01} zIndex={24} />
	{/snippet}
</Button>

<Button x={uiX(0.595)} y={uiY(0.712)} anchor={0.5} sizes={{ width: betHitWidth, height: betHitHeight }} onpress={pressIncrease} disabled={increaseDisabled}>
	{#snippet children({ center })}
		<Rectangle {...center} anchor={0.5} width={betHitWidth} height={betHitHeight} backgroundColor={0xffffff} backgroundAlpha={0.01} zIndex={24} />
	{/snippet}
</Button>
