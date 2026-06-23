// @ts-ignore
import config from 'config-vite';

const workspacePackages = [
	'components-layout',
	'components-pixi',
	'components-shared',
	'components-ui-html',
	'components-ui-pixi',
	'constants-shared',
	'envs',
	'pixi-svelte',
	'rgs-fetcher',
	'rgs-requests',
	'state-shared',
	'utils-bet',
	'utils-book',
	'utils-event-emitter',
	'utils-fetcher',
	'utils-layout',
	'utils-shared',
	'utils-slots',
	'utils-sound',
	'utils-xstate',
];

export default () => {
	const baseConfig = config();

	return {
		...baseConfig,
		optimizeDeps: {
			...baseConfig.optimizeDeps,
			include: [
				...(baseConfig.optimizeDeps?.include ?? []),
				'@lingui/core',
				'@lingui/message-utils/compileMessage',
				'@messageformat/parser',
				'earcut',
				'eventemitter3',
				'howler',
				'lodash',
				'pixi.js',
				'resize-observer',
				'webfontloader',
			],
			exclude: [...(baseConfig.optimizeDeps?.exclude ?? []), ...workspacePackages],
		},
	};
};
