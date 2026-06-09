# The Inheritance Design Notes

## Game identity

- Public game name: The Inheritance
- SDK folder: `2_0_The_Inheritance`
- Theme: mystery mansion / legacy / hidden vault / inheritance hunt
- Main colors: black, antique gold, dark green, warm mansion lighting

## Game layout

- 5 reels x 5 rows
- 15 paylines, matching the supplied payline image
- RTP configuration target: 97%
- Max win target: 5000x
- Row index 0 is the top row
- Row index 4 is the bottom row

## Payline paths

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
| `M100` | Diamond Seal Multiplier 100 | current-spin x100 multiplier |
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

## Bet modes

- Base spin cost: 1x
- Scatter chance enhancer cost: 3x
- Bonus buy cost: 100x

Scatter chance enhancer target:

```text
Normal 3-scatter trigger design reference: 1 in 255
Enhancer target: 8% relative increase to the 3-scatter trigger chance
Enhancer target reference: about 1 in 236 before final tuning
```

## First version rules

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
- Multiplier implementation: natural reel-strip Diamond Seal symbols in base and free-spin strips
- Base multipliers remain possible, including x100, at lower frequency than free/bought spins
- Free and bought bonus spins use higher-frequency multiplier reel strips
- Multiplier application: highest Diamond Seal visible on the current spin only
- Multiplier reset: every spin starts from x1 unless a Diamond Seal lands
- No stacking, persistence, or carryover

## Reel set

- `BR0.csv`: base-game strip with low-frequency natural multipliers, including all five Diamond Seal values
- `FR0.csv`: normal free-spin / bought-bonus strip with higher-frequency natural multipliers
- `FRWCAP.csv`: wincap-support free-spin strip with natural multipliers

## Frontend win effect thresholds

- Big Win: 12x bet
- Mega Win: 24x bet
- Epic Win: 50x+ bet
- Legendary Win: 100x+ bet

## Important note

This is the first math scaffold. The reel strips and paytable are starter values and must be tuned after the first simulation reports. Full RTP/math certification is not complete yet.
