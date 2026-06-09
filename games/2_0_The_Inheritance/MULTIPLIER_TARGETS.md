# The Inheritance Multiplier Hit-Rate Targets

These are the target visible-board multiplier hit rates for bonus/free-spin mode before final reel tuning.

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

The multiplier set remains 5 symbols:

```text
M2, M5, M10, M20, M100
```

`M50` does not exist and must not be added to the math model or frontend asset mapping.

## Implementation direction

Short reel strips alone are not suitable for hitting exact rare-symbol probabilities, especially `M100 = 0.001`, because each reel exposes three visible rows.

Use controlled reel weighting or controlled multiplier selection to target these probabilities:

```text
M2    = 0.090
M5    = 0.080
M10   = 0.070
M20   = 0.050
M100  = 0.001
None  = 0.709
```

Final tuning should be verified with at least 100,000 bonus/free-spin samples, not 500 samples.
