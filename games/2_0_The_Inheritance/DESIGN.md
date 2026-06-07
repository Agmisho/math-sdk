# Magic Guns Design Notes

## Game identity

- Public game name: Magic Guns
- SDK folder: `2_0_The_Inheritance`
- Theme: dark fantasy western / magical gunslinger
- Main colors: dark purple, gold, black, magical lightning glow

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
- Wild multiplier values during free spins: 2x, 3x, 4x, 5x, 10x, 20x, 50x
- Max win target: 5000x

## Frontend win effect thresholds

These are frontend display thresholds from our previous direction:

- Big Win: 12x bet
- Mega Win: 24x bet
- Epic Win: 50x+ bet
- Legendary Win: 100x+ bet

## Important note

This is the first math scaffold. The reel strips and paytable are starter values copied from the SDK lines-game pattern and renamed into the Magic Guns project. They must be tuned after the first simulation reports.
