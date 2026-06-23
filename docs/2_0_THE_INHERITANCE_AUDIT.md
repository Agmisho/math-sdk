# 2_0_THE_INHERITANCE Audit

This audit records the current local source of truth for The Inheritance before adding new feature mechanics. It intentionally avoids unrelated game folders and treats the local `games/2_0_The_Inheritance` and `web-sdk/apps/the-inheritance` implementations as canonical.

## A. Exact Project Paths

| Area | Path | Status |
| --- | --- | --- |
| Math game root | `games/2_0_The_Inheritance` | Present |
| Frontend game root | `web-sdk/apps/the-inheritance` | Present |
| Alternate frontend path | `web-sdk/apps/2_0_The_Inheritance` | Not present |
| Math symbol assets | `games/2_0_The_Inheritance/assets/symbols/png` | Present, multiplier PNGs only |
| Frontend asset root | `web-sdk/apps/the-inheritance/static/assets/the-inheritance` | Present |
| Frontend cleaned symbols | `web-sdk/apps/the-inheritance/static/assets/the-inheritance/symbols-cleaned` | Present |
| Reel-strip CSVs | `games/2_0_The_Inheritance/reels` | `BR0.csv`, `FR0.csv`, `FR100.csv`, `FRWCAP.csv` |
| Generated books | `games/2_0_The_Inheritance/library/publish_files` | `books_base.jsonl.zst`, `books_scatter_boost.jsonl.zst`, `books_bonus.jsonl.zst` |
| Generated configs | `games/2_0_The_Inheritance/library/configs` | Event configs, frontend config, math config |
| Lookup tables | `games/2_0_The_Inheritance/library/lookup_tables` and `library/publish_files` | Present for base, scatter boost, bonus |
| Force files | `games/2_0_The_Inheritance/library/forces` | Present |
| Math dev tests | `games/2_0_The_Inheritance/dev_*.py` | Present |
| Frontend Storybook | `web-sdk/apps/the-inheritance/src/stories` | Present |

Current commands:

| Purpose | Command |
| --- | --- |
| Math smoke test | `PYTHONPATH=. python games/2_0_The_Inheritance/dev_sdk_smoke_test.py` |
| Legacy Key test | `PYTHONPATH=. python games/2_0_The_Inheritance/dev_legacy_key_credit_test.py` |
| Multiplier test | `PYTHONPATH=. python games/2_0_The_Inheritance/dev_multiplier_test.py` |
| Full SDK generation | `PYTHONPATH=. python games/2_0_The_Inheritance/run.py` |
| Frontend build | `cd web-sdk && pnpm --filter the-inheritance build` |
| Frontend dev | `cd web-sdk && pnpm --filter the-inheritance dev -- --host 127.0.0.1 --port 3007` |

## B. Current Math SDK Architecture

| File / Folder | Role |
| --- | --- |
| `run.py` | SDK generation entrypoint. Runs simulations, config generation, forced event config additions, analysis, and format checks. |
| `game_config.py` | Canonical math configuration: game id, RTP target, win cap, dimensions, paytable, paylines, special symbols, reel loading, bet modes, distribution conditions, and Bonus Buy free-spin count. |
| `gamestate.py` | Concrete game state class inheriting the game-specific override. |
| `game_calculations.py` | Game-specific calculations layer currently extending shared `Executables`; no separate custom calculation body found. |
| `game_executables.py` | Current multiplier handling, Legacy Key collection, collection event emission, and line evaluation call using `Lines.get_lines(... multiplier_method="global")`. |
| `game_override.py` | Game-specific reset logic, special symbol property assignment, Legacy Key virtual scatter credit, free-spin trigger/retrigger overrides, and Bonus Buy 10-free-spin override. |
| `game_events.py` | Not present for this game. Custom events are emitted from `game_executables.py` and `game_override.py`. |
| `reels/` | Active and inactive reel CSVs. Active config loads `BR0`, `FR0`, and `FRWCAP` as `WCAP`. `FR100.csv` exists but is not loaded. |
| `library/configs/` | Generated event configs, verification JSON, frontend config, backend config, and math config. |
| `library/publish_files/` | Compressed books, lookup-table copies, and `index.json` mode manifest. |
| `library/lookup_tables/` | Lookup tables and segmented lookup tables for all current modes. |
| `library/forces/` | Force records and `force.json`. |
| `dev_sdk_smoke_test.py` | Lightweight architecture/smoke validation. |
| `dev_multiplier_test.py` | Natural Diamond Seal multiplier validation. |
| `dev_legacy_key_credit_test.py` | Legacy Key virtual scatter credit validation. |

## C. Current Frontend Architecture

