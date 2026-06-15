<script lang="ts">
	import { Button } from 'components-pixi';
	import { OnHotkey } from 'components-shared';
	import { Rectangle, Sprite } from 'pixi-svelte';
	import { stateBet, stateBetDerived, stateConfig, stateModal, stateSound } from 'state-shared';

	import { getContext } from '../game/context';

	const context = getContext();
	const UI_RATIO = 1672 / 941;
	const BLEND_MODE = 'screen' as const;

	let stopDisabled = $state(false);

	const spinDisabled = $derived.by(() => {
		if (context.stateXstateDerived.isIdle()) return !stateBetDerived.isBetCostAvailable();
		if (stopDisabled) return true;
		if (stateBet.isTurbo && !stateBetDerived.hasAutoBetCounter()) return true;
		return false;
	});
	const autoDisabled = $derived.by(() => {
		if (stateBet.isSpaceHold) return true;
		if (!context.stateXstateDerived.isIdle() && !stateBetDerived.hasAutoBetCounter()) return true;
		if (!stateBetDerived.isBetCostAvailable()) return true;
		return false;
	});
	const buyDisabled = $derived(!context.stateXstateDerived.isIdle());
	const speedDisabled = $derived(stateBet.isSpaceHold);
	const smallestBet = $derived(stateConfig.betAmountOptions[0]);
	const biggestBet = $derived(stateConfig.betAmountOptions[stateConfig.betAmountOptions.length - 1]);
	const decreaseDisabled = $derived(
		!context.stateXstateDerived.isIdle() || stateBet.betAmount === smallestBet,
	);
	const increaseDisabled = $derived(
		!context.stateXstateDerived.isIdle() || stateBet.betAmount === biggestBet,
	);

	const canvas = () => context.stateLayoutDerived.canvasSizes();
	const isPortrait = () => canvas().height > canvas().width * 1.05;
	const panelWidth = () =>
		Math.min(
			canvas().width * (isPortrait() ? 0.96 : 0.78),
			canvas().height * (isPortrait() ? 0.34 : 0.48) * UI_RATIO,
		);
	const panelHeight = () => panelWidth() / UI_RATIO;
	const panelX = () => canvas().width * 0.5;
	const panelY = () => canvas().height - panelHeight() * (isPortrait() ? 0.25 : 0.36);
	const uiX = (ratioX: number) => panelX() + panelWidth() * (ratioX - 0.5);
	const uiY = (ratioY: number) => panelY() + panelHeight() * (ratioY - 0.5);
	const smallButtonSize = () => Math.max(34, panelWidth() * (isPortrait() ? 0.078 : 0.06));
	const spinButtonSize = () => Math.max(68, panelWidth() * (isPortrait() ? 0.18 : 0.13));
	const smallButtonY = () => uiY(isPortrait() ? 0.36 : 0.34);
	const spinButtonY = () => uiY(isPortrait() ? 0.3 : 0.27);
	const betButtonY = () => uiY(0.7);
	const hitAlpha = 0.001;

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
		if (stateBetDerived.activeBetMode()?.type === 'activate') {
			stateBet.activeBetModeKey = 'BASE';
		} else {
			stateModal.modal = { name: 'buyBonus' };
		}
	};

	const pressSpin = () => {
		pressBetSound();

		if (context.stateXstateDerived.isIdle()) {
			if (stateBetDerived.activeBetMode()?.type === 'buy') stateBet.activeBetModeKey = 'BASE';
			context.eventEmitter.broadcast({ type: 'bet' });
		} else if (!stopDisabled) {
			if (stateBetDerived.hasAutoBetCounter()) stateBet.autoSpinsCounter = 0;
			context.eventEmitter.broadcast({ type: 'stopButtonClick' });
		}
	};

	const pressDecrease = () => {
		pressGeneral();
		const nextSmaller = [...stateConfig.betAmountOptions]
			.sort((a, b) => b - a)
			.find((option) => option < stateBet.betAmount);

		stateBetDerived.setBetAmount(nextSmaller || smallestBet);
	};

	const pressIncrease = () => {
		pressGeneral();
		const nextBigger = [...stateConfig.betAmountOptions]
			.sort((a, b) => a - b)
			.find((option) => option > stateBet.betAmount);

		stateBetDerived.setBetAmount(nextBigger || biggestBet);
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

<OnHotkey hotkey="Space" disabled={spinDisabled} onpress={pressSpin} />

<Sprite
	key="inheritanceUiPanel"
	anchor={0.5}
	x={panelX()}
	y={panelY()}
	width={panelWidth()}
	height={panelHeight()}
	zIndex={30}
/>

<Button x={uiX(0.108)} y={smallButtonY()} anchor={0.5} sizes={{ width: smallButtonSize(), height: smallButtonSize() }} onpress={pressInfo}>
	{#snippet children({ center, hovered, pressed })}
		<Sprite key="buttonInfo" {...center} anchor={0.5} width={smallButtonSize()} height={smallButtonSize()} alpha={pressed ? 0.82 : hovered ? 1 : 0.96} blendMode={BLEND_MODE} zIndex={32} />
	{/snippet}
</Button>

<Button
	x={uiX(0.196)}
	y={smallButtonY()}
	anchor={0.5}
	sizes={{ width: smallButtonSize(), height: smallButtonSize() }}
	onpress={pressSpeed}
	disabled={speedDisabled}
>
	{#snippet children({ center, hovered, pressed })}
		<Sprite key={stateBet.isTurbo ? 'buttonSpeedActive' : 'buttonSpeed'} {...center} anchor={0.5} width={smallButtonSize()} height={smallButtonSize()} alpha={speedDisabled ? 0.4 : pressed ? 0.82 : hovered || stateBet.isTurbo ? 1 : 0.96} blendMode={BLEND_MODE} zIndex={32} />
	{/snippet}
</Button>

<Button x={uiX(0.286)} y={smallButtonY()} anchor={0.5} sizes={{ width: smallButtonSize(), height: smallButtonSize() }} onpress={pressVolume}>
	{#snippet children({ center, hovered, pressed })}
		<Sprite key="buttonVolume" {...center} anchor={0.5} width={smallButtonSize()} height={smallButtonSize()} alpha={stateSound.volumeValueMaster === 0 ? 0.48 : pressed ? 0.82 : hovered ? 1 : 0.96} blendMode={BLEND_MODE} zIndex={32} />
	{/snippet}
</Button>

<Button
	x={panelX()}
	y={spinButtonY()}
	anchor={0.5}
	sizes={{ width: spinButtonSize(), height: spinButtonSize() }}
	onpress={pressSpin}
	disabled={spinDisabled}
>
	{#snippet children({ center, hovered, pressed })}
		<Sprite key="buttonSpin" {...center} anchor={0.5} width={spinButtonSize()} height={spinButtonSize()} alpha={spinDisabled ? 0.46 : pressed ? 0.84 : hovered ? 1 : 0.98} blendMode={BLEND_MODE} zIndex={33} />
	{/snippet}
</Button>

<Button
	x={uiX(0.694)}
	y={smallButtonY()}
	anchor={0.5}
	sizes={{ width: smallButtonSize(), height: smallButtonSize() }}
	onpress={pressAuto}
	disabled={autoDisabled}
>
	{#snippet children({ center, hovered, pressed })}
		<Sprite key="buttonAuto" {...center} anchor={0.5} width={smallButtonSize()} height={smallButtonSize()} alpha={autoDisabled ? 0.42 : pressed ? 0.82 : hovered || stateBetDerived.hasAutoBetCounter() ? 1 : 0.96} blendMode={BLEND_MODE} zIndex={32} />
	{/snippet}
</Button>

<Button
	x={uiX(0.786)}
	y={smallButtonY()}
	anchor={0.5}
	sizes={{ width: smallButtonSize(), height: smallButtonSize() }}
	onpress={pressBuy}
	disabled={buyDisabled}
>
	{#snippet children({ center, hovered, pressed })}
		<Sprite key="buttonBuy" {...center} anchor={0.5} width={smallButtonSize()} height={smallButtonSize()} alpha={buyDisabled ? 0.42 : pressed ? 0.82 : hovered || stateBetDerived.activeBetMode()?.type === 'activate' ? 1 : 0.96} blendMode={BLEND_MODE} zIndex={32} />
	{/snippet}
</Button>

<Button
	x={uiX(0.372)}
	y={betButtonY()}
	anchor={0.5}
	sizes={{ width: smallButtonSize() * 0.9, height: smallButtonSize() * 0.72 }}
	onpress={pressDecrease}
	disabled={decreaseDisabled}
>
	{#snippet children({ center })}
		<Rectangle {...center} anchor={0.5} width={smallButtonSize() * 0.9} height={smallButtonSize() * 0.72} backgroundColor={0xffffff} backgroundAlpha={hitAlpha} zIndex={34} />
	{/snippet}
</Button>

<Button
	x={uiX(0.628)}
	y={betButtonY()}
	anchor={0.5}
	sizes={{ width: smallButtonSize() * 0.9, height: smallButtonSize() * 0.72 }}
	onpress={pressIncrease}
	disabled={increaseDisabled}
>
	{#snippet children({ center })}
		<Rectangle {...center} anchor={0.5} width={smallButtonSize() * 0.9} height={smallButtonSize() * 0.72} backgroundColor={0xffffff} backgroundAlpha={hitAlpha} zIndex={34} />
	{/snippet}
</Button>
