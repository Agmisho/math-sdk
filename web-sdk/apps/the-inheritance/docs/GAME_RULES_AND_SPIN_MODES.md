# The Inheritance Game Rules And Spin Modes

This document maps the existing The Inheritance implementation before gameplay changes. It separates code-confirmed facts from gaps and business decisions so future work does not invent slot behavior that already exists in the math package.

## 1. Game Overview

### Confirmed From Code

- Game package: `games/2_0_The_Inheritance`.
- Frontend package: `web-sdk/apps/the-inheritance`.
- Game id: `2_0_The_Inheritance`.
- Game name: `The Inheritance`.
- Math RTP: `0.9700`.
- Max win / win cap: `5000x`.
- Grid: `5` reels by `5` visible rows.
- Win type: fixed paylines, not ways.
- Paylines: `15`.
- Base game type string: `basegame`.
- Free game type string: `freegame`.
- Math bet modes: `base`, `scatter_boost`, `bonus`.
- Publish library modes and costs are listed in `games/2_0_The_Inheritance/library/publish_files/index.json`.
- Frontend uses `Frame1.png`, the current frame layout, key panel, and bottom UI layout. This document does not move or redesign those assets.

### Not Found In Code

- No math spin mode named `boot`, `bootstrap`, `initial`, `startup`, or `demo` was found.

### Implemented After Phase 3

- Frontend game state now has explicit `spinMode: 'base' | 'boot' | 'bought' | 'free'`.
- Frontend game state now tracks `freeSpinsRemaining`, `freeSpinsAwarded`, `freeSpinsTotalWin`, and `isBonusBuy`.
- Math config now defines `bonus_buy_free_spins = 10`, and the math override uses that value for bought basegame triggers.

### Needs Business Decision

- The math Legacy Key target is `10`; the current frontend placeholder target is `20`.
- The math `scatter_boost` cost is `3x`; current frontend copy/config says `2x`.
- Normal base trigger awards remain `3 scatters = 8`, `4 scatters = 12`, `5 scatters = 15`; Bonus Buy now overrides the initial award to exactly `10`.

## 2. Exact Spin-Mode Table

| Mode | Trigger | Debit | Reel / Symbol Rules | Feature Rules | Result | Next State |
| --- | --- | --- | --- | --- | --- | --- |
| Base Spin | Player spin using math mode `base`; frontend mode key usually `BASE` | Config cost `1.0x` underlying bet | Base reveal uses `BR0.csv`; free spins use `FR0.csv`; wincap free spins can weight `FR0` and `FRWCAP` | Can trigger Free Spins with effective scatter count `3`, `4`, or `5`; can collect Legacy Keys in basegame; Legacy scatter credit can apply | Pays line wins, can enter Free Spins, emits final win | Returns to `basegame` unless Free Spins are triggered |
| Scatter Boost Spin | Player activates `scatter_boost`; frontend mode key currently `SCATTER_BOOST` | Math cost `3.0x`; frontend currently says `2.0x` | Same active reel strips as base (`BR0` for basegame, `FR0` for freegame); distribution quota raises forced-freegame selection from `0.100` to `0.108` | Can trigger Free Spins; can collect Legacy Keys; Legacy scatter credit can apply | Same result types as base, with higher free-game distribution quota | Remains in basegame after result unless Free Spins are triggered |
| Boot / Initial Board | Frontend creates `INITIAL_BOARD` in `web-sdk/apps/the-inheritance/src/game/constants.ts` before the first paid result | No debit found | Static frontend display board only; not a math spin | Should not trigger Free Spins or collect Legacy Keys | Shows initial symbols only | First real spin is a paid mode |
| Bought Spin / Bonus Buy | Player chooses buy mode `bonus`; frontend key currently `BONUS` | Config cost `100.0x` underlying bet | Initial trigger reveal uses `BR0` with forced scatter count; Free Spins use `FR0`, or `FR0` plus `FRWCAP` for wincap condition | Math now awards exactly `10` initial free spins through `bonus_buy_free_spins`; Legacy Key collection is blocked in `bonus` | Enters Free Spins immediately after the forced trigger reveal | Free Spins, then basegame |
| Free Spin | Started by `run_freespin_from_base()` after base/scatter boost/buy trigger | No additional debit in math | Uses `FR0`; wincap condition can select `FR0` or `FRWCAP` with weights `{FR0: 1, WCAP: 8}` | Can retrigger on natural scatters: `2 -> 3`, `3 -> 5`, `4 -> 8`, `5 -> 12`; Legacy Keys are not collected in freegame | Accumulates freegame wins and emits `freeSpinEnd` | Returns to `basegame` after all free spins are complete |

