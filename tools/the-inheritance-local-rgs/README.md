# The Inheritance Local RGS Bridge

This development-only service keeps the Math SDK and web SDK separated while
allowing the local frontend to play real deterministic Math SDK results.

Run from the repository root:

```powershell
python tools/the-inheritance-local-rgs/server.py
```

The local demo balance is kept in a separate file:

```text
tools/the-inheritance-local-rgs/demo_settings.py
```

By default the demo starts with `$1,000.00`. This setting is local-development
only; it is not imported by the production web SDK path or by the Math SDK
submission.

The bridge listens on `http://127.0.0.1:3008`. When the frontend has no
`rgs_url` query parameter, `rgs-requests` uses this local endpoint. When Stake
provides an RGS URL, the normal remote request path is used unchanged.

The bridge stores settled rounds in memory for the current process and supports
local replay through:

```text
GET /bet/replay/:game/:version/:mode/:roundID
```

This is for local Web SDK replay testing only. Restarting the bridge clears the
local replay cache.

The bridge is not part of either Stake submission. The Math SDK remains under
`games/2_0_The_Inheritance`; the frontend receives only settled round events.
