<script lang="ts">
	import { onMount } from 'svelte';

	import { EnablePixiExtension } from 'components-pixi';
	import { EnableHotkey } from 'components-shared';
	import { App, Text } from 'pixi-svelte';
	import { stateModal, stateUi } from 'state-shared';

	import { GameVersion, Modals } from 'components-ui-html';

	import { getContext } from '../game/context';
	import { stateMathSession } from '../game/stateMathSession.svelte';
	import EnableSound from './EnableSound.svelte';
	import EnableGameActor from './EnableGameActor.svelte';
	import TheInheritanceSession from './TheInheritanceSession.svelte';
	import ResumeBet from './ResumeBet.svelte';
	import Sound from './Sound.svelte';
	import Background from './Background.svelte';
	import LoadingScreen from './LoadingScreen.svelte';
	import BoardFrame from './BoardFrame.svelte';
	import Board from './Board.svelte';
	import Anticipations from './Anticipations.svelte';
	import Win from './Win.svelte';
	import FreeSpinIntro from './FreeSpinIntro.svelte';
	import FreeSpinCounter from './FreeSpinCounter.svelte';
	import FreeSpinOutro from './FreeSpinOutro.svelte';
	import Transition from './Transition.svelte';
	import InheritanceUi from './InheritanceUi.svelte';
	import InheritanceBuyModal from './InheritanceBuyModal.svelte';
	import InheritanceInfoModal from './InheritanceInfoModal.svelte';
	import LegacyFeatureUnlockedModal from './LegacyFeatureUnlockedModal.svelte';
	import GlobalMultiplier from './GlobalMultiplier.svelte';

	const context = getContext();

	onMount(() => (context.stateLayout.showLoadingScreen = true));

	context.eventEmitter.subscribeOnMount({
		buyBonusConfirm: () => {
			stateModal.modal = { name: 'buyBonusConfirm' };
		},
	});
</script>

<App>
	<EnableSound />
	<EnableHotkey />
	<TheInheritanceSession />
	{#if stateMathSession.status === 'ready'}
		<EnableGameActor />
	{/if}
	<EnablePixiExtension />

	<Background />
	{#if stateMathSession.config?.developmentOnly}
		<Text
			text={`DEV MATH ${stateMathSession.config.profile} (${stateMathSession.config.rtp}%)`}
			x={12}
			y={10}
			style={{ fontFamily: 'Arial', fontSize: 12, fill: 0xffe6a2, fontWeight: '700' }}
			zIndex={90}
		/>
	{/if}
	{#if stateUi.config.mode === 'replay'}
		<Text
			text="REPLAY - NO BET"
			x={12}
			y={28}
			style={{ fontFamily: 'Arial', fontSize: 12, fill: 0xffffff, fontWeight: '700' }}
			zIndex={90}
		/>
	{/if}
	{#if stateMathSession.status === 'blocked'}
		<Text
			text="Math package mismatch. Check local RGS RTP settings."
			anchor={0.5}
			x={context.stateLayoutDerived.canvasSizes().width / 2}
			y={context.stateLayoutDerived.canvasSizes().height / 2}
			style={{ fontFamily: 'Georgia', fontSize: 24, fill: 0xffe6a2, fontWeight: '700', align: 'center' }}
			zIndex={91}
		/>
	{/if}

	{#if context.stateLayout.showLoadingScreen}
		<LoadingScreen onloaded={() => (context.stateLayout.showLoadingScreen = false)} />
	{:else}
		<ResumeBet />
		<Sound />

		<BoardFrame />
		<Board />
		<Anticipations />
		<GlobalMultiplier />

		<InheritanceUi />
		<Win />
		<FreeSpinIntro />
		<FreeSpinCounter />
		<FreeSpinOutro />
		<Transition />
	{/if}
</App>

<Modals>
	{#snippet version()}
		<GameVersion version="0.0.0" />
	{/snippet}
</Modals>
<InheritanceBuyModal />
<InheritanceInfoModal />
<LegacyFeatureUnlockedModal />
