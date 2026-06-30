import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
export default () => ({
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: vitePreprocess(),
	kit: {
		// See https://kit.svelte.dev/docs/adapters for more information about adapters.
		adapter: adapter(
			process.env.THE_INHERITANCE_RELEASE_BUILD_DIR
				? {
						pages: process.env.THE_INHERITANCE_RELEASE_BUILD_DIR,
						assets: process.env.THE_INHERITANCE_RELEASE_BUILD_DIR,
					}
				: undefined,
		),
		output: {
			bundleStrategy: 'inline',
		},
	},
});
