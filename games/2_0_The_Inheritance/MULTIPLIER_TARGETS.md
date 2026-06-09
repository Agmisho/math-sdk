# The Inheritance Multiplier Hit-Rate Targets

These are the target visible-board multiplier hit rates for bonus/free-spin mode before final reel tuning.

## Target probabilities

| Multiplier | Symbol | Target hit rate |
|---:|---|---:|
| x2 | `M2` | 0.100 |
| x5 | `M5` | 0.090 |
| x10 | `M10` | 0.080 |
| x20 | `M20` | 0.070 |
| x50 | `M50` | 0.005 |
| x100 | `M100` | 0.001 |
| No multiplier | none | 0.654 |

Total multiplier hit rate:

```text
0.100 + 0.090 + 0.080 + 0.070 + 0.005 + 0.001 = 0.346
```

No-multiplier rate:

```text
1.000 - 0.346 = 0.654
```

## Important symbol model note

Adding `M50` changes the multiplier set from 5 symbols to 6 symbols.

Previous multiplier symbols:

```text
M2, M5, M10, M20, M100
```

New multiplier symbols:

```text
M2, M5, M10, M20, M50, M100
```

If the game must remain exactly 22 total symbols, one regular paying symbol must be removed or merged. If 23 symbols are acceptable, no regular symbol needs to be removed.

## Implementation direction

Do not rely only on short reel strips to achieve `M50 = 0.005` and `M100 = 0.001`. Short strips make rare symbols appear too often because each reel exposes three visible rows.

Use controlled reel paths or controlled multiplier injection/tuning:

```text
M2    common
M5    common-low
M10   medium
M20   medium-low
M50   rare
M100  ultra rare
```

Final tuning should be verified with at least 100,000 bonus/free-spin samples, not 500 samples.
