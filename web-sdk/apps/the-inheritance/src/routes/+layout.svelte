<script lang="ts">
	import { type Snippet } from 'svelte';
	import { GlobalStyle } from 'components-ui-html';
	import { LoaderStakeEngine, LoadI18n } from 'components-shared';
	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';

	import messagesMap from '../i18n/messagesMap';

	type Props = { children: Snippet };

	const props: Props = $props();
	// Stake Engine serves a game beneath its front-end file namespace. A relative
	// URL keeps this loader inside the uploaded game folder instead of requesting
	// the Stake Engine website root.
	const loaderUrlStakeEngine = './stake-engine-loader.gif';

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
