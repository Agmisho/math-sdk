# 2_0_THE_INHERITANCE Post-Change Report

## Current Slice

This report covers the first implementation slice after the source-of-truth audit: a separated, deterministic Legacy Key / Vault Reel math resolver plus frontend event consumption.

## Files Changed

- `games/2_0_The_Inheritance/inheritance_symbol_roles.py`
- `games/2_0_The_Inheritance/inheritance_feature_config.py`
- `games/2_0_The_Inheritance/inheritance_vault_reels.py`
- `games/2_0_The_Inheritance/game_config.py`
- `games/2_0_The_Inheritance/game_executables.py`
- `games/2_0_The_Inheritance/game_override.py`
- `games/2_0_The_Inheritance/gamestate.py`
- `games/2_0_The_Inheritance/dev_vault_reel_feature_test.py`
- `web-sdk/apps/the-inheritance/src/game/typesBookEvent.ts`
- `web-sdk/apps/the-inheritance/src/game/bookEventHandlerMap.ts`
- `web-sdk/apps/the-inheritance/src/game/stateGame.svelte.ts`
- `web-sdk/apps/the-inheritance/src/stories/ModeBaseBookEvent.stories.svelte`
- `web-sdk/apps/the-inheritance/src/stories/data/base_events.ts`

## Features Retained Unchanged

- Existing reels, paylines, paytable, win cap, bet modes, free-spin triggers, Bonus Buy cost, and current Diamond Seal multiplier values are preserved.
- Existing Diamond Seal multiplier stacking remains `highest visible/source multiplier wins` as a one-spin global multiplier.
- Existing Legacy Key virtual scatter credit remains in place.

## Feature Added

The Vault Reel resolver can be enabled by `config.inheritance_feature_config["vault_reel"]["enabled"]`.

When enabled:

1. Existing Key-role symbols (`H4`) are scanned after board reveal and collection update.
2. Each candidate Key reel is hypothetically transformed into the existing Wild symbol (`W`).
3. The existing `Lines.get_lines` evaluator checks whether the transformed reel creates or improves real payable line wins.
4. The reel is transformed only if payable improvement exists.
5. Existing Diamond Seal symbols on transformed reels are preserved as multiplier sources.
6. A Vault Reel multiplier can be selected from existing multiplier symbols using weights derived from current reel strips.
7. Final line wins use the existing global `highest` multiplier stacking rule.
8. A deterministic `vaultReelResolved` event is emitted for frontend rendering.

## Default Runtime Status

The new Vault Reel feature is intentionally disabled by default until simulation and RTP tuning are completed. A 100-spin default-config sample emitted `0` Vault Reel events.

This avoids silently changing the current RTP, hit rate, max-win frequency, and bonus distribution before a math tuning pass.

## Event Contract

`vaultReelResolved` includes:

- source Key symbol and position
- target reel
- original symbols
- transformed Wild positions
- Wild symbol ID
- multiplier symbol/value/source position
- multiplier stack data
- affected paylines
- line win before transform
- line win before multiplier
- final line win
- total spin win before/after
- cap status

## Tests Run

- `PYTHONPATH=. python games/2_0_The_Inheritance/dev_vault_reel_feature_test.py`
- `PYTHONPATH=. python games/2_0_The_Inheritance/dev_legacy_key_credit_test.py`
- `PYTHONPATH=. python games/2_0_The_Inheritance/dev_sdk_smoke_test.py`
- `PYTHONPATH=. python games/2_0_The_Inheritance/dev_multiplier_test.py`
- `cd web-sdk && pnpm --filter the-inheritance build`

## Simulation Status

Full book generation, lookup-table regeneration, and RTP tuning have not been run for the new enabled Vault Reel feature. This is required before turning the feature on in default production config.

## Remaining Work

- Tune and simulate Vault Reel activation frequency.
- Add dedicated configured feature modes for Vault Free Spins, high-volatility free spins, Sealed Will collection/showdown, and Portrait Mystery.
- Generate books, compressed books, configs, lookup tables, and updated reports after economics are approved.
- Expand frontend visuals from the current deterministic board-settle handler into the full Key/Vault unlock animation sequence.
