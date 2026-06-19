<script lang="ts">
	import { onMount } from 'svelte';

	import type { LoadedAudio } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { sound, type SoundName } from '../game/sound';

	const context = getContext();

	onMount(() => {
		try {
			const loadedAudio = $state.snapshot(
				context.stateApp.loadedAssets['sound'],
			) as LoadedAudio<SoundName> | undefined;

			if (!loadedAudio) return;

			const { destroy } = sound.load(loadedAudio);

			return () => {
				// Equivalent to onDestroy(); Leave this comment for searching.
				destroy();
			};
		} catch (error) {
			console.warn('Sound loading disabled because audio assets are unavailable.', error);
		}
	});

	try {
		sound.enableEffect();
		sound.volumeEffect();
	} catch (error) {
		console.warn('Sound controls disabled because audio assets are unavailable.', error);
	}
</script>