| File / Folder | Role |
| --- | --- |
| `package.json` | SvelteKit app package for `the-inheritance`. |
| `src/routes/+page.svelte` | Route entry rendering the game. |
| `src/components/Game.svelte` | Main Pixi/Svelte game composition. |
| `src/game/context.ts` | Frontend context wiring for shared state and helpers. |
| `src/game/typesBookEvent.ts` | BookEvent union, including standard events and current custom collection/multiplier events. |
| `src/game/typesEmitterEvent.ts` | Emitter-event union composed from component event types. |
| `src/game/bookEventHandlerMap.ts` | Book event playback and UI/event-emitter integration. |
| `src/game/eventEmitter.ts` | Typed emitter instance. |
| `src/game/stateGame.svelte.ts` | Board/reel state, layout, explicit spin mode, free-spin state, Legacy Key frontend counter. |
| `src/game/stateInheritanceUi.svelte.ts` | Inheritance-specific modal state. |
| `src/game/config.ts` | Frontend mirror of core game config, paytable, paylines, padding reels, and bet-mode display config. |
| `src/game/assets.ts` | Asset key to image/spine/spritesheet mapping. |
| `src/components/Board*.svelte` | Board, frame, mask, and reel container components. |
| `src/components/Symbol*.svelte`, `ReelSymbol.svelte` | Symbol rendering and state presentation. |
| `src/components/InheritanceInfoModal.svelte` | Paytable/rules modal. |
| `src/components/InheritanceBuyModal.svelte` | Buy Bonus and Scatter Boost confirmation UI. |
| `src/components/InheritanceUi.svelte` | Pixi UI panel, buttons, bet, balance, spin, auto, buy, speed, volume. |
| `src/components/FreeSpin*.svelte` | Free-spin intro, counter, animation, and outro components. |
| `src/components/LegacyKeyCounter.svelte`, `LegacyFeatureUnlockedModal.svelte` | Legacy Key display and placeholder unlocked modal. |
| `src/stories/data` | Current Storybook book/event fixtures. |

## D. Canonical Symbol Registry

The canonical internal IDs are the IDs in `game_config.py`, reel CSVs, paytable, frontend config, and `assets.ts`. Player-facing names below are taken from current frontend labels/assets unless noted.

