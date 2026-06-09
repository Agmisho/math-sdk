# The Inheritance Design Notes

## Game identity

- Public game name: The Inheritance
- SDK folder: `2_0_The_Inheritance`
- Theme: mystery mansion / legacy / hidden vault / inheritance hunt
- Main colors: black, antique gold, dark green, warm mansion lighting

## Symbol model

Total symbols: 22

- 1 scatter
- 5 multiplier symbols
- 1 wild
- 15 regular paying symbols

## Special symbols

| Math symbol | Asset name | Role |
|---|---|---|
| `S` | Vault Scatter | Bonus trigger |
| `M2` | Diamond Seal Multiplier 2 | current-spin x2 multiplier |
| `M5` | Diamond Seal Multiplier 5 | current-spin x5 multiplier |
| `M10` | Diamond Seal Multiplier 10 | current-spin x10 multiplier |
| `M20` | Diamond Seal Multiplier 20 | current-spin x20 multiplier |
| `M100` | Diamond Seal Multiplier 100 | current-spin x100 multiplier / ultra rare |
| `W` | Wild | Wild substitute |

## Paying symbols

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

## First version rules

- 5 reels x 3 rows
- 20 paylines
- Base spin cost: 1x
- Bonus buy cost: 100x
- Free spins trigger:
  - 3 scatters = 8 free spins
  - 4 scatters = 12 free spins
  - 5 scatters = 15 free spins
- Free spin retrigger:
  - 2 scatters = +3 free spins
  - 3 scatters = +5 free spins
  - 4 scatters = +8 free spins
  - 5 scatters = +12 free spins
- Multiplier values: x2, x5, x10, x20, x100
- Multiplier application: highest Diamond Seal visible on the current spin only
- Multiplier reset: every spin starts from x1 unless a Diamond Seal lands
- Max win target: 5000x

## Frontend win effect thresholds

- Big Win: 12x bet
- Mega Win: 24x bet
- Epic Win: 50x+ bet
- Legendary Win: 100x+ bet

## Important note

This is the first math scaffold. The reel strips and paytable are starter values and must be tuned after the first simulation reports.