## 3. Base Spin Flow

### Confirmed From Code

1. `GameState.run_spin()` resets the seed and loops until criteria are satisfied.
2. Each attempt calls `reset_book()`, `draw_board()`, `update_collection_state()`, `evaluate_lines_board()`, `check_fs_condition()`, `evaluate_finalwin()`, and `check_repeat()`.
3. `draw_board()` uses distribution conditions from the selected bet mode.
4. If `force_freegame` is false in basegame, `draw_board()` redraws natural base boards while the visible scatter count is at least the base trigger threshold (`3`).
5. If `force_freegame` is true in basegame, `draw_board()` calls `force_special_board("scatter", num_scatters)` where `num_scatters` is selected from `scatter_triggers`.
6. Base mode distributions:
   - `wincap`: quota `0.001`
   - `freegame`: quota `0.100`
   - `0`: quota `0.400`
   - `basegame`: quota `0.499`
7. Free-spin trigger awards in basegame:
   - `3` scatters: `8` free spins
   - `4` scatters: `12` free spins
   - `5` scatters: `15` free spins

### Source Files

- `games/2_0_The_Inheritance/gamestate.py`
- `games/2_0_The_Inheritance/game_config.py`
- `games/2_0_The_Inheritance/game_override.py`
- `src/calculations/board.py`
- `src/calculations/statistics.py`

## 4. Boot Spin Flow

### Confirmed From Code

- The frontend has an `INITIAL_BOARD` constant with 5 reels and 7 symbols per reel, where the visible board is `INITIAL_BOARD[reel].length - 2`, giving 5 visible rows plus padding.
- This board is used for frontend reel initialization. It is not a math package spin mode.
- There is no debit, no `reveal` event from math, no `finalWin`, and no backend round for this board.

### Not Found In Code

- No implementation named `boot spin`, `bootstrap spin`, `initial spin`, or `startup spin`.
- No code that should credit or debit the player from the opening board.

### Source Files

- `web-sdk/apps/the-inheritance/src/game/constants.ts`
- `web-sdk/apps/the-inheritance/src/game/stateGame.svelte.ts`

## 5. Bought Spin / Bonus Buy Flow

### Confirmed From Code

- Math bet mode name: `bonus`.
- Publish-library mode name: `bonus`.
- Frontend mode key: `BONUS`.
- Cost: `100.0x` underlying bet in math config and publish index.
- `is_buybonus=True` in math config.
- Bonus mode distributions:
  - `wincap`: quota `0.001`
  - `freegame`: quota `0.999`
- Bonus mode uses the same `freegame_condition` structure as base forced freegame:
  - basegame reel weights: `{BR0: 1}`
  - freegame reel weights: `{FR0: 1}`
  - scatter trigger weights: `{3: 50, 4: 20, 5: 5}`
  - `force_freegame: True`
- Math now forces a free-spin trigger and overrides the initial Bonus Buy award to `bonus_buy_free_spins = 10`.
- Legacy Key collection is blocked when `self.betmode == "bonus"`.

### Current Frontend And Local Behavior

- `InheritanceBuyModal.svelte` blocks confirmation if `stateBet.balanceAmount < stateBet.betAmount * gameConfig.betModes.bonus.cost`.
- On confirmation, `InheritanceBuyModal.svelte` calls `stateGameDerived.startBonusBuy()`, sets `stateBet.activeBetModeKey = 'BONUS'`, closes the modal, and broadcasts `{ type: 'bet' }`.
- The shared xstate request path sends `mode: stateBet.activeBetModeKey` to `requestBet()`.
- `InheritanceUi.svelte` avoids starting a buy mode from the normal Spin button by resetting active buy mode back to `BASE` before broadcasting a normal bet.
- The current local mock in `web-sdk/packages/rgs-requests/src/rgs-requests.ts` deducts the `100x` buy price once, emits exactly `10` free-spin updates for Bonus Buy, evaluates line wins from the documented paytable/paylines, and credits the total free-spin payout.

