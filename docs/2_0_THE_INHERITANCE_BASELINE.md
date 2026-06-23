# 2_0_THE_INHERITANCE Baseline

This file captures the current local baseline before adding Key-driven Vault Reel or other new feature mechanics. Values are confirmed from code and generated local output where available.

## Core Math Baseline

| Item | Current value | Source |
| --- | --- | --- |
| Game id | `2_0_The_Inheritance` | `game_config.py` |
| Working name | `The Inheritance` | `game_config.py` |
| Board size | 5 reels x 5 rows | `game_config.py` |
| Pay method | 15 fixed paylines, left-to-right | `game_config.py`, `src/calculations/lines.py` |
| RTP target | `0.9700` | `game_config.py` |
| Win cap | `5000x` | `game_config.py` |
| Base mode cost | `1.0x` | `game_config.py`, `publish_files/index.json` |
| Scatter Boost cost | Math `3.0x`; frontend currently `2.0x` | `game_config.py`, `config.ts` |
| Bonus Buy cost | `100.0x` | `game_config.py`, `publish_files/index.json` |
| Bonus Buy free spins | `10` | `game_config.py`, `game_override.py` |

## Paytable

| Symbol | 5 | 4 | 3 |
| --- | ---: | ---: | ---: |
| `W` | 50 | 20 | 10 |
| `H1` | 80 | 25 | 12 |
| `H2` | 60 | 20 | 10 |
| `H3` | 45 | 15 | 8 |
| `H4` | 35 | 12 | 6 |
| `H5` | 25 | 10 | 5 |
| `H6` | 20 | 8 | 4 |
| `H7` | 15 | 6 | 3 |
| `H8` | 12 | 5 | 2 |
| `H9` | 10 | 4 | 1.5 |
| `L1` | 5 | 1 | 0.5 |
| `L2` | 4 | 0.8 | 0.4 |
| `L3` | 3 | 0.7 | 0.3 |
| `L4` | 2.5 | 0.6 | 0.3 |
| `L5` | 2 | 0.5 | 0.2 |
| `L6` | 1.5 | 0.4 | 0.1 |

## Paylines

| Line | Rows |
| ---: | --- |
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

## Current Reel / Multiplier Baseline

| Strip | Stops per reel | Scatter count | Multiplier count | Notes |
| --- | ---: | ---: | ---: | --- |
| `BR0.csv` | 80 | 1 per reel | 5 total | Active base strip |
| `FR0.csv` | 120 | 1 per reel | 18 total | Active free-spin strip |
| `FRWCAP.csv` | 120 | 0 | 195 total | Active only as `WCAP` in wincap freegame condition |
| `FR100.csv` | 30 | 0 | 1 total | Exists, not loaded in active config |

Multiplier values:

```text
M2 = 2
M5 = 5
M10 = 10
M20 = 20
M100 = 100
```

Stacking rule: highest visible Diamond Seal applies globally to all line wins for the current reveal. It resets next spin. No persistence or additive stacking is currently used.

## Feature Baseline

| Feature | Current baseline |
| --- | --- |
| Base free-spin trigger | 3 scatters = 8 FS, 4 scatters = 12 FS, 5 scatters = 15 FS |
| Free-spin retrigger | 2 scatters = +3 FS, 3 = +5 FS, 4 = +8 FS, 5 = +12 FS |
| Bonus Buy | 100x cost, force-freegame mode, exactly 10 initial free spins in current source |
| Legacy Key | `H4`, target 10 in math, collection only in basegame when betmode is not `bonus` |
| Legacy scatter credit | Full key meter plus exactly 2 natural basegame scatters can create 3 effective scatters |
| Mystery | No deterministic reveal mechanic found |
| Sticky Wild / respin / showdown | Not found |

## Generated Output Baseline

The existing generated library contains 10,000-entry outputs for base, scatter boost, and bonus. These files may be stale relative to the latest Bonus Buy 10-free-spin source change and should be regenerated before final economic certification.

| Mode | Cost | Generated entries | Generated RTP field | Average win | Max win field | Non-zero HR | Nil probability | Source |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `base` | 1 | 10,000 | 10.642 | 10.642 | 500000.0 | 6.112 | 0.836 | `library/stats_summary.json` |
| `scatter_boost` | 3 | 10,000 | 3.661 | 10.982 | 500000.0 | 5.889 | 0.830 | `library/stats_summary.json` |
| `bonus` | 100 | 10,000 | 0.542 | 54.217 | 500000.0 | 1.226 | 0.185 | `library/stats_summary.json` |

Mode fence info from `library/statistics_summary.json`:

| Mode | Segment | HR | RTP contribution field | Average win |
| --- | --- | ---: | ---: | ---: |
| `base` | `freegame` | 255.0 | 0.37 | 94.35 |
| `base` | `basegame` | 3.5 | 0.59 | 2.06 |
| `scatter_boost` | `freegame` | 236.0 | 0.39 | 276.12 |
| `scatter_boost` | `basegame` | 3.5 | 0.57 | 5.98 |
| `bonus` | `freegame` | Not populated | Not populated | Not populated |

Verification files:

| Mode | Entries | Payout hash |
| --- | ---: | --- |
| `base` | 10,000 | `260b169d995f96de108047ced9602111` |
| `scatter_boost` | 10,000 | `b27d9743acec173430a060524bb77a30` |
| `bonus` | 10,000 | `7b32d45048d112931ce19ac2c3cbae4d` |

## Current Build / Test Status

Last known local checks before new feature mechanics:

| Check | Status |
| --- | --- |
| `dev_legacy_key_credit_test.py` | Passing |
| `dev_sdk_smoke_test.py` | Passing |
| Targeted Bonus Buy math check | Passing: first `freeSpinTrigger.totalFs == 10` |
| `pnpm --filter the-inheritance build` | Passing after stopping dev server and clearing generated build folder |
| Dev server | Running at `http://127.0.0.1:3007/` |
| Headless browser runtime check | Loaded Pixi canvas with zero runtime/console errors |

## Baseline Concerns To Resolve Before Final Tuning

- Generated stats should be regenerated after the Bonus Buy source update.
- Scatter Boost cost mismatch must be resolved deliberately: math and generated outputs say `3x`, frontend says `2x`.
- Frontend paytable mirror must be reconciled with math for `L4` and `L6` 3-kind values.
- Existing statistics output format needs interpretation before claiming final simulated RTP, because current generated `stats_summary.json` values are not simple `0.97`-style RTP fractions for all modes.

