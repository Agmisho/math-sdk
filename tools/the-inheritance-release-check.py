"""Run a deterministic release proof for The Inheritance."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web-sdk"
APP_DIR = WEB_DIR / "apps" / "the-inheritance"
RELEASE_BUILD_ROOT = APP_DIR / "build-release"
SUBMISSION_PROFILE = "rtp_97"
SUBMISSION_RTP = "0.97"
CHECK_TIMEOUT_SECONDS = 300
FRONTEND_BUILD_TIMEOUT_SECONDS = 720

CHECKS = (
    "games/2_0_The_Inheritance/tools/validate_release_packages.py",
    "games/2_0_The_Inheritance/dev_design_contract_test.py",
    "games/2_0_The_Inheritance/dev_legacy_key_credit_test.py",
    "games/2_0_The_Inheritance/dev_multiplier_test.py",
    "games/2_0_The_Inheritance/dev_rtp_profile_test.py",
    "games/2_0_The_Inheritance/dev_static_release_artifact_test.py",
    "games/2_0_The_Inheritance/dev_sdk_smoke_test.py",
    "games/2_0_The_Inheritance/dev_vault_reel_feature_test.py",
    "games/2_0_The_Inheritance/dev_wild_substitution_test.py",
    "tools/the-inheritance-local-rgs/dev_local_rgs_bridge_test.py",
    "web-sdk/apps/the-inheritance/dev_frontend_audit_test.py",
    "web-sdk/apps/the-inheritance/dev_release_asset_qa_test.py",
)


def _popen_group_kwargs() -> dict:
    if os.name == "nt":
        return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    return {"start_new_session": True}


def _terminate_process_group(process: subprocess.Popen) -> None:
    """Stop the complete child-process tree created for one command."""
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

    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            os.killpg(process.pid, 0)
        except ProcessLookupError:
            return
        time.sleep(0.1)

    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def run_command(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout_seconds: int,
) -> None:
    print("$ " + " ".join(command), flush=True)
    process = subprocess.Popen(command, cwd=cwd, env=env, **_popen_group_kwargs())
    try:
        return_code = process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        _terminate_process_group(process)
        raise RuntimeError(
            f"Command exceeded its {timeout_seconds}-second limit: {' '.join(command)}"
        ) from exc

    # A successful parent command must not leave a child process holding the CI
    # step open. This is a no-op when the process group is already gone.
    _terminate_process_group(process)
    if return_code:
        raise subprocess.CalledProcessError(return_code, command)


def selected_output_dir() -> Path:
    configured = os.getenv("THE_INHERITANCE_RELEASE_BUILD_DIR")
    output_dir = Path(configured) if configured else RELEASE_BUILD_ROOT / "local-rtp_97"
    output_dir = output_dir.resolve()
    allowed_root = RELEASE_BUILD_ROOT.resolve()
    if not output_dir.is_relative_to(allowed_root):
        raise RuntimeError(f"Release output must stay under {allowed_root}: {output_dir}")
    return output_dir


def validate_static_output(output_dir: Path) -> None:
    index_html = output_dir / "index.html"
    app_dir = output_dir / "_app"
    if not index_html.is_file() or not app_dir.is_dir() or not any(app_dir.rglob("*.js")):
        raise RuntimeError("Frontend build did not produce a complete static site.")
    for item in output_dir.rglob("*"):
        if item.is_symlink():
            raise RuntimeError(f"Submission frontend cannot contain symlinks: {item}")

    proof = {
        "gameName": "The Inheritance",
        "profile": SUBMISSION_PROFILE,
        "rtp": float(SUBMISSION_RTP),
        "staticOutput": str(output_dir),
        "validated": True,
    }
    (output_dir / "release-proof.json").write_text(
        json.dumps(proof, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def run_static_checks() -> None:
    for check in CHECKS:
        run_command(
            [sys.executable, check],
            cwd=ROOT,
            timeout_seconds=CHECK_TIMEOUT_SECONDS,
        )


def build_submission_frontend() -> None:
    pnpm = shutil.which("pnpm")
    if not pnpm:
        raise RuntimeError("pnpm was not found on PATH")

    output_dir = selected_output_dir()
    if output_dir.exists():
        shutil.rmtree(output_dir)

    env = os.environ.copy()
    env.update(
        {
            "CI": "true",
            "PUBLIC_SITE_MODE": "release-proof",
            "PUBLIC_SENTRY_DSN": "none",
            "PUBLIC_CHROMATIC": "false",
            "PUBLIC_THE_INHERITANCE_RTP": SUBMISSION_RTP,
            "THE_INHERITANCE_RELEASE_BUILD_DIR": str(output_dir),
            "NPM_CONFIG_NODE_LINKER": "hoisted",
        }
    )

    # Turbo builds the official workspace dependency graph before the game.
    run_command(
        [pnpm, "exec", "turbo", "run", "build", "--filter=the-inheritance"],
        cwd=WEB_DIR,
        env=env,
        timeout_seconds=FRONTEND_BUILD_TIMEOUT_SECONDS,
    )
    validate_static_output(output_dir)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-web-build", action="store_true")
    parser.add_argument("--web-build-only", action="store_true")
    args = parser.parse_args()

    if not args.web_build_only:
        run_static_checks()
    if not args.skip_web_build:
        build_submission_frontend()
    print("The Inheritance release proof: OK", flush=True)


if __name__ == "__main__":
    main()