### Implemented Phase 3 Delta

- Bonus Buy deducts the configured `100x` buy amount once.
- Bonus Buy starts in explicit frontend mode `bought`.
- Bonus Buy transitions into explicit frontend mode `free`.
- The initial Bonus Buy award is exactly `10` free spins in math, frontend state, and local no-backend responses.
- Free Spins do not send additional paid requests; free-spin payouts are accumulated in `freeSpinsTotalWin`.
- At `freeSpinEnd`, the frontend returns to base state and clears `isBonusBuy`.

### Source Files

- `games/2_0_The_Inheritance/game_config.py`
- `games/2_0_The_Inheritance/game_override.py`
- `games/2_0_The_Inheritance/library/publish_files/index.json`
- `web-sdk/apps/the-inheritance/src/components/InheritanceBuyModal.svelte`
- `web-sdk/apps/the-inheritance/src/components/InheritanceUi.svelte`
- `web-sdk/packages/utils-xstate/src/createPrimaryMachines.ts`
- `web-sdk/packages/rgs-requests/src/rgs-requests.ts`

## 6. Free Spins Flow

### Confirmed From Code

1. `run_freespin_from_base()` sets the free-spin amount and calls `run_freespin()`.
2. `run_freespin()` calls `reset_fs_spin()`, then loops while `fs < tot_fs`.
3. Each free spin calls `update_freespin()`, `draw_board()`, `update_collection_state()`, `evaluate_lines_board()`, retrigger check, and win-manager update.
4. Freegame retrigger awards:
   - `2` scatters: `3` additional free spins
   - `3` scatters: `5` additional free spins
   - `4` scatters: `8` additional free spins
   - `5` scatters: `12` additional free spins
5. Freegame uses natural scatter count for retriggers. Legacy scatter credit is not used in freegame.
6. `freespin_end_event()` emits the free-game total amount.
7. `final_win_event()` emits final payout after base plus freegame winnings are calculated.

### Source Files

- `games/2_0_The_Inheritance/gamestate.py`
- `games/2_0_The_Inheritance/game_override.py`
- `src/events/events.py`
- `src/state/state.py`

## 7. Vault Scatter Rules And Occurrence Source

### Confirmed From Code

- Exact symbol id: `S`.
- Frontend asset: `web-sdk/apps/the-inheritance/static/assets/the-inheritance/symbols-cleaned/Vault Scatter.png`.
- Frontend asset key: `S` in `web-sdk/apps/the-inheritance/src/game/assets.ts`.
- Math internal classification: special symbol type `scatter`.
- Frontend display name in current info modal: `Vault Scatter`.
- Scatters are not in the paytable and do not pay independently.
- Scatters can appear on all five reels in active base and free strips.
- Because forced scatter placement subtracts a random row offset from the chosen scatter stop, a forced scatter can land on any visible row.

### Reel-Strip Occurrence Source

The real occurrence source is a combination of reel CSV stop counts, bet-mode distribution quotas, and `draw_board()` forcing/rejection logic.

| Source | Reel 1 | Reel 2 | Reel 3 | Reel 4 | Reel 5 | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `BR0.csv` | `1 / 80` | `1 / 80` | `1 / 80` | `1 / 80` | `1 / 80` | Base reveal strip. Natural non-force basegame redraws if `3+` visible scatters land. |
| `FR0.csv` | `1 / 120` | `1 / 120` | `1 / 120` | `1 / 120` | `1 / 120` | Freegame strip. Used for Free Spins. |
| `FRWCAP.csv` | `0 / 120` | `0 / 120` | `0 / 120` | `0 / 120` | `0 / 120` | Wincap-support freegame strip. |
| `FR100.csv` | `0 / 30` | `0 / 30` | `0 / 30` | `0 / 30` | `0 / 30` | File exists, but is not loaded in active `game_config.py`. |

