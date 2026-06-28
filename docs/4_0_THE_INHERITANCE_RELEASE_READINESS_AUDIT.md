# The Inheritance Release Readiness Audit

Date: 2026-06-28

Scope:

- Original design plan: `C:\Users\Agmish\Desktop\THE_INHERITANCE_FULL_GAME_DESCRIPTION.docx`
- Math SDK: `games/2_0_The_Inheritance`
- Web SDK: `web-sdk/apps/the-inheritance`
- Local demo bridge: `tools/the-inheritance-local-rgs`

This audit compares the current product to the attached plan, fixes verified
implementation mismatches, and records remaining approval or business risks.

## Executive Summary

Current status: ready for continued local QA and provider review, with one
approval-sensitive business decision still open.

Confirmed aligned:

- 5 reels x 5 visible rows.
- 15 fixed paylines, left to right.
- Base Spin costs 1x.
- Scatter Boost costs 3x.
- Bonus Buy costs 100x and awards 10 Free Spins.
- Free Spins do not deduct an extra bet.
- Legacy Key target is 10.
- RTP editions are 92%, 93%, 94%, 95%, 96%, and 97%.
- Maximum round cap remains 5000x.
- Local demo starts at `$1,000.00`.
- Frontend uses settled Math/RGS results instead of calculating outcomes.

Fixed in this pass:

- Wild substitution is now blocked for Legacy Key (`H4`), Vault Scatter (`S`),
  and Diamond Seal multiplier symbols (`M2`, `M5`, `M10`, `M20`, `M100`).
- The Wild can still substitute normal paying symbols and can still pay as five
  Wilds.
- Added a focused Wild substitution regression test.
- Regenerated local books and RTP profile validation after the math change.
- Fixed the The Inheritance SvelteKit `tsconfig` warning by extending the
  generated `.svelte-kit/tsconfig.json`.
- Added local RGS in-memory replay support for settled demo rounds.
- Updated local RGS tests for replay.

## Plan Comparison

| Plan Item | Current Result |
| --- | --- |
| Premium mansion 5x5 slot | Implemented in the existing The Inheritance app and math package. |
| 15 fixed paylines | Implemented in `game_config.py` and mirrored in Web config. |
| Base mode 1x | Implemented. |
| Scatter Boost 3x | Implemented as `scatter_boost`. |
| Bonus Buy 100x | Implemented as `bonus`. |
| Bonus Buy awards 10 Free Spins | Implemented and validated by design contract. |
| Free Spins no extra debit | Implemented in math and local RGS balance flow. |
| Vault Scatter ID `S` | Implemented. |
| Vault Scatter base trigger 3/4/5 = 8/12/15 FS | Implemented. |
| Vault Scatter free-spin retrigger 2/3/4/5 = +3/+5/+8/+12 FS | Implemented. |
| Legacy Key ID `H4` | Implemented. |
| Legacy Key target 10 | Implemented. |
| Keys collect only final settled paid Base/Scatter Boost boards | Math/RGS authority implemented; local RGS rewrites display events from session state. |
| Keys do not count Boot, Bonus Buy, or Free Spins | Implemented and tested. |
| Full Key meter gives one virtual Vault support credit | Implemented. |
| Credit consumes only when it creates/enhances valid Free Spins | Implemented and tested. |
| Diamond Seal multipliers highest-visible rule | Implemented and tested. |
| RTP 92% through 97% editions | Regenerated and validated in `RTP_PROFILE_VALIDATION.json`. |
| Disabled mechanics not marketed as active | Master GDD marks Decree/Vault Reel style mechanics as not implemented. |

## Validation Performed

Math and RGS:

```powershell
python games/2_0_The_Inheritance/dev_wild_substitution_test.py
python games/2_0_The_Inheritance/dev_design_contract_test.py
python games/2_0_The_Inheritance/dev_legacy_key_credit_test.py
python games/2_0_The_Inheritance/dev_rtp_profile_test.py
python games/2_0_The_Inheritance/dev_multiplier_test.py
python games/2_0_The_Inheritance/dev_sdk_smoke_test.py
python tools/the-inheritance-local-rgs/dev_local_rgs_bridge_test.py
python -m py_compile tools/the-inheritance-local-rgs/server.py tools/the-inheritance-local-rgs/dev_local_rgs_bridge_test.py
```

