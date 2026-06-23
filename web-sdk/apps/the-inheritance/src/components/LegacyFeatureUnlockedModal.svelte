<script lang="ts">
	import { Popup } from 'components-shared';

	import { stateInheritanceUi } from '../game/stateInheritanceUi.svelte';

	const close = () => (stateInheritanceUi.modal = null);
</script>

{#if stateInheritanceUi.modal === 'legacyFeatureUnlocked'}
	<Popup zIndex={1000} onclose={close}>
		<section class="legacy-unlocked" role="dialog" aria-modal="true" aria-label="Legacy Feature Unlocked">
			<p>THE INHERITANCE</p>
			<h2>Legacy Feature Unlocked</h2>
			<span>Full feature coming soon.</span>
			<button onclick={close}>Continue</button>
		</section>
	</Popup>
{/if}

<style lang="scss">
	.legacy-unlocked {
		position: relative;
		z-index: 100;
		width: min(520px, calc(100vw - 2rem));
		padding: 1.4rem;
		border: 1px solid rgba(255, 226, 146, 0.74);
		background: linear-gradient(180deg, rgba(8, 28, 17, 0.98), rgba(4, 9, 8, 0.98));
		box-shadow: 0 22px 70px rgba(0, 0, 0, 0.58), inset 0 0 34px rgba(192, 142, 48, 0.18);
		color: #f7e3ac;
		font-family: Georgia, 'Times New Roman', serif;
		text-align: center;
	}

	p {
		margin: 0 0 0.25rem;
		color: #6ee0a4;
		font-size: 0.72rem;
		font-weight: 800;
		letter-spacing: 0.12em;
	}

	h2 {
		margin: 0;
		font-size: clamp(1.45rem, 4vw, 2.25rem);
		font-weight: 800;
	}

	span {
		display: block;
		margin-top: 0.65rem;
		color: rgba(255, 244, 203, 0.9);
		font-size: 0.95rem;
	}

	button {
		min-width: 12rem;
		min-height: 2.45rem;
		margin-top: 1.25rem;
		border: 2px solid rgba(255, 241, 185, 0.9);
		background: rgba(8, 48, 27, 0.9);
		color: #fff6c8;
		cursor: pointer;
		font-family: Georgia, 'Times New Roman', serif;
		font-size: 0.95rem;
		font-weight: 800;
		text-transform: uppercase;
	}

	button:hover {
		background: rgba(20, 91, 52, 0.95);
	}
</style>
