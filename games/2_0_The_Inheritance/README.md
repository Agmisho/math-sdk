# The Inheritance

Internal SDK folder: `games/2_0_The_Inheritance`.

## Direction

The Inheritance is a premium mystery mansion slot game using a dark mansion / hidden legacy theme with antique gold, black, dark green, and warm mansion lighting.

## Math model

- 5 reels
- 5 rows
- 15 paylines
- RTP configuration: 97%
- Volatility target: High
- Max win target: 5000x
- Base mode
- Scatter chance enhancer mode
- Bonus buy mode
- Free spins from 3+ scatters
- Persistent Legacy Key virtual scatter credit
- `run.py` is the SDK generation entrypoint
- Development scripts are separate and are not part of the production generation flow

## Buy menu

The frontend `BUY` button opens a Buy menu with two options:

| Buy menu option | Internal mode | Cost | Behavior |
|---|---|---:|---|
| Scatter Boost | `scatter_boost` | 3x base bet per spin | Base spin with 8% relative higher 3-scatter trigger chance |
| Bonus Buy | `bonus` | 100x base bet | Starts a bought 3-, 4-, or 5-scatter entry state and awards 10 free spins |

Scatter chance enhancer target:

```text
Normal 3-scatter trigger design reference: 1 in 255
Scatter boost target reference: about 8% relative higher chance, around 1 in 222
```

Bonus Buy entry behavior:

```text
Bonus Buy can start as if triggered by 3, 4, or 5 scatters and awards 10 free spins.
The configured scatter entry weights are defined in game_config.py under freegame_condition.scatter_triggers.
```

## Bet modes

| Mode | Cost | Purpose |
|---|---:|---|
| `base` | 1x | Standard base spin |
| `scatter_boost` | 3x | Buy-menu Scatter Boost spin |
| `bonus` | 100x | Buy-menu Bonus Buy feature |

## Payline layout

Rows are indexed from top to bottom:

```text
Top row    = 0
Second row = 1
Middle row = 2
Fourth row = 3
Bottom row = 4
```

The 15 paylines match the supplied 5x5 payline image:

| Line | Row path |
|---:|---|
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

## Symbol model

Total symbols: 22

- 1 scatter
- 5 Diamond Seal multiplier symbols
- 1 wild
- 15 regular paying symbols

## Special symbols

| Math symbol | Asset name | Role |
|---|---|---|
| `S` | Vault_Scatter | Free-spin trigger |
| `W` | Wild | Wild substitute |
| `M2` | Diamond Seal Multiplier 2 | Current-spin x2 multiplier |
| `M5` | Diamond Seal Multiplier 5 | Current-spin x5 multiplier |
| `M10` | Diamond Seal Multiplier 10 | Current-spin x10 multiplier |
| `M20` | Diamond Seal Multiplier 20 | Current-spin x20 multiplier |
| `M100` | Diamond Seal Multiplier 100 | Current-spin x100 multiplier |

## Regular paying symbols

| Math symbol | Asset name |
|---|---|
| `H1` | Heiress |
| `H2` | Covered Portrait Mystery |
| `H3` | Treasure Chest |
| `H4` | Legacy Key |
| `H5` | Diamond Brooch |
| `H6` | Antique Pocket Watch |
| `H7` | Magnifying Glass |
| `H8` | will |
| `H9` | Old Letter |
| `L1` | A |
| `L2` | K |
| `L3` | Q |
| `L4` | J |
| `L5` | 10 |
| `L6` | Family Crest |

## Paytable

