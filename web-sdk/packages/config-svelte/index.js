import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const isTheInheritanceApp = process.cwd().replaceAll('\\', '/').endsWith('/apps/the-inheritance');
const releaseBuildDir = isTheInheritanceApp
	? process.env.THE_INHERITANCE_RELEASE_BUILD_DIR
	: undefined;

/** @type {import('@sveltejs/kit').Config} */
export default () => ({
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: vitePreprocess(),
	kit: {
		// See https://kit.svelte.dev/docs/adapters for more information about adapters.
		adapter: adapter(
			releaseBuildDir
				? {
						pages: releaseBuildDir,
						assets: releaseBuildDir,
					}
				: undefined,
		),
		output: {
			bundleStrategy: 'inline',
		},
	},
});
