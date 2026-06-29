<script lang="ts" module>
	export type EmitterEventLegacyKeyCounter =
		| {
				type: 'collectionUpdate';
				collected?: number;
				target?: number;
				positions?: unknown[];
				gameType?: string;
			}
		| {
				type: 'legacyScatterCredit';
				used?: boolean;
				collected?: number;
				target?: number;
			};
</script>

<script lang="ts">
	import { MainContainer } from 'components-layout';
	import { Sprite, Text, REM } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();
	const ARTBOARD = { width: 1672, height: 941 };
	const TOTAL_KEYS = 10;
	const keySlots = Array.from({ length: TOTAL_KEYS }, (_, index) => index);

	let collectedKeys = $state(0);

	const px = (value: number) => context.stateLayoutDerived.mainLayout().width * (value / ARTBOARD.width);
	const py = (value: number) => context.stateLayoutDerived.mainLayout().height * (value / ARTBOARD.height);
	const size = (value: number) => context.stateLayoutDerived.mainLayout().width * (value / ARTBOARD.width);

	const counterX = (index: number) => px(440 + index * 88);
	const counterY = py(72);
	const keySize = size(78);

	const textStyle = {
		fontFamily: 'proxima-nova',
		fontSize: REM * 0.95,
		fontWeight: '800',
		fill: 0xfff0a8,
		stroke: { color: 0x000000, width: 4 },
	};

	context.eventEmitter.subscribeOnMount({
		collectionUpdate: ({ collected }) => {
			collectedKeys = Math.max(0, Math.min(TOTAL_KEYS, collected ?? 0));
		},
	});
</script>

<MainContainer>
	{#each keySlots as keySlot}
		<Sprite
			key="H4"
			anchor={0.5}
			x={counterX(keySlot)}
			y={counterY}
			width={keySize}
			height={keySize}
			alpha={keySlot < collectedKeys ? 1 : 0.22}
			rotation={-0.35}
			zIndex={18}
		/>
	{/each}

	<Text
		anchor={0.5}
		x={px(1278)}
		y={py(72)}
		text={`${collectedKeys}/${TOTAL_KEYS}`}
		style={textStyle}
		zIndex={19}
	/>
</MainContainer>
