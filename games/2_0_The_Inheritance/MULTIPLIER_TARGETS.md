# The Inheritance Multiplier Reel Notes

The final implementation uses natural reel-strip multiplier symbols.

## Implementation model

Multiplier outcomes are not selected by controlled injection. Diamond Seal symbols exist directly in reel strips:

- `BR0.csv` contains low-frequency base-game multipliers.
- `FR0.csv` contains normal free-spin multipliers at a higher frequency than `BR0.csv`.
- `FRWCAP.csv` contains wincap-support multipliers.

The multiplier set is exactly five Diamond Seal symbols:

```text
M2, M5, M10, M20, M100
```

## Application rule

The visible board determines the applied multiplier for each spin evaluation:

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