### Mode Behavior

| Mode | Scatter Occurrence / Trigger Source |
| --- | --- |
| Base | Mode distribution selects criteria. Non-force basegame draws from `BR0` and rejects `3+` natural scatters. Forced freegame criteria uses `scatter_triggers {3: 50, 4: 20, 5: 5}`. |
| Scatter Boost | Same strips and scatter trigger weights as base, but freegame criteria quota is `0.108` instead of base `0.100`. |
| Bonus Buy | Current math mode `bonus` selects `freegame` criteria with quota `0.999` or `wincap` with quota `0.001`; the trigger board is forced from `BR0`. |
| Free Spins | Natural draws from `FR0`, except wincap criteria can use `FR0` and `FRWCAP`; retrigger checks use natural scatter count. |

### Trigger Counts

- Basegame trigger: effective `3`, `4`, or `5` scatters.
- Freegame retrigger: natural `2`, `3`, `4`, or `5` scatters.
- Legacy scatter credit can add one virtual scatter in basegame only when the key meter is full and exactly two natural scatters land under a forced-freegame distribution.

### Source Files

- `games/2_0_The_Inheritance/game_config.py`
- `games/2_0_The_Inheritance/reels/BR0.csv`
- `games/2_0_The_Inheritance/reels/FR0.csv`
- `games/2_0_The_Inheritance/reels/FRWCAP.csv`
- `games/2_0_The_Inheritance/reels/FR100.csv`
- `src/calculations/board.py`
- `src/calculations/statistics.py`

## 8. High / Low / Special Symbol Table

### Confirmed From Code

| Symbol ID | Displayed Name | Frontend Asset | Classification | Payout Behavior | Special Behavior / Feature Interaction |
| --- | --- | --- | --- | --- | --- |
| `S` | Vault Scatter | `Vault Scatter.png` | Special | No line pay | Triggers/retriggers Free Spins; no independent scatter pay found. |
| `W` | Wild | `Wild.png` | Special paying symbol | 3=`10x`, 4=`20x`, 5=`50x` | Substitutes for paying symbols. All-wild lines can pay as Wild. Does not substitute Scatter. |
| `M2` | Diamond Seal Multiplier 2 | `Diamond Seal Multiplier 2.png` | Special multiplier | No line pay | Fixed current-spin global multiplier value `2`. |
| `M5` | Diamond Seal Multiplier 5 | `Diamond Seal Multiplier 5.png` | Special multiplier | No line pay | Fixed current-spin global multiplier value `5`. |
| `M10` | Diamond Seal Multiplier 10 | `Diamond Seal Multiplier 10.png` | Special multiplier | No line pay | Fixed current-spin global multiplier value `10`. |
| `M20` | Diamond Seal Multiplier 20 | `Diamond Seal Multiplier 20.png` | Special multiplier | No line pay | Fixed current-spin global multiplier value `20`. |
| `M100` | Diamond Seal Multiplier 100 | `Diamond Seal Multiplier 100.png` | Special multiplier | No line pay | Fixed current-spin global multiplier value `100`. |
| `H1` | Heiress | `Heiress.png` | High | 3=`12x`, 4=`25x`, 5=`80x` | Normal line-pay symbol. |
| `H2` | Covered Portrait / Mystery | `Covered Portrait Mystery.png` | High | 3=`10x`, 4=`20x`, 5=`60x` | Normal line-pay symbol; no mystery transform found. |
| `H3` | Treasure Chest | `Treasure Chest.png` | High | 3=`8x`, 4=`15x`, 5=`45x` | Normal line-pay symbol. |
| `H4` | Legacy Key | `Legacy Key.png` | High and collection symbol | 3=`6x`, 4=`12x`, 5=`35x` | Counts toward Legacy Key meter in eligible basegame spins; can also pay lines. |
| `H5` | Diamond Brooch | `Diamond Brooch.png` | High | 3=`5x`, 4=`10x`, 5=`25x` | Normal line-pay symbol. |
| `H6` | Pocket Watch | `Antique Pocket Watch.png` | High | 3=`4x`, 4=`8x`, 5=`20x` | Normal line-pay symbol. |
| `H7` | Magnifying Glass | `Magnifying Glass.png` | High | 3=`3x`, 4=`6x`, 5=`15x` | Normal line-pay symbol. |
| `H8` | Will | `will.png` | High | 3=`2x`, 4=`5x`, 5=`12x` | Normal line-pay symbol. |
| `H9` | Old Letter | `Old Letter.png` | High | 3=`1.5x`, 4=`4x`, 5=`10x` | Normal line-pay symbol. |
| `L1` | A | `A.png` | Low | 3=`0.5x`, 4=`1x`, 5=`5x` | Normal line-pay symbol. |
| `L2` | K | `K.png` | Low | 3=`0.4x`, 4=`0.8x`, 5=`4x` | Normal line-pay symbol. |
| `L3` | Q | `Q.png` | Low | 3=`0.3x`, 4=`0.7x`, 5=`3x` | Normal line-pay symbol. |
| `L4` | J | `J.png` | Low | 3=`0.3x`, 4=`0.6x`, 5=`2.5x` | Normal line-pay symbol. |
| `L5` | 10 | `10.png` | Low | 3=`0.2x`, 4=`0.5x`, 5=`2x` | Normal line-pay symbol. |
| `L6` | Family Crest | `Family Crest Wild.png` | Low | 3=`0.1x`, 4=`0.4x`, 5=`1.5x` | Math treats this as a normal low symbol, despite the asset filename including `Wild`. |

