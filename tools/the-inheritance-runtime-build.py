"""Build the runtime dependency and static frontend needed for submission."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import signal
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web-sdk"
PIXI_DIR = WEB_DIR / "packages" / "pixi-svelte"


def _popen_group_kwargs() -> dict:
    if os.name == "nt":
        return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    return {"start_new_session": True}


def _stop_process_tree(process: subprocess.Popen) -> None:
    """Terminate a command and all child processes it created."""
    if process.poll() is not None:
        return

    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return

    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=5)


def run(command: list[str], env: dict[str, str], timeout: int) -> None:
    print("$ " + " ".join(command), flush=True)
    process = subprocess.Popen(command, cwd=WEB_DIR, env=env, **_popen_group_kwargs())
    try:
        return_code = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        _stop_process_tree(process)
        raise RuntimeError(f"Command timed out after {timeout}s: {' '.join(command)}") from exc
    if return_code:
        raise subprocess.CalledProcessError(return_code, command)


def static_site_ready(output_dir: Path) -> bool:
    app_dir = output_dir / "_app"
    return (output_dir / "index.html").is_file() and app_dir.is_dir() and any(app_dir.rglob("*.js"))


def run_app_build(command: list[str], env: dict[str, str], output_dir: Path, timeout: int) -> None:
    """Build the app and clean up pnpm only after a complete static site exists."""
    print("$ " + " ".join(command), flush=True)
    process = subprocess.Popen(command, cwd=WEB_DIR, env=env, **_popen_group_kwargs())
    deadline = time.monotonic() + timeout
    ready_at: float | None = None

    while True:
        return_code = process.poll()
        if return_code is not None:
            if return_code:
                raise subprocess.CalledProcessError(return_code, command)
            return

        if static_site_ready(output_dir):
            if ready_at is None:
                ready_at = time.monotonic()
            elif time.monotonic() - ready_at >= 10:
                _stop_process_tree(process)
                print(
                    "Static site is complete and stable; stopped leftover pnpm process tree.",
                    flush=True,
                )
                return

        if time.monotonic() >= deadline:
            complete = static_site_ready(output_dir)
            _stop_process_tree(process)
            if complete:
                print(
                    "Static site is complete after command timeout; stopped leftover pnpm process tree.",
                    flush=True,
                )
                return
            raise RuntimeError(f"App build timed out after {timeout}s before static output was complete")

        time.sleep(1)


def main() -> None:
    pnpm = shutil.which("pnpm")
    if not pnpm:
        raise RuntimeError("pnpm was not found on PATH")

    env = os.environ.copy()
    env.setdefault("NPM_CONFIG_NODE_LINKER", "hoisted")
    env.setdefault("CI", "true")

    output_value = env.get("THE_INHERITANCE_RELEASE_BUILD_DIR")
    if not output_value:
        raise RuntimeError("THE_INHERITANCE_RELEASE_BUILD_DIR is required")
    output_dir = Path(output_value).resolve()

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

    run_app_build(
        [pnpm, "--filter", "the-inheritance", "run", "build"],
        env,
        output_dir,
        480,
    )


if __name__ == "__main__":
    main()
