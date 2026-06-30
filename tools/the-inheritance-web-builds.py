"""Build isolated Stake Engine frontend artifacts for The Inheritance."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web-sdk"
APP_DIR = WEB_DIR / "apps" / "the-inheritance"
RTP_VALUES = ("0.92", "0.93", "0.94", "0.95", "0.96", "0.97")


def run(command: list[str], env: dict[str, str]) -> None:
    print("$ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=WEB_DIR, env=env, check=True)


def main() -> None:
    pnpm = shutil.which("pnpm")
    if not pnpm:
        raise RuntimeError("pnpm was not found on PATH")

    base_env = os.environ.copy()
    base_env.setdefault("PUBLIC_SITE_MODE", "release-proof")
    base_env.setdefault("PUBLIC_SENTRY_DSN", "none")
    base_env.setdefault("PUBLIC_CHROMATIC", "false")
    base_env.setdefault("NPM_CONFIG_NODE_LINKER", "hoisted")
    base_env.setdefault("npm_config_node_linker", "hoisted")

    # Shared library packages must build without the game-specific output path.
    shared_env = base_env.copy()
    shared_env.pop("PUBLIC_THE_INHERITANCE_RTP", None)
    shared_env.pop("THE_INHERITANCE_RELEASE_BUILD_DIR", None)
    run([pnpm, "exec", "turbo", "run", "build", "--filter=the-inheritance"], shared_env)

    run_id = os.getenv("THE_INHERITANCE_RELEASE_RUN_ID") or time.strftime("%Y%m%d-%H%M%S")
    release_root = APP_DIR / "build-release" / f"proof-{run_id}"
    for rtp in RTP_VALUES:
        profile = f"rtp_{round(float(rtp) * 100)}"
        output_dir = release_root / profile
        if output_dir.exists():
            raise RuntimeError(f"Release output already exists: {output_dir}")
        game_env = base_env.copy()
        game_env["PUBLIC_THE_INHERITANCE_RTP"] = rtp
        game_env["THE_INHERITANCE_RELEASE_BUILD_DIR"] = str(output_dir)
        run([pnpm, "--filter", "the-inheritance", "build"], game_env)


if __name__ == "__main__":
    main()
