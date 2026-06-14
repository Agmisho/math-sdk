import { createLayout } from 'utils-layout';

const ARTBOARD_RATIO = 1672 / 941;

export const { stateLayout, stateLayoutDerived } = createLayout({
	backgroundRatio: {
		normal: ARTBOARD_RATIO,
		portrait: ARTBOARD_RATIO,
	},
	mainSizesMap: {
		desktop: { width: 1672, height: 941 },
		tablet: { width: 1000, height: 1000 },
		landscape: { width: 1672, height: 941 },
		portrait: { width: 800, height: 1422 },
	},
});