### Multiplier Symbol Behavior

- Available values: `2`, `5`, `10`, `20`, `100`.
- The highest visible multiplier symbol on the current board is used.
- The multiplier is applied globally to line wins for the current reveal only.
- Total win is the sum of multiplied line wins.
- No persistence, collection, movement, or carry-over behavior was found for multiplier symbols.
- In freegame, a multiplier update can emit even if no multiplier symbol is visible; in that case the applied multiplier is `1`.

### Multiplier Reel Counts

| Reel Strip | `M2` | `M5` | `M10` | `M20` | `M100` | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `BR0.csv` | 1 | 1 | 1 | 1 | 1 | 5 |
| `FR0.csv` | 5 | 6 | 3 | 2 | 2 | 18 |
| `FRWCAP.csv` | 25 | 25 | 30 | 40 | 75 | 195 |

### Source Files

- `games/2_0_The_Inheritance/game_config.py`
- `games/2_0_The_Inheritance/game_executables.py`
- `games/2_0_The_Inheritance/game_override.py`
- `src/calculations/symbol.py`
- `src/calculations/lines.py`
- `web-sdk/apps/the-inheritance/src/game/assets.ts`
- `web-sdk/apps/the-inheritance/src/components/InheritanceInfoModal.svelte`

## 9. Paytable And Multiplier Behavior

### Confirmed From Code

- Number of paylines: `15`.
- Win direction: left-to-right starting from reel `0`.
- Minimum match count: `3`, because paytable entries start at 3 of a kind.
- Wins are line-based; multiple paylines can pay in the same reveal.
- Wild substitution:
  - Wild substitutes paying symbols.
  - All-wild lines can pay as Wild.
  - The line calculator compares the wild-only payout against the substituted-symbol payout and uses the better paying result.
- Scatter payout rules:
  - Scatter has no paytable entry.
  - Scatter triggers features; it does not pay independently in current math.
- Multiplier application order:
  - Base line payout is calculated from paytable.
  - Current-spin global multiplier is applied to that line win.
  - The multiplied line wins are summed into spin and total win.
- Maximum win: `5000x` by math config and bet-mode max win.

### Payline Table

