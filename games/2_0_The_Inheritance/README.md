# The Inheritance

Internal SDK folder: `games/2_0_The_Inheritance`.

## Direction

The Inheritance is a premium mystery mansion slot game using a dark mansion / hidden legacy theme with antique gold, black, dark green, and warm mansion lighting.

## Math model

- 5 reels
- 3 rows
- 20 paylines
- Max win target: 5000x
- Base mode
- Bonus buy mode
- Free spins from 3+ scatters

## Symbol model

Total symbols: 22

- 1 scatter
- 5 Diamond Seal multiplier symbols
- 1 wild
- 15 regular paying symbols

## Special symbols

| Math symbol | Asset name | Role |
|---|---|---|
| `S` | Vault Scatter | Free-spin trigger |
| `W` | Wild | Wild substitute |
| `M2` | Diamond Seal Multiplier 2 | Current-spin x2 multiplier |
| `M5` | Diamond Seal Multiplier 5 | Current-spin x5 multiplier |
| `M10` | Diamond Seal Multiplier 10 | Current-spin x10 multiplier |
| `M20` | Diamond Seal Multiplier 20 | Current-spin x20 multiplier |
| `M100` | Diamond Seal Multiplier 100 | Current-spin x100 multiplier |

## Regular paying symbols

| Math symbol | Asset name |
|---|---|
| `H1` | Heriess |
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
| `L6` | Family Crest Wild |

## Paytable

| Symbol | 5-of-a-kind | 4-of-a-kind | 3-of-a-kind |
|---|---:|---:|---:|
| `W` | 50 | 20 | 10 |
| `H1` | 80 | 25 | 12 |
| `H2` | 60 | 20 | 10 |
| `H3` | 45 | 15 | 8 |
| `H4` | 35 | 12 | 6 |
| `H5` | 25 | 10 | 5 |
| `H6` | 20 | 8 | 4 |
| `H7` | 15 | 6 | 3 |
| `H8` | 12 | 5 | 2 |
| `H9` | 10 | 4 | 1.5 |
| `L1` | 5 | 1 | 0.5 |
| `L2` | 4 | 0.8 | 0.4 |
| `L3` | 3 | 0.7 | 0.3 |
| `L4` | 2.5 | 0.6 | 0.25 |
| `L5` | 2 | 0.5 | 0.2 |
| `L6` | 1.5 | 0.4 | 0.15 |

Multiplier symbols do not have direct paytable payouts.

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

## Diamond Seal multiplier behavior

Diamond Seal multipliers are moving reel symbols only.

- `M2`, `M5`, `M10`, `M20`, and `M100` are separate symbols.
- They can land in the same spin, on the same line, or next to each other.
- If one or more land in the same spin, the highest visible multiplier applies.
- The multiplier applies only to the current spin.
- The next spin starts from x1 unless another Diamond Seal symbol lands.
- There is no stacking, no carryover, and no persistent bonus multiplier.

Target controlled hit rates:

| Result | Target rate |
|---|---:|
| No multiplier | 0.709 |
| `M2` | 0.090 |
| `M5` | 0.080 |
| `M10` | 0.070 |
| `M20` | 0.050 |
| `M100` | 0.001 |

## Collection event

`H4` Legacy Key is the collection symbol.

`collectionUpdate` should include:

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
PYTHONPATH=. python3 games/2_0_The_Inheritance/run.py
```

Full book generation should wait until feature logic and fast tests are stable.
