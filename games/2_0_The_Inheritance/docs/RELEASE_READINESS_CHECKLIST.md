# The Inheritance Release Readiness Checklist

This checklist is the current provider-review gate for The Inheritance. It is
not a submission approval. Submit only after every automated and manual evidence
item below is complete.

## Automated release proof

Run from the repository root:

```powershell
python tools/the-inheritance-release-check.py
```

This executes:

- Math SDK design, multiplier, wild substitution, Vault Reel, Legacy Key, RTP,
  SDK smoke, and static artifact checks.
- Local RGS bridge checks, including selected RTP profile binding, process-local
  replay, HTTP replay route, insufficient-balance rejection, payout scaling, and
  authoritative Legacy Key collection updates.
- Frontend static wiring checks for insufficient-balance protection, Legacy Key
  display authority, build-time RTP display binding, and feature presenters.
- Frontend static asset checks for the themed loader, custom main music, spin
  sound, and scatter landing sound.
- Web builds for every approved frontend RTP value:
  `0.92`, `0.93`, `0.94`, `0.95`, `0.96`, and `0.97`.

The same proof is wired into:

```text
.github/workflows/the-inheritance-release.yml
```

## RTP binding gate

- Math/RGS profile selection is server-side through `THE_INHERITANCE_RTP`.
- Frontend display binding is build-time through `PUBLIC_THE_INHERITANCE_RTP`.
- `PUBLIC_THE_INHERITANCE_RTP` must match the RTP profile folder being
  submitted.
- RTP is not player-selectable and must not change during a session.

Example 92% local proof:

```powershell
$env:THE_INHERITANCE_RTP='92'
$env:PUBLIC_THE_INHERITANCE_RTP='0.92'
python tools/the-inheritance-local-rgs/server.py
cd web-sdk
pnpm --filter the-inheritance build
```

## Local replay gate

The development bridge supports replay for the current process through:

```text
GET /bet/replay/:game/:version/:mode/:roundID
GET /bet/replay?roundID=:roundID
```

Replay is local QA only. Restarting the bridge clears process-local rounds. Do
not describe this bridge as a production RGS persistence model.

## Legacy Key approval gate

The current design uses persistent Legacy Key progress as a virtual scatter
credit. This must receive written Stake/provider approval before submission.

Until that written position exists, submission status remains:

```text
Not ready
```

If Stake rejects persistent Legacy Key state, the feature must be changed to a
single-round deterministic math event or removed from the submission profile.

## Browser, mobile, audio, and performance evidence

Attach evidence for each selected RTP release candidate:

- Desktop browser smoke: game opens, no red console errors, 10 spins, win, loss,
  bonus trigger, Bonus Buy, Scatter Boost, Info, Auto, replay URL.
- Mobile portrait smoke: game opens, layout fits, UI buttons clickable, no
  overlap, no red console errors.
- Audio smoke: main background music, low-volume spin, scatter landing sound,
  mute/unmute, no missing-audio crash.
- Performance smoke: initial load, spin animation, win animation, free-spin
  intro/outro, no sustained frame drops or memory growth observed.

Store screenshots, console logs, and command output with the release notes. The
automated proof confirms assets and builds; this manual browser evidence is
still required before provider submission.

## Current release position

Do not submit yet unless all items below are true:

- Automated release proof passes in CI.
- Correct RTP profile folder is selected and matches the built frontend RTP.
- Stake/provider written position on persistent Legacy Keys is available.
- Local replay evidence is attached.
- Browser, mobile, audio, and performance evidence is attached.
