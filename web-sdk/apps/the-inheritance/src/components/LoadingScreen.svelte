<script lang="ts">
	import { Container, Rectangle, Sprite } from 'pixi-svelte';
	import { FadeContainer, LoadingProgress } from 'components-pixi';
	import { MainContainer } from 'components-layout';

	import { getContext } from '../game/context';
	import TransitionAnimation from './TransitionAnimation.svelte';
	import PressToContinue from './PressToContinue.svelte';

	type Props = {
		onloaded: () => void;
	};

	const props: Props = $props();
	const context = getContext();

	let loadingType = $state<'start' | 'transition'>('start');
	const layout = () => context.stateLayoutDerived.mainLayout();
	const loadingBarWidth = () => Math.min(540, layout().width * 0.34);
</script>

<!-- title artwork and loading progress -->
<FadeContainer show={loadingType === 'start'}>
	<MainContainer>
		<Sprite
			key="inheritanceLoader"
			anchor={0.5}
			x={layout().width * 0.5}
			y={layout().height * 0.5}
			width={layout().width}
			height={layout().height}
			zIndex={-2}
		/>
		<Rectangle
			x={0}
			y={0}
			width={layout().width}
			height={layout().height}
			backgroundColor={0x000000}
			backgroundAlpha={0.1}
			zIndex={-1}
		/>
		<Container
			x={layout().width * 0.5}
			y={layout().height * 0.82}
		>
			{#if !context.stateApp.loaded}
				<LoadingProgress width={loadingBarWidth()} height={22}>
					{#snippet background(sizes)}
						<Rectangle
							{...sizes}
							borderRadius={11}
							backgroundColor={0x020c08}
							backgroundAlpha={0.95}
						/>
					{/snippet}
					{#snippet progress(sizes)}
						<Rectangle
							{...sizes}
							borderRadius={11}
							backgroundColor={0x2f9a61}
							backgroundAlpha={0.95}
						/>
					{/snippet}
					{#snippet frame(sizes)}
						<Rectangle
							{...sizes}
							borderRadius={11}
							backgroundColor={0x000000}
							backgroundAlpha={0}
							borderColor={0xd6ad58}
							borderWidth={3}
							borderAlpha={0.95}
						/>
					{/snippet}
				</LoadingProgress>
			{/if}
		</Container>
	</MainContainer>
</FadeContainer>

<!-- press to continue -->
<FadeContainer show={loadingType === 'start' && context.stateApp.loaded}>
	<PressToContinue onpress={() => (loadingType = 'transition')} />
</FadeContainer>

<!-- transition between the loading screen and the game -->
<FadeContainer show={loadingType === 'transition'}>
	<TransitionAnimation oncomplete={props.onloaded} />
</FadeContainer>
