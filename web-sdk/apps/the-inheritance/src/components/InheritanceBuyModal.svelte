<script lang="ts">
	import { Popup } from 'components-shared';
	import { stateBet } from 'state-shared';

	import { getContext } from '../game/context';
	import { stateInheritanceUi } from '../game/stateInheritanceUi.svelte';

	const context = getContext();
	const BASE_MODE_KEY = 'BASE';
	const BONUS_MODE_KEY = 'BONUS';
	const SCATTER_BOOST_MODE_KEY = 'SCATTER_BOOST';
	const BUY_BONUS_MULTIPLIER = 100;
	const SCATTER_BOOST_MULTIPLIER = 2;

	const close = () => (stateInheritanceUi.modal = null);
	const formatMoney = (value: number) =>
		`$${Number(value || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
	const featureCost = (multiplier: number) => stateBet.betAmount * multiplier;
	const canAfford = (multiplier: number) => stateBet.balanceAmount <= 0 || stateBet.balanceAmount >= featureCost(multiplier);
	const isScatterBoostActive = () => stateBet.activeBetModeKey.toUpperCase() === SCATTER_BOOST_MODE_KEY;

	const activateScatterBoost = () => {
		stateBet.activeBetModeKey = SCATTER_BOOST_MODE_KEY;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		close();
	};

	const deactivateScatterBoost = () => {
		stateBet.activeBetModeKey = BASE_MODE_KEY;
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		close();
	};

	const buyBonus = () => {
		stateBet.activeBetModeKey = BONUS_MODE_KEY;
		context.eventEmitter.broadcast({ type: 'soundPressBet' });
		close();
		context.eventEmitter.broadcast({ type: 'bet' });
	};
</script>

{#if stateInheritanceUi.modal === 'buy'}
	<Popup zIndex={1000} onclose={close}>
		<section class="inheritance-modal" role="dialog" aria-modal="true" aria-label="Buy features">
			<header>
				<p>THE INHERITANCE</p>
				<h2>Buy Feature</h2>
			</header>

			<div class="feature-grid">
				<article class="feature-card">
					<div>
						<h3>Buy Bonus</h3>
						<p>Start 10 free spins immediately.</p>
						<strong>{formatMoney(featureCost(BUY_BONUS_MULTIPLIER))}</strong>
						<span>{BUY_BONUS_MULTIPLIER}x current bet</span>
					</div>
					<button onclick={buyBonus} disabled={!canAfford(BUY_BONUS_MULTIPLIER)}>Buy</button>
				</article>

				<article class="feature-card">
					<div>
						<h3>Scatter Boost</h3>
						<p>Increase the chance of landing a scatter/free-spin trigger on reel spins.</p>
						<strong>{formatMoney(featureCost(SCATTER_BOOST_MULTIPLIER))}</strong>
						<span>{SCATTER_BOOST_MULTIPLIER}x current bet per spin</span>
					</div>
					{#if isScatterBoostActive()}
						<button class="secondary" onclick={deactivateScatterBoost}>Disable</button>
					{:else}
						<button onclick={activateScatterBoost} disabled={!canAfford(SCATTER_BOOST_MULTIPLIER)}>Activate</button>
					{/if}
				</article>
			</div>
		</section>
	</Popup>
{/if}

<style lang="scss">
	.inheritance-modal {
		position: relative;
		z-index: 100;
		width: min(760px, calc(100vw - 2rem));
		max-height: calc(100vh - 5rem);
		overflow: auto;
		padding: 1.4rem;
		border: 1px solid rgba(255, 226, 146, 0.72);
		background: linear-gradient(180deg, rgba(11, 31, 20, 0.98), rgba(5, 10, 8, 0.98));
		box-shadow: 0 22px 70px rgba(0, 0, 0, 0.55), inset 0 0 34px rgba(192, 142, 48, 0.18);
		color: #f8e4ad;
		font-family: Georgia, 'Times New Roman', serif;
	}

	header {
		text-align: center;
		margin-bottom: 1rem;
	}

	header p {
		margin: 0 0 0.25rem;
		color: #6ee0a4;
		font-size: 0.72rem;
		font-weight: 800;
		letter-spacing: 0.12em;
	}

	h2 {
		margin: 0;
		font-size: clamp(1.35rem, 4vw, 2rem);
		font-weight: 800;
	}

	.feature-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 1rem;
	}

	.feature-card {
		display: flex;
		min-height: 13rem;
		flex-direction: column;
		justify-content: space-between;
		gap: 1rem;
		padding: 1rem;
		border: 1px solid rgba(255, 226, 146, 0.48);
		background: rgba(4, 24, 14, 0.76);
	}

	h3 {
		margin: 0 0 0.6rem;
		font-size: 1.1rem;
		color: #fff3bd;
	}

	p {
		margin: 0 0 0.9rem;
		min-height: 3.2rem;
		font-size: 0.9rem;
		line-height: 1.35;
		color: rgba(255, 244, 203, 0.9);
	}

	strong,
	span {
		display: block;
		text-align: center;
	}

	strong {
		font-size: 1.25rem;
		color: #ffffff;
	}

	span {
		margin-top: 0.25rem;
		font-size: 0.78rem;
		color: #72d99d;
	}

	button {
		width: 100%;
		min-height: 2.4rem;
		border: 2px solid rgba(255, 241, 185, 0.9);
		background: rgba(8, 48, 27, 0.9);
		color: #fff6c8;
		cursor: pointer;
		font-family: Georgia, 'Times New Roman', serif;
		font-size: 0.95rem;
		font-weight: 800;
		text-transform: uppercase;
	}

	button:hover:not(:disabled) {
		background: rgba(20, 91, 52, 0.95);
	}

	button.secondary {
		background: rgba(56, 30, 18, 0.9);
	}

	button:disabled {
		cursor: not-allowed;
		opacity: 0.42;
	}

	@media (max-width: 640px) {
		.inheritance-modal {
			padding: 1rem;
		}

		.feature-grid {
			grid-template-columns: 1fr;
		}

		.feature-card {
			min-height: 0;
		}
	}
</style>