| Internal Symbol ID | Player-facing name | Current role | Paytable role | Special attributes | Asset file | Frontend component/renderer | Used in base | Used in feature | Existing multiplier behavior |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S` | Vault Scatter | Free-spin trigger | No paytable entry | `scatter` | `Vault Scatter.png` | `SymbolSprite.svelte` via `SYMBOL_INFO_MAP` | Yes, `BR0` | Yes, `FR0`; not in `FRWCAP` | None |
| `W` | Wild | Wild substitute | 3=`10`, 4=`20`, 5=`50` | `wild` | `Wild.png` | `SymbolSprite.svelte` | Yes | Yes | Multiplied by current global Diamond Seal if any |
| `M2` | Diamond Seal Multiplier 2 | Multiplier symbol | No line pay | `multiplier`, assigned `multiplier=2` | `Diamond Seal Multiplier 2.png` | `SymbolSprite.svelte`, `GlobalMultiplier.svelte` available | Yes | Yes | Highest visible Diamond Seal applies `2x` globally |
| `M5` | Diamond Seal Multiplier 5 | Multiplier symbol | No line pay | `multiplier`, assigned `multiplier=5` | `Diamond Seal Multiplier 5.png` | Same | Yes | Yes | Highest visible Diamond Seal applies `5x` globally |
| `M10` | Diamond Seal Multiplier 10 | Multiplier symbol | No line pay | `multiplier`, assigned `multiplier=10` | `Diamond Seal Multiplier 10.png` | Same | Yes | Yes | Highest visible Diamond Seal applies `10x` globally |
| `M20` | Diamond Seal Multiplier 20 | Multiplier symbol | No line pay | `multiplier`, assigned `multiplier=20` | `Diamond Seal Multiplier 20.png` | Same | Yes | Yes | Highest visible Diamond Seal applies `20x` globally |
| `M100` | Diamond Seal Multiplier 100 | Multiplier symbol | No line pay | `multiplier`, assigned `multiplier=100` | `Diamond Seal Multiplier 100.png` | Same | Yes | Yes | Highest visible Diamond Seal applies `100x` globally |
| `H1` | Heiress | High symbol | 3=`12`, 4=`25`, 5=`80` | None | `Heiress.png` | `SymbolSprite.svelte` | Yes | Yes | Multiplied by current global Diamond Seal if any |
| `H2` | Covered Portrait / Covered Portrait Mystery | High symbol; possible mystery identity by name only | 3=`10`, 4=`20`, 5=`60` | None found | `Covered Portrait Mystery.png` | `SymbolSprite.svelte` | Yes | Yes | No mystery transform currently found |
| `H3` | Treasure Chest | High symbol | 3=`8`, 4=`15`, 5=`45` | None | `Treasure Chest.png` | `SymbolSprite.svelte` | Yes | Yes | Multiplied by current global Diamond Seal if any |
| `H4` | Legacy Key | High symbol and collection symbol | 3=`6`, 4=`12`, 5=`35` | Collection role in game executables; frontend `special_properties: ['collection']` | `Legacy Key.png` | `SymbolSprite.svelte`, `LegacyKeyCounter.svelte` | Yes | Yes on strips, but collection only in base/scatter boost | Multiplied by current global Diamond Seal if line win |
| `H5` | Diamond Brooch | High symbol | 3=`5`, 4=`10`, 5=`25` | None | `Diamond Brooch.png` | `SymbolSprite.svelte` | Yes | Yes | Multiplied by current global Diamond Seal if any |
| `H6` | Antique Pocket Watch | High symbol | 3=`4`, 4=`8`, 5=`20` | None | `Antique Pocket Watch.png` | `SymbolSprite.svelte` | Yes | Yes | Multiplied by current global Diamond Seal if any |
| `H7` | Magnifying Glass | High symbol | 3=`3`, 4=`6`, 5=`15` | None | `Magnifying Glass.png` | `SymbolSprite.svelte` | Yes | Yes | Multiplied by current global Diamond Seal if any |
| `H8` | Will | High symbol | 3=`2`, 4=`5`, 5=`12` | None | `will.png` | `SymbolSprite.svelte` | Yes | Yes | Multiplied by current global Diamond Seal if any |
| `H9` | Old Letter | High symbol | 3=`1.5`, 4=`4`, 5=`10` | None | `Old Letter.png` | `SymbolSprite.svelte` | Yes | Yes | Multiplied by current global Diamond Seal if any |
| `L1` | A | Low symbol | 3=`0.5`, 4=`1`, 5=`5` | None | `A.png` | `SymbolSprite.svelte` | Yes | Yes | Multiplied by current global Diamond Seal if any |
| `L2` | K | Low symbol | 3=`0.4`, 4=`0.8`, 5=`4` | None | `K.png` | `SymbolSprite.svelte` | Yes | Yes | Multiplied by current global Diamond Seal if any |
| `L3` | Q | Low symbol | 3=`0.3`, 4=`0.7`, 5=`3` | None | `Q.png` | `SymbolSprite.svelte` | Yes | Yes | Multiplied by current global Diamond Seal if any |
| `L4` | J | Low symbol | Math 3=`0.3`, 4=`0.6`, 5=`2.5`; frontend currently 3=`0.25` | None | `J.png` | `SymbolSprite.svelte` | Yes | Yes | Frontend paytable mirror differs from math at 3-kind |
| `L5` | 10 | Low symbol | 3=`0.2`, 4=`0.5`, 5=`2` | None | `10.png` | `SymbolSprite.svelte` | Yes | Yes | Multiplied by current global Diamond Seal if any |
| `L6` | Family Crest | Low symbol | Math 3=`0.1`, 4=`0.4`, 5=`1.5`; frontend currently 3=`0.15` | None | `Family Crest Wild.png` | `SymbolSprite.svelte` | Yes | Yes | Asset filename says Wild, but math treats `L6` as a low paying symbol |

Alias notes:

- `Legacy Key`, `Golden Key`, and `Master Key` should resolve to canonical ID `H4` only if business copy chooses those names. Current code/assets use `Legacy Key`.
- `Vault`, `Mansion Vault`, `Secret Vault`, and `Vault Scatter` should resolve to canonical ID `S`. Current code/assets use `Vault Scatter`.
- `Covered Portrait`, `Covered Portrait Mystery`, and `Portrait Mystery` currently resolve to canonical ID `H2`; no actual mystery reveal behavior was found.
- `Family Crest Wild` is the current asset filename for canonical ID `L6`, but `L6` is not math Wild.

## E. Full Multiplier Inventory

Current multiplier source is exactly the five Diamond Seal symbols: `M2`, `M5`, `M10`, `M20`, and `M100`.

| Symbol ID | Name | Asset | Value | Base availability | Free-spin availability | Bonus-buy availability | Type | Trigger / assignment | Stacking rule | Event | Frontend display |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| `M2` | Diamond Seal Multiplier 2 | `Diamond Seal Multiplier 2.png` | 2 | Natural reel strip | Natural reel strip | Natural free-spin strip after buy | One-spin global multiplier | `assign_fixed_mult_property()` assigns symbol attribute; `get_landed_multiplier()` reads visible board | Highest visible Diamond Seal wins; no persistence | `multiplierUpdate` | Symbol itself plus available `GlobalMultiplier.svelte` |
| `M5` | Diamond Seal Multiplier 5 | `Diamond Seal Multiplier 5.png` | 5 | Natural reel strip | Natural reel strip | Natural free-spin strip after buy | Same | Same | Same | Same | Same |
| `M10` | Diamond Seal Multiplier 10 | `Diamond Seal Multiplier 10.png` | 10 | Natural reel strip | Natural reel strip | Natural free-spin strip after buy | Same | Same | Same | Same | Same |
| `M20` | Diamond Seal Multiplier 20 | `Diamond Seal Multiplier 20.png` | 20 | Natural reel strip | Natural reel strip | Natural free-spin strip after buy | Same | Same | Same | Same | Same |
| `M100` | Diamond Seal Multiplier 100 | `Diamond Seal Multiplier 100.png` | 100 | Natural reel strip | Natural reel strip | Natural free-spin strip after buy | Same | Same | Same | Same | Same |

Multiplier strip counts:

| Strip | Reels x Stops | M2 | M5 | M10 | M20 | M100 | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `BR0.csv` | 5 x 80 | 1 | 1 | 1 | 1 | 1 | 5 |
| `FR0.csv` | 5 x 120 | 5 | 6 | 3 | 2 | 2 | 18 |
| `FRWCAP.csv` | 5 x 120 | 25 | 25 | 30 | 40 | 75 | 195 |
| `FR100.csv` | 5 x 30 | 0 | 0 | 0 | 0 | 1 | 1, but inactive |

Implementation facts:

- `special_symbol_functions` is assigned in `game_override.py`.
- `assign_fixed_mult_property()` assigns `multiplier` attributes to `M2`, `M5`, `M10`, `M20`, `M100`.
- `GameExecutables.get_landed_multiplier()` returns the highest visible multiplier value, or `1`.
- `GameExecutables.evaluate_lines_board()` calls `Lines.get_lines(... multiplier_method="global", global_multiplier=spin_multiplier)`.
- `src/wins/multiplier_strategy.py` supports `global`, `symbol`, and `combined`, but The Inheritance currently uses `global`.
- `win_data.meta` contains `lineIndex`, `multiplier`, `winWithoutMult`, `globalMult`, and `lineMultiplier`.
- No reel multiplier, persistent multiplier, sticky multiplier, collector multiplier, or feature-total multiplier was found.
- Existing tests: `games/2_0_The_Inheritance/dev_multiplier_test.py`.
- Existing Storybook data includes multiplier-bearing books/events, but generated story data may be stale relative to current math.

## F. Existing Features And Game Modes

| Mode / Feature | Confirmed behavior |
| --- | --- |
| Base mode `base` | Cost `1x`, uses `BR0` in basegame, can trigger free spins, can collect Legacy Keys. |
| Scatter Boost `scatter_boost` | Math cost `3x`, uses same strips with higher freegame distribution quota (`0.108` vs `0.100`); frontend currently displays/configures `2x`. |
| Bonus Buy `bonus` | Cost `100x`, `is_buybonus=True`, force-freegame distribution. Current math override awards exactly `10` bought free spins. |
| Boot / initial board | Frontend-only `INITIAL_BOARD`; no debit or math result. |
| Free spins | Triggered from base/scatter boost/bonus. Uses `FR0`; wincap can use `FR0` and `FRWCAP`. |
| Free-spin retrigger | Natural freegame scatters: 2 => +3, 3 => +5, 4 => +8, 5 => +12. |
| Legacy Key collection | `H4` visible symbols collect in `basegame` when betmode is not `bonus`; target is 10 in math. |
| Legacy virtual scatter credit | When starting an eligible paid spin with 10 keys, exactly 2 natural scatters can become 3 effective scatters; collection resets after use. |
| Mystery mode | No implemented mystery reveal found despite `H2` asset/name. |
| Respin / hold-and-spin / showdown | Not found in current math. |
| Sticky Wilds | Not found in current math. |
| Max-win forcing | `wincap` distribution with `FRWCAP` support and win cap `5000x`. |

## G. Current Mathematical Baseline

See `docs/2_0_THE_INHERITANCE_BASELINE.md` for the captured baseline. Important audit note: generated library stats currently report values that do not cleanly align with the `0.97` target and should be regenerated/reviewed before economics certification.

## Known Gaps Before New Feature Work

- Frontend config has `scatter_boost.cost = 2.0`; math config and generated publish index have `scatter_boost.cost = 3.0`.
- Frontend paytable mirror differs from math for `L4` 3-kind and `L6` 3-kind.
- Current math has no Vault Reel expansion, sticky Wild free-spin mode, collection respin/showdown, or deterministic portrait mystery reveal.
- Existing generated books/configs were created before the latest confirmed Bonus Buy 10-free-spin override unless regenerated after commit `10f0c79`.
- `FR100.csv` exists but is not active in `game_config.py`.
- No `game_events.py` exists for this game; new event work should either add it intentionally or continue the current custom event pattern deliberately.

