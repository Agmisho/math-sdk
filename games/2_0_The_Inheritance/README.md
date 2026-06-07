# The Inheritance

Internal SDK folder: `games/2_0_The_Inheritance`.

## Direction

The Inheritance is a premium mystery mansion slot game using the visual direction from the provided sample:

- Dark mansion / hidden legacy theme
- Gold, black, green, and antique luxury styling
- Vault, family crest, portrait, key, will, brooch, watch, and mystery-object symbols
- Bonus scatter: Vault Scatter
- Wild symbol: Wild
- Regular family crest symbol: Family Crest Wild
- Multiplier symbols: Diamond Seal Multipliers
- Win effects for Big, Mega, Epic, and Legendary wins

## First math version

This first scaffold uses a simple Stake Engine lines-game structure:

- 5 reels
- 3 rows
- 20 paylines
- 22 total symbols
- 1 scatter: `S`
- 5 multipliers: `M2`, `M5`, `M10`, `M20`, `M100`
- 1 wild: `W`
- 15 regular paying symbols: `H1-H9`, `L1-L6`
- Base mode
- Bonus buy mode
- Free spins from 3+ scatters
- Max win target: 5000x

## Frontend symbol mapping

The math engine keeps compact symbol IDs. The frontend should map them to the actual asset names:

| Math symbol | Asset name |
|---|---|
| `S` | Vault Scatter |
| `M2` | Diamond Seal Multiplier 2 |
| `M5` | Diamond Seal Multiplier 5 |
| `M10` | Diamond Seal Multiplier 10 |
| `M20` | Diamond Seal Multiplier 20 |
| `M100` | Diamond Seal Multiplier 100 |
| `W` | Wild |
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

## Planned frontend events

The starter math files use the default line-win events first. Later we will add custom event names that the frontend can animate:

- `bonusTrigger`
- `bonusIntro`
- `scatterLanding`
- `multiplierLanding`
- `mansionLevelUpdate`
- `collectedUpdate`
- `bigWin`
- `megaWin`
- `epicWin`
- `legendaryWin`

## Next work

1. Run the math scaffold in Codespaces.
2. Fix any SDK runtime errors.
3. Tune reel strips.
4. Tune paytable.
5. Add collection and mansion level logic.
6. Generate books/configs.
7. Connect frontend assets in `arcane-reels`.
