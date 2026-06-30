"""Serve a generated The Inheritance static frontend for Playwright CI."""

from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path


HOST = "127.0.0.1"
PORT = int(os.getenv("THE_INHERITANCE_STATIC_PORT", "3007"))
static_dir_value = os.getenv("THE_INHERITANCE_E2E_STATIC_DIR")
if not static_dir_value:
    raise RuntimeError("THE_INHERITANCE_E2E_STATIC_DIR must point to the generated frontend.")

STATIC_DIR = Path(static_dir_value).resolve()
if not (STATIC_DIR / "index.html").is_file():
    raise RuntimeError(f"Generated frontend is missing index.html: {STATIC_DIR}")


class StaticFrontendHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), StaticFrontendHandler)
    print(f"Serving {STATIC_DIR} at http://{HOST}:{PORT}", flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
