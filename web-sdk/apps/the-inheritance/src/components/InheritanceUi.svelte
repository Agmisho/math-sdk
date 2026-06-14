<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { Button } from 'components-pixi';
	import { OnHotkey } from 'components-shared';
	import { Rectangle, Sprite } from 'pixi-svelte';
	import { stateBet, stateBetDerived, stateConfig, stateModal, stateSound } from 'state-shared';

	import { getContext } from '../game/context';

	const context = getContext();
	const ARTBOARD = { width: 1672, height: 941 };
	const BLEND_MODE = 'screen';

	let stopDisabled = $state(false);

	const px = (value: number) => context.stateLayoutDerived.mainLayout().width * (value / ARTBOARD.width);
	const py = (value: number) => context.stateLayoutDerived.mainLayout().height * (value / ARTBOARD.height);
	const size = (value: number) => context.stateLayoutDerived.mainLayout().width * (value / ARTBOARD.width);

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

<MainContainer>
	<Sprite
		key="inheritanceUiPanel"
		anchor={0}
		x={0}
		y={0}
		width={context.stateLayoutDerived.mainLayout().width}
		height={context.stateLayoutDerived.mainLayout().height}
		blendMode={BLEND_MODE}
	/>

	<OnHotkey hotkey="Space" disabled={spinDisabled} onpress={pressSpin} />

	<Button x={px(180)} y={py(435)} anchor={0.5} sizes={{ width: size(165), height: size(165) }} onpress={pressInfo}>
		{#snippet children({ center, hovered, pressed })}
			<Sprite
				key="buttonInfo"
				{...center}
				anchor={0.5}
				width={size(165)}
				height={size(165)}
				alpha={pressed ? 0.84 : hovered ? 1 : 0.95}
				blendMode={BLEND_MODE}
			/>
		{/snippet}
	</Button>

	<Button
		x={px(365)}
		y={py(435)}
		anchor={0.5}
		sizes={{ width: size(165), height: size(165) }}
		onpress={pressSpeed}
		disabled={speedDisabled}
	>
		{#snippet children({ center, hovered, pressed })}
			<Sprite
				key={stateBet.isTurbo ? 'buttonSpeedActive' : 'buttonSpeed'}
				{...center}
				anchor={0.5}
				width={size(165)}
				height={size(165)}
				alpha={speedDisabled ? 0.45 : pressed ? 0.84 : hovered || stateBet.isTurbo ? 1 : 0.95}
				blendMode={BLEND_MODE}
			/>
		{/snippet}
	</Button>

	<Button x={px(550)} y={py(435)} anchor={0.5} sizes={{ width: size(165), height: size(165) }} onpress={pressVolume}>
		{#snippet children({ center, hovered, pressed })}
			<Sprite
				key="buttonVolume"
				{...center}
				anchor={0.5}
				width={size(165)}
				height={size(165)}
				alpha={stateSound.volumeValueMaster === 0 ? 0.5 : pressed ? 0.84 : hovered ? 1 : 0.95}
				blendMode={BLEND_MODE}
			/>
		{/snippet}
	</Button>

	<Button
		x={px(836)}
		y={py(375)}
		anchor={0.5}
		sizes={{ width: size(320), height: size(320) }}
		onpress={pressSpin}
		disabled={spinDisabled}
	>
		{#snippet children({ center, hovered, pressed })}
			<Sprite
				key="buttonSpin"
				{...center}
				anchor={0.5}
				width={size(320)}
				height={size(320)}
				alpha={spinDisabled ? 0.48 : pressed ? 0.84 : hovered ? 1 : 0.98}
				blendMode={BLEND_MODE}
			/>
		{/snippet}
	</Button>

	<Button
		x={px(1130)}
		y={py(435)}
		anchor={0.5}
		sizes={{ width: size(165), height: size(165) }}
		onpress={pressAuto}
		disabled={autoDisabled}
	>
		{#snippet children({ center, hovered, pressed })}
			<Sprite
				key="buttonAuto"
				{...center}
				anchor={0.5}
				width={size(165)}
				height={size(165)}
				alpha={autoDisabled ? 0.45 : pressed ? 0.84 : hovered || stateBetDerived.hasAutoBetCounter() ? 1 : 0.95}
				blendMode={BLEND_MODE}
			/>
		{/snippet}
	</Button>

	<Button
		x={px(1310)}
		y={py(435)}
		anchor={0.5}
		sizes={{ width: size(165), height: size(165) }}
		onpress={pressBuy}
		disabled={buyDisabled}
	>
		{#snippet children({ center, hovered, pressed })}
			<Sprite
				key="buttonBuy"
				{...center}
				anchor={0.5}
				width={size(165)}
				height={size(165)}
				alpha={buyDisabled ? 0.45 : pressed ? 0.84 : hovered || stateBetDerived.activeBetMode()?.type === 'activate' ? 1 : 0.95}
				blendMode={BLEND_MODE}
			/>
		{/snippet}
	</Button>

	<Button
		x={px(606)}
		y={py(676)}
		anchor={0.5}
		sizes={{ width: size(130), height: size(120) }}
		onpress={pressDecrease}
		disabled={decreaseDisabled}
	>
		{#snippet children({ center })}
			<Rectangle {...center} anchor={0.5} width={size(130)} height={size(120)} alpha={0.001} backgroundColor={0xffffff} />
		{/snippet}
	</Button>

	<Button
		x={px(1070)}
		y={py(676)}
		anchor={0.5}
		sizes={{ width: size(130), height: size(120) }}
		onpress={pressIncrease}
		disabled={increaseDisabled}
	>
		{#snippet children({ center })}
			<Rectangle {...center} anchor={0.5} width={size(130)} height={size(120)} alpha={0.001} backgroundColor={0xffffff} />
		{/snippet}
	</Button>
</MainContainer>
