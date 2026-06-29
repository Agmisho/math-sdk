<script lang="ts" module>
	export type EmitterEventFreeSpinCounter =
		| { type: 'freeSpinCounterShow' }
		| { type: 'freeSpinCounterHide' }
		| { type: 'freeSpinCounterUpdate'; current?: number; total?: number };
</script>

<script lang="ts">
	import { FadeContainer } from 'components-pixi';

	import { getContext } from '../game/context';
	import { anchorToPivot, BitmapText, Container, Sprite, type Sizes } from 'pixi-svelte';

	const context = getContext();
	const PANEL_KEY_DESKTOP = 'Frame_FSCounter.png';
	const PANEL_RATIO_DESKTOP = 824 / 622;
	const panelKey = PANEL_KEY_DESKTOP;
	const panelWidth = $derived(context.stateGameDerived.frameLayout().width * 0.15);
	const panelSizes = $derived({
		width: panelWidth,
		height: panelWidth / PANEL_RATIO_DESKTOP,
	});
	const scale = 1;
	const position = $derived.by(() => {
		const frame = context.stateGameDerived.frameLayout();
		const stacked = context.stateLayoutDerived.isStacked();
		if (stacked) {
			return {
				x: frame.grid.x + panelSizes.width * 0.55,
				y: Math.max(panelSizes.height * 0.65, frame.grid.y - panelSizes.height * 0.34),
			};
		}

		return {
			x: frame.grid.x - panelSizes.width * 0.7,
			y: frame.grid.y + panelSizes.height * 0.25,
		};
	});

	const fontSize = $derived(panelWidth * 0.14);

	let show = $state(false);
	let current = $state(0);
	let total = $state(0);
	let titleSizes: Sizes = $state({ width: 0, height: 0 });
	let counterSizes: Sizes = $state({ width: 0, height: 0 });

	const textContainerSizes = $derived({
		width: titleSizes.width,
		height: titleSizes.height + counterSizes.height,
	});
	const counterPosition = $derived({ x: titleSizes.width / 2, y: titleSizes.height });

	context.eventEmitter.subscribeOnMount({
		freeSpinCounterShow: () => (show = true),
		freeSpinCounterHide: () => (show = false),
		freeSpinCounterUpdate: (emitterEvent) => {
			if (emitterEvent.current !== undefined) current = emitterEvent.current;
			if (emitterEvent.total !== undefined) total = emitterEvent.total;
		},
	});
</script>

<FadeContainer {show} {...position} {scale}>
	<Sprite key={panelKey} {...panelSizes} />
	<Container
		x={panelSizes.width * 0.5}
		y={panelSizes.height * 0.48}
		pivot={anchorToPivot({
			sizes: textContainerSizes,
			anchor: { x: 0.5, y: 0.5 },
		})}
	>
		<BitmapText
			text={'FREE SPIN'}
			style={{
				fontFamily: 'gold',
				fontSize,
				wordWrap: false,
			}}
			onresize={(sizes) => (titleSizes = sizes)}
		/>
		<BitmapText
			text={`${current} OF ${total}`}
			{...counterPosition}
			anchor={{ x: 0.5, y: 0 }}
			style={{
				fontFamily: 'gold',
				fontSize,
			}}
			onresize={(sizes) => (counterSizes = sizes)}
		/>
	</Container>
</FadeContainer>
