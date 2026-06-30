# The Inheritance Manual QA Evidence

Use this file for each release candidate. Attach screenshots, browser console exports, RGS health output, and replay round IDs to the release ticket or CI artifact.

## Build Under Test

| Field | Value |
| --- | --- |
| Commit | TBD |
| RTP profile | TBD |
| Frontend URL | TBD |
| Local RGS URL | `http://127.0.0.1:3008` |
| Date | TBD |
| Tester | TBD |

## Evidence Checklist

| Check | Result | Evidence location |
| --- | --- | --- |
| Desktop fresh load, no red console errors | TBD | TBD |
| Mobile portrait fresh load, no red console errors | TBD | TBD |
| 10 normal spins complete | TBD | TBD |
| Losing spin | TBD | TBD |
| Winning spin | TBD | TBD |
| Minimum bet | TBD | TBD |
| Maximum bet | TBD | TBD |
| Zero balance or insufficient balance blocked | TBD | TBD |
| Stop during spin | TBD | TBD |
| Turbo speed | TBD | TBD |
| Auto spin | TBD | TBD |
| Scatter Boost | TBD | TBD |
| Bonus Buy | TBD | TBD |
| Natural 3+ Vault scatter trigger | TBD | TBD |
| Legacy Key collection from settled RGS event | TBD | TBD |
| Legacy Key credit with 2+ natural Vaults | TBD | TBD |
| Replay URL does not mutate state | TBD | TBD |
| Main music, spin sound, scatter sound | TBD | TBD |
| Performance during 10 spins | TBD | TBD |

## Notes

- Record the `/game/session-config` response for every release run.
- Record the replay database path from `/health`; do not commit the SQLite database.
- Use RGS round IDs in the evidence so any visual result can be replayed through `?replayRound=<roundID>`.
