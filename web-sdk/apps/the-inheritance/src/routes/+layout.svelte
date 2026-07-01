<script lang="ts">
	import { type Snippet } from 'svelte';
	import { GlobalStyle } from 'components-ui-html';
	import { LoaderStakeEngine, LoadI18n } from 'components-shared';
	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';

	import messagesMap from '../i18n/messagesMap';

	type Props = { children: Snippet };

	const props: Props = $props();
	// Use the same Vite-resolved loader pattern as Stake Engine's sample games.
	// This emits a deployable URL inside the generated static frontend.
	const loaderUrlStakeEngine = new URL('../../stake-engine-loader.gif', import.meta.url).href;

	setContext();
</script>

<GlobalStyle>
	<LoadI18n {messagesMap}>
		<div data-testid="the-inheritance-app" data-game-id="2_0_The_Inheritance">
			<Game />
		</div>
	</LoadI18n>
</GlobalStyle>

<LoaderStakeEngine src={loaderUrlStakeEngine} />

{@render props.children()}
