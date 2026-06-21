<script lang="ts">
	import { Popup } from 'components-shared';

	import config from '../game/config';
	import { stateInheritanceUi } from '../game/stateInheritanceUi.svelte';

	type PaytableEntry = Record<string, number>;
	type SymbolConfig = { paytable?: PaytableEntry[]; special_properties?: string[] };

	const rows = [0, 1, 2, 3, 4];
	const columns = [0, 1, 2, 3, 4];
	const symbolConfigs = config.symbols as Record<string, SymbolConfig>;
	const paylinePatterns = Object.entries(config.paylines).map(([id, pattern]) => ({ id, pattern }));
	const symbolOrder = ['W', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6'];
	const paytableSymbols = symbolOrder
		.map((name) => ({ name, data: symbolConfigs[name] }))
		.filter((symbol) => Boolean(symbol.data?.paytable));
	const specialSymbols = ['S', 'W', 'H4', 'M2', 'M5', 'M10', 'M20', 'M100'];

	const symbolLabels: Record<string, string> = {
		S: 'Vault Scatter',
		W: 'Wild',
		M2: '2x Multiplier',
		M5: '5x Multiplier',
		M10: '10x Multiplier',
		M20: '20x Multiplier',
		M100: '100x Multiplier',
		H1: 'Heiress',
		H2: 'Covered Portrait',
		H3: 'Treasure Chest',
		H4: 'Legacy Key',
		H5: 'Diamond Brooch',
		H6: 'Pocket Watch',
		H7: 'Magnifying Glass',
		H8: 'Will',
		H9: 'Old Letter',
		L1: 'A',
		L2: 'K',
		L3: 'Q',
		L4: 'J',
		L5: '10',
		L6: 'Family Crest',
	};

	const symbolFiles: Record<string, string> = {
		S: 'Vault Scatter.png',
		W: 'Wild.png',
		M2: 'Diamond Seal Multiplier 2.png',
		M5: 'Diamond Seal Multiplier 5.png',
		M10: 'Diamond Seal Multiplier 10.png',
		M20: 'Diamond Seal Multiplier 20.png',
		M100: 'Diamond Seal Multiplier 100.png',
		H1: 'Heiress.png',
		H2: 'Covered Portrait Mystery.png',
		H3: 'Treasure Chest.png',
		H4: 'Legacy Key.png',
		H5: 'Diamond Brooch.png',
		H6: 'Antique Pocket Watch.png',
		H7: 'Magnifying Glass.png',
		H8: 'will.png',
		H9: 'Old Letter.png',
		L1: 'A.png',
		L2: 'K.png',
		L3: 'Q.png',
		L4: 'J.png',
		L5: '10.png',
		L6: 'Family Crest Wild.png',
	};

	const close = () => (stateInheritanceUi.modal = null);
	const symbolAsset = (name: string) =>
		`/assets/the-inheritance/symbols-cleaned/${symbolFiles[name].split('/').map(encodeURIComponent).join('/')}`;
	const payFor = (data: SymbolConfig, kind: '3' | '4' | '5') =>
		data.paytable?.find((entry) => entry[kind] !== undefined)?.[kind];
	const formatMultiplier = (value?: number) => (value === undefined ? '-' : `${value}x`);
</script>

{#if stateInheritanceUi.modal === 'info'}
	<Popup zIndex={1000} onclose={close}>
		<section class="inheritance-info" role="dialog" aria-modal="true" aria-label="The Inheritance rules and paytable">
			<header>
				<p>THE INHERITANCE</p>
				<h2>Rules & Paytable</h2>
			</header>

			<div class="rule-summary">
				<div><strong>RTP</strong><span>{(config.rtp * 100).toFixed(2)}%</span></div>
				<div><strong>Max Win</strong><span>{config.betModes.base.max_win}x</span></div>
				<div><strong>Rows</strong><span>5x5</span></div>
				<div><strong>Lines</strong><span>{paylinePatterns.length}</span></div>
			</div>

			<section class="info-section">
				<h3>Paylines</h3>
				<div class="paylines">
					{#each paylinePatterns as payline}
						<article class="payline-card" aria-label={`Payline ${payline.id}`}>
							<span>{payline.id}</span>
							<div class="payline-grid">
								{#each rows as row}
									{#each columns as column}
										<i class:active={payline.pattern[column] === row}></i>
									{/each}
								{/each}
							</div>
						</article>
					{/each}
				</div>
			</section>

			<section class="info-section">
				<h3>Symbols Payout</h3>
				<table>
					<thead>
						<tr><th>Symbol</th><th>3</th><th>4</th><th>5</th></tr>
					</thead>
					<tbody>
						{#each paytableSymbols as symbol}
							<tr>
								<td>
									<img src={symbolAsset(symbol.name)} alt="" />
									<span>{symbolLabels[symbol.name]}</span>
								</td>
								<td>{formatMultiplier(payFor(symbol.data, '3'))}</td>
								<td>{formatMultiplier(payFor(symbol.data, '4'))}</td>
								<td>{formatMultiplier(payFor(symbol.data, '5'))}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</section>

			<section class="info-section">
				<h3>Special Symbols & Features</h3>
				<div class="special-grid">
					{#each specialSymbols as symbolName}
						<article>
							<img src={symbolAsset(symbolName)} alt="" />
							<div>
								<strong>{symbolLabels[symbolName]}</strong>
								{#if symbolName === 'S'}
									<p>Scatter symbol. Landing enough scatters awards the free-spin bonus.</p>
								{:else if symbolName === 'W'}
									<p>Wild symbol. Substitutes for regular paying symbols.</p>
								{:else if symbolName === 'H4'}
									<p>Legacy Key. Each landed key increases the key counter.</p>
								{:else}
									<p>Free-spin multiplier symbol with the displayed multiplier value.</p>
								{/if}
							</div>
						</article>
					{/each}
				</div>
			</section>

			<section class="info-section compact">
				<h3>Feature Costs</h3>
				<p>Buy Bonus costs 100x the selected bet and starts 10 free spins. Scatter Boost costs 2x the selected bet per spin and increases the scatter/free-spin trigger chance while active.</p>
				<p>All displayed wins are illustrative until confirmed and settled by the RGS. Malfunction voids all plays and payouts.</p>
			</section>
		</section>
	</Popup>
{/if}

<style lang="scss">
	.inheritance-info {
		position: relative;
		z-index: 100;
		width: min(1040px, calc(100vw - 2rem));
		max-height: calc(100vh - 5rem);
		overflow: auto;
		padding: 1.25rem;
		border: 1px solid rgba(255, 226, 146, 0.74);
		background: linear-gradient(180deg, rgba(8, 28, 17, 0.98), rgba(4, 9, 8, 0.98));
		box-shadow: 0 22px 70px rgba(0, 0, 0, 0.58), inset 0 0 34px rgba(192, 142, 48, 0.18);
		color: #f7e3ac;
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

	h2,
	h3 {
		margin: 0;
	}

	h2 {
		font-size: clamp(1.35rem, 4vw, 2rem);
		font-weight: 800;
	}

	h3 {
		margin-bottom: 0.75rem;
		font-size: 1rem;
		color: #fff2bb;
	}

	.rule-summary {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		gap: 0.65rem;
		margin-bottom: 1rem;
	}

	.rule-summary div,
	.info-section {
		border: 1px solid rgba(255, 226, 146, 0.35);
		background: rgba(4, 24, 14, 0.68);
	}

	.rule-summary div {
		padding: 0.65rem;
		text-align: center;
	}

	.rule-summary strong,
	.rule-summary span {
		display: block;
	}

	.rule-summary strong {
		font-size: 0.72rem;
		text-transform: uppercase;
		color: #74d99f;
	}

	.rule-summary span {
		margin-top: 0.2rem;
		font-size: 1.05rem;
		font-weight: 800;
	}

	.info-section {
		padding: 1rem;
		margin-bottom: 1rem;
	}

	.paylines {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(92px, 1fr));
		gap: 0.65rem;
	}

	.payline-card {
		display: grid;
		grid-template-columns: auto 1fr;
		align-items: center;
		gap: 0.45rem;
		font-size: 0.75rem;
	}

	.payline-card span {
		color: #74d99f;
		font-weight: 800;
	}

	.payline-grid {
		display: grid;
		grid-template-columns: repeat(5, 1fr);
		aspect-ratio: 1;
		border: 1px solid rgba(255, 255, 255, 0.8);
	}

	.payline-grid i {
		border-right: 1px solid rgba(255, 255, 255, 0.72);
		border-bottom: 1px solid rgba(255, 255, 255, 0.72);
		background: rgba(0, 0, 0, 0.42);
	}

	.payline-grid i:nth-child(5n) {
		border-right: 0;
	}

	.payline-grid i:nth-last-child(-n + 5) {
		border-bottom: 0;
	}

	.payline-grid i.active {
		background: #49b95a;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.9rem;
	}

	th,
	td {
		padding: 0.42rem;
		border-bottom: 1px solid rgba(255, 226, 146, 0.22);
		text-align: center;
	}

	th {
		color: #74d99f;
		text-transform: uppercase;
	}

	td:first-child {
		display: flex;
		align-items: center;
		gap: 0.55rem;
		text-align: left;
	}

	img {
		width: 2.35rem;
		height: 2.35rem;
		object-fit: contain;
	}

	.special-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
		gap: 0.75rem;
	}

	.special-grid article {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.55rem;
		background: rgba(0, 0, 0, 0.22);
	}

	.special-grid strong {
		display: block;
		color: #fff2bb;
	}

	.special-grid p,
	.compact p {
		margin: 0.25rem 0 0;
		font-size: 0.82rem;
		line-height: 1.35;
		color: rgba(255, 244, 203, 0.9);
	}

	.compact p + p {
		margin-top: 0.65rem;
	}

	@media (max-width: 760px) {
		.rule-summary {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}

		table {
			font-size: 0.78rem;
		}

		img {
			width: 2rem;
			height: 2rem;
		}
	}
</style>
