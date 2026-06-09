# The Inheritance Multiplier Hit-Rate Targets

These are the target controlled multiplier hit rates for free-spin mode before final reel tuning.

## Target probabilities

| Multiplier | Symbol | Target hit rate |
|---:|---|---:|
| x2 | `M2` | 0.090 |
| x5 | `M5` | 0.080 |
| x10 | `M10` | 0.070 |
| x20 | `M20` | 0.050 |
| x100 | `M100` | 0.001 |
| No multiplier | none | 0.709 |

Total multiplier hit rate:

```text
0.090 + 0.080 + 0.070 + 0.050 + 0.001 = 0.291
```

No-multiplier rate:

```text
1.000 - 0.291 = 0.709
```

## Symbol model note

The multiplier set is exactly five Diamond Seal symbols:

```text
M2, M5, M10, M20, M100
```

## Implementation direction

Short reel strips alone are not suitable for hitting exact rare-symbol probabilities, especially `M100 = 0.001`, because each reel exposes three visible rows.

Use controlled multiplier selection to target these probabilities:

```text
M2    = 0.090
M5    = 0.080
M10   = 0.070
M20   = 0.050
M100  = 0.001
None  = 0.709
```

## Application rule

The controlled multiplier result applies to the current free-spin evaluation only:

```text
- no multiplier result applies x1
- one or more visible Diamond Seal symbols apply the highest visible value
- the next spin starts from x1 again
- no stacking or carryover is used
```

Final tuning should be verified with at least 100,000 free-spin samples.