| Symbol | 5-of-a-kind | 4-of-a-kind | 3-of-a-kind |
|---|---:|---:|---:|
| `W` | 20 | - | - |
| `H1` | 5 | 2.5 | 0.5 |
| `H2` | 5 | 2.5 | 0.5 |
| `H3` | 10 | 5 | 1 |
| `H4` | 10 | 5 | 1 |
| `H5` | 20 | 1 | 2 |
| `H6` | 20 | 1 | 2 |
| `H7` | 15 | 6 | 3 |
| `H8` | 12 | 5 | 2 |
| `H9` | 10 | 4 | 1.5 |
| `L1` | 1 | 0.5 | 0.1 |
| `L2` | 1 | 0.5 | 0.1 |
| `L3` | 1 | 0.5 | 0.1 |
| `L4` | 1 | 0.5 | 0.1 |
| `L5` | 1 | 0.5 | 0.1 |
| `L6` | 1.5 | 0.4 | 0.1 |

Multiplier symbols do not have direct paytable payouts.

## Reels

- `BR0.csv` is the base-game reel strip and contains all Diamond Seal multiplier symbols at lower frequency.
- `FR0.csv` is the normal free-spin / bought-bonus reel strip and contains Diamond Seal multiplier symbols at a much higher frequency than `BR0.csv`.
- `FRWCAP.csv` is the wincap-support free-spin reel strip and contains natural Diamond Seal multiplier symbols.
- The `WCAP` reel condition is included in the distribution model for wincap simulations.

Current build-level frequency direction:

```text
BR0 base game: lower multiplier frequency, all M2/M5/M10/M20/M100 possible
FR0 free / bought bonus: much higher multiplier frequency
FRWCAP: wincap-support multiplier-rich free-spin strip
```

## Free spins

Base game trigger:

- 3 scatters = 8 free spins
- 4 scatters = 12 free spins
- 5 scatters = 15 free spins

Free-spin retrigger:

- 2 scatters = +3 free spins
- 3 scatters = +5 free spins
- 4 scatters = +8 free spins
- 5 scatters = +12 free spins

## Legacy Key persistent scatter credit

`H4` Legacy Key is both a paying symbol and the persistent collection symbol.

Rules:

- Legacy Keys are collected only during paid `base` and `scatter_boost` spins.
- Legacy Keys are not collected during free spins.
- Legacy Keys are not collected during Bonus Buy.
- Key collection persists between paid spins and must be stored by the frontend/server player state.
- Collection target is 10 keys.
- When the player starts an eligible paid spin with 10 keys, one virtual scatter credit is available.
- If that spin lands exactly 2 natural scatters, the virtual credit makes it 3 effective scatters.
- 3 effective scatters trigger 8 free spins.
- After the virtual scatter credit is used and the free game is won/triggered, collection resets to 0.

`legacyScatterCredit` includes:

- `collected`
- `target`
- `virtualScatters`
- `naturalScatters`
- `effectiveScatters`
- `used`
- `gameType`

## Diamond Seal multiplier behavior

Diamond Seal multipliers are natural moving reel symbols.

- `M2`, `M5`, `M10`, `M20`, and `M100` are separate symbols.
- They can land in the same spin, on the same line, or next to each other.
- If one or more land in the same spin, the highest visible multiplier applies globally to that spin.
- The multiplier applies only to the current spin.
- The next spin starts from x1 unless another Diamond Seal symbol lands.
- There is no stacking, no carryover, and no persistent bonus multiplier.

`multiplierUpdate` includes:

- `multiplier`
- `appliedMultiplier`
- `landedMultiplier`
- `positions`
- `gameType`

## Collection event

`collectionUpdate` includes:

- `collected`
- `target`
- `mansionLevel`
- `displayMultiplier`
- `positions`
- `gameType`

Collection progress is separate from Diamond Seal multiplier logic.

## Development tests

From repository root:

```bash
PYTHONPATH=games/2_0_The_Inheritance:. python3 games/2_0_The_Inheritance/dev_multiplier_test.py
PYTHONPATH=games/2_0_The_Inheritance:. python3 games/2_0_The_Inheritance/dev_sdk_smoke_test.py
PYTHONPATH=. python3 games/2_0_The_Inheritance/dev_legacy_key_credit_test.py
```

Full SDK generation uses:

```bash
PYTHONPATH=. python3 games/2_0_The_Inheritance/run.py
```
