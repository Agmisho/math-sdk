"""Build the runtime dependency and static frontend needed for submission."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web-sdk"
PIXI_DIR = WEB_DIR / "packages" / "pixi-svelte"


def run(command: list[str], env: dict[str, str], timeout: int) -> None:
    print("$ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=WEB_DIR, env=env, check=True, timeout=timeout)


def main() -> None:
    pnpm = shutil.which("pnpm")
    if not pnpm:
        raise RuntimeError("pnpm was not found on PATH")

    env = os.environ.copy()
    env.setdefault("NPM_CONFIG_NODE_LINKER", "hoisted")
    env.setdefault("CI", "true")

    dist_dir = PIXI_DIR / "dist"
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    # Runtime output is required by the game. Type declarations are required
    # only when publishing pixi-svelte itself, not for the static game upload.
    run(
        [pnpm, "--filter", "pixi-svelte", "exec", "svelte-package", "--types=false"],
        env,
        240,
    )
    if not (dist_dir / "index.js").is_file():
        raise RuntimeError("pixi-svelte did not produce dist/index.js")

    run([pnpm, "--filter", "the-inheritance", "run", "build"], env, 480)


if __name__ == "__main__":
    main()
