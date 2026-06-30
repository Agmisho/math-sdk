# The Inheritance QA Test Matrix

This matrix records the minimum release proof expected before provider review. The Math SDK remains the authority for outcomes, RTP, books, lookup weights, Legacy Key state, and replay payloads.

## Automated Gates

| Area | Command | Required result |
| --- | --- | --- |
| RTP upload packages | `python games/2_0_The_Inheritance/tools/validate_release_packages.py` | Every `release/rtp_92` through `release/rtp_97` folder is self-contained and hash-validated. |
| Static math artifacts | `python games/2_0_The_Inheritance/dev_static_release_artifact_test.py` | Committed artifact manifest matches generated release folders. |
| Local RGS contract | `python tools/the-inheritance-local-rgs/dev_local_rgs_bridge_test.py` | Release RTP binding, insufficient balance, authoritative Keys, and persistent replay pass. |
| Frontend contract | `python web-sdk/apps/the-inheritance/dev_frontend_audit_test.py` | RTP verification, replay blocking, Key display authority, and critical UI guards pass. |
| Full release proof | `python tools/the-inheritance-release-check.py` | All Python checks and all six frontend RTP builds pass. |
| Browser smoke | `cd web-sdk && pnpm --filter the-inheritance e2e-smoke` | Desktop canvas renders, session config resolves, no red console errors, audio assets resolve. |
| Mobile smoke | `cd web-sdk && pnpm --filter the-inheritance e2e-mobile` | Portrait viewport renders without blank canvas or console errors. |

## Manual Release Checks

| Scenario | Desktop | Mobile portrait | Evidence |
| --- | --- | --- | --- |
| Game opens from fresh session | Required | Required | Screenshot plus console log. |
| Base spin debits once | Required | Required | Balance before/after and round ID. |
| Zero balance blocks spin | Required | Required | Console clean, no replay row, no balance/key mutation. |
| Scatter Boost uses server mode | Required | Optional | RGS round mode and cost. |
| Bonus Buy uses server mode | Required | Optional | RGS round mode, cost, 10 free spins. |
| Legacy Key meter | Required | Required | `collectionUpdate.collected` drives display; no frontend recount. |
| Replay URL | Required | Optional | `?replayRound=<roundID>` shows replay label and blocks betting. |
| Audio | Required | Optional | Main loop starts after user gesture; spin/scatter sounds play at controlled volume. |
| Performance | Required | Required | No blank frames; no sustained long tasks during 10 spins. |

## Release Blockers

- Any RTP folder missing `index.json`, `manifest.json`, the three books, or the three lookup tables.
- Any frontend path that lets URL params, localStorage, or UI choose RTP.
- Any replay route that changes balance, spin index, Key progress, or free spin state.
- Any Key meter update that is not sourced from the RGS `collectionUpdate.collected` value.
- Any browser console red error, blank canvas, or missing audio asset in the release smoke tests.
