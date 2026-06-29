<script lang="ts" module>
	import { sound, type MusicName, type SoundEffectName, type SoundName } from '../game/sound';

	export type EmitterEventSound =
		| { type: 'soundMusic'; name: MusicName }
		| { type: 'soundOnce'; name: SoundEffectName; forcePlay?: boolean }
		| { type: 'soundLoop'; name: SoundEffectName }
		| { type: 'soundStop'; name: SoundName }
		| { type: 'soundFade'; name: SoundName; from: number; to: number; duration: number }
		| { type: 'soundScatterCounterIncrease' }
		| { type: 'soundScatterCounterClear' };
</script>

<script lang="ts">
	import { onMount } from 'svelte';

	import { waitForTimeout } from 'utils-shared/wait';
	import { SECOND } from 'constants-shared/time';
	import { stateBet, stateSoundDerived } from 'state-shared';

	import { getContext } from '../game/context';

	const context = getContext();
	const CUSTOM_AUDIO = {
		main: '/assets/the-inheritance/audio/main-theme.mp3',
		spin: '/assets/the-inheritance/audio/spin.mp3',
		scatter: '/assets/the-inheritance/audio/scatter-landing.mp3',
	};
	const CUSTOM_MUSIC_VOLUME = 0.46;
	const CUSTOM_SPIN_VOLUME = 0.22;
	const CUSTOM_SCATTER_VOLUME = 0.82;
	const CUSTOM_SCATTER_SOUNDS = new Set<SoundEffectName>([
		'sfx_scatter_reveal',
		'sfx_scatter_stop_1',
		'sfx_scatter_stop_2',
		'sfx_scatter_stop_3',
		'sfx_scatter_stop_4',
		'sfx_scatter_stop_5',
	]);
	type AudioChannel = {
		src: string;
		preload: string;
		loop: boolean;
		volume: number;
		currentTime: number;
		play: () => Promise<void>;
		pause: () => void;
	};

	let mainMusic = $state<AudioChannel | null>(null);
	let spinSound = $state<AudioChannel | null>(null);
	let scatterSound = $state<AudioChannel | null>(null);

	const createAudio = (src: string, options: { loop?: boolean } = {}) => {
		if (typeof document === 'undefined') return null;
		const audio = document.createElement('audio') as AudioChannel;
		audio.src = src;
		audio.preload = 'auto';
		audio.loop = options.loop ?? false;
		audio.volume = 0;
		return audio;
	};

	const playAudio = (audio: AudioChannel | null) => {
		if (!audio) return;
		audio.currentTime = 0;
		void audio.play().catch((error) => {
			console.warn('Custom The Inheritance audio could not play.', error);
		});
	};

	const playMusic = (name: MusicName) => {
		if (name === 'bgm_main') {
			void mainMusic?.play().catch((error) => {
				console.warn('The Inheritance background music could not play.', error);
			});
			return;
		}
		sound.players?.music?.play?.({ name });
	};
	const playOnce = (name: SoundEffectName, forcePlay?: boolean) => {
		if (name === 'sfx_btn_spin') {
			playAudio(spinSound);
			return;
		}
		if (CUSTOM_SCATTER_SOUNDS.has(name)) {
			playAudio(scatterSound);
			return;
		}
		sound.players?.once?.play?.({ name, forcePlay });
	};
	const playLoop = (name: SoundEffectName) => sound.players?.loop?.play?.({ name });

	$effect(() => {
		if (mainMusic) mainMusic.volume = stateSoundDerived.volumeMusic() * CUSTOM_MUSIC_VOLUME;
		if (spinSound) spinSound.volume = stateSoundDerived.volumeSoundEffect() * CUSTOM_SPIN_VOLUME;
		if (scatterSound) scatterSound.volume = stateSoundDerived.volumeSoundEffect() * CUSTOM_SCATTER_VOLUME;
	});

	context.eventEmitter.subscribeOnMount({
		// ui
		soundBetMode: async ({ betModeKey }) => {
			if (betModeKey === 'SUPERSPIN') {
				// check if SUPERSPIN, when changing the bet mode.
				playOnce('sfx_winlevel_end');
				await waitForTimeout(SECOND);
				playMusic('bgm_freespin');
			} else {
				playMusic('bgm_main');
			}
		},
		soundPressGeneral: () => playOnce('sfx_btn_general'),
		soundPressBet: () => playOnce('sfx_btn_spin'),
		// scatterCounter
		soundScatterCounterIncrease: () => (context.stateGame.scatterCounter = context.stateGame.scatterCounter + 1), // prettier-ignore
		soundScatterCounterClear: () => (context.stateGame.scatterCounter = 0),
		// game
		soundMusic: ({ name }) => playMusic(name),
		soundLoop: ({ name }) => playLoop(name),
		soundOnce: ({ name, forcePlay }) => playOnce(name, forcePlay),
		soundStop: ({ name }) => sound.stop?.({ name }),
		soundFade: async ({ name, duration, from, to }) => await sound.fade?.({ name, duration, from, to }), // prettier-ignore
	});

	onMount(() => {
		mainMusic = createAudio(CUSTOM_AUDIO.main, { loop: true });
		spinSound = createAudio(CUSTOM_AUDIO.spin);
		scatterSound = createAudio(CUSTOM_AUDIO.scatter);

		if (stateBet.activeBetModeKey === 'SUPERSPIN') {
			// check if SUPERSPIN, when resume bet and the bet is a super spin.
			playMusic('bgm_freespin');
		} else {
			playMusic('bgm_main');

			//How to control volume per soundfile(use fade)
			// sound.players.music.fade({ name: 'bgm_main', from: 0, to: 1, duration: 2000 });

			//How to control rate per soundfile
			// sound.players.music.rate({ rate: 2, name: 'bgm_main'}); // change play back rate(1: default, 0: slow, 1+ fasterm and higher pitch )
		}

		return () => {
			mainMusic?.pause();
			spinSound?.pause();
			scatterSound?.pause();
		};
	});
</script>