Generation:

```powershell
python games/2_0_The_Inheritance/run.py
python games/2_0_The_Inheritance/generate_rtp_profiles.py --profiles 92 93 94 95 96 97 --active-profile 97 --threads 10
```

Web:

```powershell
pnpm --filter the-inheritance build
```

Runtime:

- Vite dev server: `http://127.0.0.1:3007/`
- Local RGS health: `http://127.0.0.1:3008/health`
- Local page returned HTTP `200`.
- Local RGS health returned profile `rtp_97`, demo balance `$1,000.00`,
  Legacy Key target `10`.
- Local play requests for `base`, `scatter_boost`, and `bonus` returned settled
  event sequences and balance updates.
- Local replay returned the stored settled round by `roundID`.

## RTP Validation

The regenerated RTP report shows all modes in all profiles at target with tiny
floating point error and a max payout multiplier of `5000.0`.

Source:

- `games/2_0_The_Inheritance/docs/RTP_PROFILE_VALIDATION.json`

Active report summary:

- `rtp_92`: base, scatter boost, bonus all target `0.92`.
- `rtp_93`: base, scatter boost, bonus all target `0.93`.
- `rtp_94`: base, scatter boost, bonus all target `0.94`.
- `rtp_95`: base, scatter boost, bonus all target `0.95`.
- `rtp_96`: base, scatter boost, bonus all target `0.96`.
- `rtp_97`: base, scatter boost, bonus all target `0.97`.

## Stake Engine Readiness Notes

Official documentation checked:

- `https://stake-engine.com/docs/approval-guidelines`
- `https://stake-engine.com/docs/build-and-deploy`
- `https://stake-engine.com/docs/bet-replay`

Code-level alignment:

- Frontend and math remain separated.
- Frontend receives deterministic event data and does not calculate outcomes.
- Web build is static via SvelteKit adapter-static.
- Local demo RGS is development-only and does not change the production remote
  RGS request path.
- Replay support exists in the Web SDK path and now exists in the local demo
  bridge for settled local rounds.

Approval-sensitive business risk:

- The current Legacy Key meter is persistent across paid spins. Stake approval
  guidance surfaces stateless game expectations and restrictions around
  continuation-style behavior. The Key meter must be explicitly reviewed with
  Stake/provider approval. If persistent paid-spin progression is not allowed,
  the Release 1 design must either remove it or convert it into a same-round,
  fully book-contained mechanic.

This audit is not a formal Stake certification. Final approval still requires
submission-side review, jurisdiction settings, and the provider's approval
process.

## Remaining Known Gaps

- In-app browser console automation was not available in this Codex session, so
  browser-console inspection was not automated. HTTP/runtime checks passed.
- Generated `library/` book and lookup artifacts are intentionally ignored by
  Git. They were regenerated locally in this pass. Re-run the generation
  commands above before packaging a Math SDK submission from a fresh clone.
- Shared `envs` package build warnings remain for optional public deployment
  variables: `PUBLIC_SITE_MODE`, `PUBLIC_SENTRY_DSN`, and `PUBLIC_CHROMATIC`.
  These are warnings, not build failures.
- Runtime asset URL warnings remain for shared sample assets resolved at
  runtime. The production build completes.
- Local RGS replay cache is in memory only and resets when the bridge restarts.
- H5/H6 paytable order remains exactly as the plan states, including the unusual
  `3-kind = 2x`, `4-kind = 1x`, `5-kind = 20x` values.

## Final Position

The current codebase is aligned with the attached plan except for the
approval-sensitive question of persistent Legacy Key progression. The verified
math mismatch found in this audit, Wild substituting Legacy Keys, has been
fixed and regression tested.
