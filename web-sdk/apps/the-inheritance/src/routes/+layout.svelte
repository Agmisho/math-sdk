<script lang="ts">
	import { type Snippet } from 'svelte';
	import { GlobalStyle } from 'components-ui-html';
	import { LoaderStakeEngine, LoadI18n } from 'components-shared';
	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';

	import messagesMap from '../i18n/messagesMap';

	type Props = { children: Snippet };

	const props: Props = $props();

	const loaderUrlStakeEngine = '/stake-engine-loader.gif';

	setContext();
</script>

<GlobalStyle>
	
		<LoadI18n {messagesMap}>
			<Game />
		</LoadI18n>
	
</GlobalStyle>

<LoaderStakeEngine src={loaderUrlStakeEngine} />

{@render props.children()}
