# Magic Guns

Internal SDK folder: `games/2_0_The_Inheritance`.

## Direction

Magic Guns is a premium dark fantasy western slot game using the theme decisions from our previous chats:

- Dark purple and gold casino style
- Magical revolvers / gunslinger feeling
- Purple magical lightning
- Bonus scatter symbols
- Wild symbol with multiplier behavior
- Bonus intro full-screen transition
- Win effects for Big, Mega, Epic, and Legendary wins

## First math version

This first scaffold uses a simple Stake Engine lines-game structure:

- 5 reels
- 3 rows
- 20 paylines
- Wild symbol: `W`
- Scatter symbol: `S`
- High symbols: `H1`, `H2`, `H3`, `H4`
- Low symbols: `L1`, `L2`, `L3`, `L4`, `L5`
- Base mode
- Bonus buy mode
- Free spins from 3+ scatters
- Wild multipliers during free spins
- Max win target: 5000x

## Frontend symbol mapping

The math engine keeps compact symbol IDs. The frontend should map them to Magic Guns assets:

| Math symbol | Theme asset idea |
|---|---|
| `W` | Magic Wild revolver |
| `S` | Bonus Scatter badge / magic guns bonus symbol |
| `H1` | Golden revolver |
| `H2` | Purple spell bullet |
| `H3` | Cowboy hat |
| `H4` | Sheriff star / cursed badge |
| `L1` | A |
| `L2` | K |
| `L3` | Q |
| `L4` | J |
| `L5` | 10 |

## Planned frontend events

The starter math files use the default line-win events first. Later we will add custom event names that the Magic Guns frontend can animate:

- `bonusTrigger`
- `bonusIntro`
- `wildMultiplier`
- `scatterLanding`
- `bigWin`
- `megaWin`
- `epicWin`
- `legendaryWin`

## Next work

1. Confirm final symbol list and asset names.
2. Confirm paylines vs ways.
3. Tune reel strips.
4. Tune paytable.
5. Add Magic Guns-specific custom events.
6. Generate books/configs.
7. Connect frontend assets in `arcane-reels`.
