# The Inheritance Local RGS Bridge

This development-only service keeps the Math SDK and web SDK separated while
allowing the local frontend to play real deterministic Math SDK results.

Run from the repository root:

```powershell
python tools/the-inheritance-local-rgs/server.py
```

The bridge listens on `http://127.0.0.1:3008`. When the frontend has no
`rgs_url` query parameter, `rgs-requests` uses this local endpoint. When Stake
provides an RGS URL, the normal remote request path is used unchanged.

The bridge is not part of either Stake submission. The Math SDK remains under
`games/2_0_The_Inheritance`; the frontend receives only settled round events.
