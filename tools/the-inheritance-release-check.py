"""Run the repeatable release-readiness proof for The Inheritance.

This script is intentionally narrow: it proves the math package, local RGS
bridge, frontend wiring, RTP binding, and build variants that are approval
critical before a provider submission package is prepared.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import time


REPO_ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = REPO_ROOT / "web-sdk"
WEB_APP_DIR = WEB_DIR / "apps" / "the-inheritance"

PYTHON_CHECKS = (
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

RTP_VALUES = ("0.92", "0.93", "0.94", "0.95", "0.96", "0.97")


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    printable = " ".join(shlex.quote(part) for part in command)
    print(f"\n$ {printable}", flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def resolve_pnpm_command() -> list[str] | None:
    configured = os.getenv("THE_INHERITANCE_PNPM_COMMAND")
    if configured:
        return shlex.split(configured)

    pnpm = shutil.which("pnpm")
    if pnpm:
        return [pnpm]

    windows_corepack = Path("D:/DevTools/node-v22.16.0-win-x64/corepack.cmd")
    if windows_corepack.is_file():
        return [str(windows_corepack), "pnpm"]

    return None


def resolve_node_tool_dir() -> Path | None:
    configured = os.getenv("THE_INHERITANCE_NODE_DIR")
    if configured:
        return Path(configured)

    node_path = shutil.which("node")
    if node_path:
        return Path(node_path).parent

    windows_node_dir = Path("D:/DevTools/node-v22.16.0-win-x64")
    if (windows_node_dir / "node.exe").is_file():
        return windows_node_dir

    return None


def run_python_checks() -> None:
    for check in PYTHON_CHECKS:
        run([sys.executable, check], cwd=REPO_ROOT)


def run_web_builds() -> None:
    pnpm = resolve_pnpm_command()
    if pnpm is None:
        raise RuntimeError(
            "pnpm was not found. Install Node/pnpm or set THE_INHERITANCE_PNPM_COMMAND."
        )

    base_env = os.environ.copy()
    base_env.setdefault("PUBLIC_SITE_MODE", "release-proof")
    base_env.setdefault("PUBLIC_SENTRY_DSN", "none")
    base_env.setdefault("PUBLIC_CHROMATIC", "false")
    base_env.setdefault("NPM_CONFIG_NODE_LINKER", "hoisted")
    base_env.setdefault("npm_config_node_linker", "hoisted")
    node_tool_dir = resolve_node_tool_dir()
    if node_tool_dir is not None:
        base_env["PATH"] = f"{node_tool_dir}{os.pathsep}{base_env.get('PATH', '')}"

    run_id = os.getenv("THE_INHERITANCE_RELEASE_RUN_ID") or time.strftime("%Y%m%d-%H%M%S")
    release_root = WEB_APP_DIR / "build-release" / f"proof-{run_id}"
    for rtp in RTP_VALUES:
        profile_slug = f"rtp_{round(float(rtp) * 100)}"
        output_dir = release_root / profile_slug
        if output_dir.exists():
            raise RuntimeError(f"Release proof output already exists: {output_dir}")
        env = base_env.copy()
        env["PUBLIC_THE_INHERITANCE_RTP"] = rtp
        env["THE_INHERITANCE_RELEASE_BUILD_DIR"] = str(output_dir)
        # Turbo honors the workspace dependency graph, so packages such as
        # pixi-svelte are built before the game consumes their dist output.
        run([*pnpm, "exec", "turbo", "run", "build", "--filter=the-inheritance"], cwd=WEB_DIR, env=env)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-web-builds",
        action="store_true",
        help="Run Python/static release proof only. CI must not use this for final release proof.",
    )
    parser.add_argument(
        "--web-builds-only",
        action="store_true",
        help="Run only the frontend RTP build matrix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.web_builds_only:
        run_python_checks()
    if not args.skip_web_builds:
        run_web_builds()
    print("\nThe Inheritance release-readiness proof: OK", flush=True)


if __name__ == "__main__":
    main()
