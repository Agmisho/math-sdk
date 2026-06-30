// @ts-ignore
import adapter from '@sveltejs/adapter-static';
// @ts-ignore
import config from 'config-svelte';

const baseConfig = config();
const releaseBuildDir = process.env.THE_INHERITANCE_RELEASE_BUILD_DIR;
if (releaseBuildDir) {
	baseConfig.kit.adapter = adapter({
		pages: releaseBuildDir,
		assets: releaseBuildDir,
	});
}

export default baseConfig;
