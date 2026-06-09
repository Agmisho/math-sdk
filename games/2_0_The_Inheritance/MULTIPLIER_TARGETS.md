# The Inheritance Multiplier Reel Notes

The final implementation uses natural reel-strip multiplier symbols in free-spin reel strips.

## Implementation model

Multiplier outcomes are not selected by controlled injection. Diamond Seal symbols exist directly in reel strips:

- `FR0.csv` contains natural free-spin multipliers.
- `FRWCAP.csv` contains natural wincap-support multipliers.
- `BR0.csv` is a base-game strip and does not carry Diamond Seal multiplier behavior.

The multiplier set is exactly five Diamond Seal symbols:

```text
M2, M5, M10, M20, M100
```

## Application rule

The visible board determines the applied multiplier for each free-spin evaluation:

```text
- no visible Diamond Seal applies x1
- one visible Diamond Seal applies its value
- multiple visible Diamond Seals apply the highest visible value
- the next spin starts from x1 again
- no stacking, persistence, or carryover is used
```

## Event rule

`multiplierUpdate` describes only the current spin:

```text
multiplier
appliedMultiplier
landedMultiplier
positions
gameType
```

`positions` lists every visible Diamond Seal symbol on the board. `appliedMultiplier` and `landedMultiplier` are the highest visible multiplier value, or 1 when no multiplier is visible.

## Tuning note

The current reel strips are development strips. Final RTP and volatility certification should be done with the normal SDK generation, optimization, and analysis flow after the fast development checks pass.
