<script lang="ts">
	import { Container, Rectangle, Sprite, Text } from 'pixi-svelte';
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
</script>

<!-- logo and loading progress -->
<FadeContainer show={loadingType === 'start'}>
	<MainContainer>
		<Container
			x={context.stateLayoutDerived.mainLayout().width * 0.5}
			y={context.stateLayoutDerived.mainLayout().height * 0.5}
		>
			<Sprite key="H4" anchor={0.5} y={-80} width={190} height={190} rotation={-0.28} />
			<Text
				text="THE INHERITANCE"
				anchor={0.5}
				y={75}
				style={{
					fontFamily: 'Georgia',
					fontSize: 54,
					fontWeight: '800',
					fill: 0xffe6a2,
					stroke: { color: 0x140b04, width: 7 },
					letterSpacing: 3,
				}}
			/>
			{#if !context.stateApp.loaded}
				<LoadingProgress y={155} width={420} height={22}>
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