| Line | Rows |
| ---: | --- |
| 1 | `[0, 0, 0, 0, 0]` |
| 2 | `[1, 1, 1, 1, 1]` |
| 3 | `[2, 2, 2, 2, 2]` |
| 4 | `[3, 3, 3, 3, 3]` |
| 5 | `[4, 4, 4, 4, 4]` |
| 6 | `[0, 1, 2, 3, 4]` |
| 7 | `[4, 3, 2, 1, 0]` |
| 8 | `[0, 1, 0, 1, 0]` |
| 9 | `[1, 0, 1, 0, 1]` |
| 10 | `[1, 2, 1, 2, 1]` |
| 11 | `[2, 1, 2, 1, 2]` |
| 12 | `[2, 3, 2, 3, 2]` |
| 13 | `[3, 2, 3, 2, 3]` |
| 14 | `[3, 4, 3, 4, 3]` |
| 15 | `[4, 3, 4, 3, 4]` |

### Source Files

- `games/2_0_The_Inheritance/game_config.py`
- `src/calculations/lines.py`
- `src/wins/multiplier_strategy.py`
- `src/wins/win_manager.py`

## 10. Legacy Key Behavior

### Confirmed From Code

- Exact symbol id: `H4`.
- Displayed name: Legacy Key.
- Frontend asset: `Legacy Key.png`.
- Math collection symbol: `collection_symbol = "H4"`.
- Math target: `10`.
- Current frontend placeholder target: `20`.
- Math collection is part of the game math, not frontend-only.
- Keys can appear on active base and free strips, but only collect when `can_collect_legacy_keys()` returns true.
- `can_collect_legacy_keys()` returns true only when:
  - `gametype == basegame`
  - `betmode != bonus`
- `update_collection_state()` adds every visible `H4` on the settled current board for eligible spins.
- Collection is capped at `collection_target`.
- When full, Legacy scatter credit is available.
- Legacy scatter credit can add one virtual scatter only when:
  - current `gametype` is `basegame`
  - bet mode is not `bonus`
  - key meter is full
  - current distribution has `force_freegame`
  - natural scatter count is exactly `2`
- When Legacy scatter credit is used:
  - event type `legacyScatterCredit` is emitted
  - key count resets to `0`
  - the effective scatter count becomes `3`
  - base free-spin trigger can proceed with `8` free spins
- In freegame, natural `2` scatters can retrigger, but Legacy scatter credit is not applied.

### Current Frontend Difference

- `stateGame.svelte.ts` currently counts visible final `H4` symbols in the settled `reveal` board and prevents duplicate board-signature counting.
- It currently uses target `20`, not the math target `10`.
- `typesBookEvent.ts` and `bookEventHandlerMap.ts` now type and handle math custom events `collectionUpdate`, `legacyScatterCredit`, and `multiplierUpdate`.

### Source Files

- `games/2_0_The_Inheritance/game_executables.py`
- `games/2_0_The_Inheritance/game_override.py`
- `games/2_0_The_Inheritance/dev_legacy_key_credit_test.py`
- `web-sdk/apps/the-inheritance/src/game/stateGame.svelte.ts`
- `web-sdk/apps/the-inheritance/src/game/typesBookEvent.ts`
- `web-sdk/apps/the-inheritance/src/game/bookEventHandlerMap.ts`

## 11. Frontend-To-Math Integration Map

### Confirmed From Code

| Area | Math / Library Source | Frontend Source | Current Status |
| --- | --- | --- | --- |
| Mode costs | `game_config.py`, `publish_files/index.json` | `config.ts`, `InheritanceUi.svelte`, `InheritanceBuyModal.svelte` | Base and bonus match; scatter boost mismatches (`3x` math vs `2x` frontend). |
| Paytable | `game_config.py` | `config.ts`, `InheritanceInfoModal.svelte` | Mostly mirrored; frontend `L4` and `L6` payout values differ from math config. |
| Symbols/assets | `game_config.py` symbols | `assets.ts` and static assets | Asset mapping exists for all math symbols. `L6` asset filename says Wild, but math treats it as low. |
| Reels/probabilities | CSV strips under `games/2_0_The_Inheritance/reels` | Frontend only has padding reels in `config.ts` | Frontend does not contain the active full reel strips. |
| Bet request | publish library / RGS play endpoint | `utils-xstate/createPrimaryMachines.ts` sends active mode key to `rgs-requests` | Real backend path can receive mode. Local mock handles base, scatter boost, and Bonus Buy without no-backend wallet errors. |
| Book events | `src/events/events.py` plus custom events in `game_executables.py`/`game_override.py` | `typesBookEvent.ts`, `bookEventHandlerMap.ts` | Standard events and custom collection/multiplier events are typed/handled. |
| Initial board | Not a math spin mode | `constants.ts` | Frontend-only display board. |
| Story data | Generated TS under `src/stories/data` | Storybook/local data | Appears stale: story data includes Wild multiplier attributes not present in current math rules. |

## 12. Known Gaps Or Unclear Logic

### Confirmed From Code

- `FR100.csv` exists but is not loaded by active math config.
- `FRWCAP.csv` is loaded as `WCAP` and used only through wincap freegame conditions.
- Local mock responses in `rgs-requests.ts` are hand-authored and still do not use active math reel strips, distribution quotas, or generated publish library results; they now mirror the documented paytable/paylines and Bonus Buy count.
- Current frontend state has explicit `spinMode: 'base' | 'boot' | 'bought' | 'free'`.

### Not Found In Code

- No generated publish-library refresh was found after the Bonus Buy rule change.
- No frontend visual use of `multiplierUpdate` positions is implemented yet; the event is consumed safely to prevent missing-handler errors.

### Needs Business Decision

- Whether to regenerate publish-library/story outputs from the updated math Bonus Buy rule.
- Whether Scatter Boost should follow math cost `3x` or user-facing earlier requirement `2x`.
- Whether Legacy Key target should follow math target `10` or current frontend placeholder `20`.
- Whether stale story data should be regenerated from current math before being used for local mock play.

## 13. Exact Source Files Used

### Math Package

- `games/2_0_The_Inheritance/game_config.py`
- `games/2_0_The_Inheritance/game_override.py`
- `games/2_0_The_Inheritance/game_executables.py`
- `games/2_0_The_Inheritance/gamestate.py`
- `games/2_0_The_Inheritance/game_optimization.py`
- `games/2_0_The_Inheritance/dev_legacy_key_credit_test.py`
- `games/2_0_The_Inheritance/dev_multiplier_test.py`
- `games/2_0_The_Inheritance/reels/BR0.csv`
- `games/2_0_The_Inheritance/reels/FR0.csv`
- `games/2_0_The_Inheritance/reels/FR100.csv`
- `games/2_0_The_Inheritance/reels/FRWCAP.csv`
- `games/2_0_The_Inheritance/library/publish_files/index.json`
- `src/calculations/board.py`
- `src/calculations/lines.py`
- `src/calculations/statistics.py`
- `src/calculations/symbol.py`
- `src/config/betmode.py`
- `src/config/config.py`
- `src/config/distributions.py`
- `src/events/events.py`
- `src/events/event_constants.py`
- `src/state/state.py`
- `src/wins/multiplier_strategy.py`
- `src/wins/win_manager.py`

### Frontend Package

- `web-sdk/apps/the-inheritance/src/game/assets.ts`
- `web-sdk/apps/the-inheritance/src/game/bookEventHandlerMap.ts`
- `web-sdk/apps/the-inheritance/src/game/config.ts`
- `web-sdk/apps/the-inheritance/src/game/constants.ts`
- `web-sdk/apps/the-inheritance/src/game/stateGame.svelte.ts`
- `web-sdk/apps/the-inheritance/src/game/typesBookEvent.ts`
- `web-sdk/apps/the-inheritance/src/components/InheritanceBuyModal.svelte`
- `web-sdk/apps/the-inheritance/src/components/InheritanceInfoModal.svelte`
- `web-sdk/apps/the-inheritance/src/components/InheritanceUi.svelte`
- `web-sdk/packages/rgs-requests/src/rgs-requests.ts`
- `web-sdk/packages/utils-xstate/src/createPrimaryMachines.ts`
- `web-sdk/packages/utils-xstate/src/createIntermediateMachineBet.ts`
- `web-sdk/packages/state-shared/src/stateBet.svelte.ts`
- `web-sdk/apps/the-inheritance/src/stories/data/base_books.ts`
- `web-sdk/apps/the-inheritance/src/stories/data/bonus_books.ts`
