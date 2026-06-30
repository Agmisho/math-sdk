"""Release proof for The Inheritance."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web-sdk"
APP_DIR = WEB_DIR / "apps" / "the-inheritance"
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
RTP_VALUES = ("0.92", "0.93", "0.94", "0.95", "0.96", "0.97")


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> None:
    print("$ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def build_frontends() -> None:
    pnpm = shutil.which("pnpm")
    if not pnpm:
        raise RuntimeError("pnpm was not found")
    base_env = os.environ.copy()
    base_env.setdefault("PUBLIC_SITE_MODE", "release-proof")
    base_env.setdefault("PUBLIC_SENTRY_DSN", "none")
    base_env.setdefault("PUBLIC_CHROMATIC", "false")
    base_env.setdefault("NPM_CONFIG_NODE_LINKER", "hoisted")
    run_id = os.getenv("THE_INHERITANCE_RELEASE_RUN_ID") or time.strftime("%Y%m%d-%H%M%S")
    release_root = APP_DIR / "build-release" / f"proof-{run_id}"
    for rtp in RTP_VALUES:
        output_dir = release_root / f"rtp_{round(float(rtp) * 100)}"
        env = base_env.copy()
        env["PUBLIC_THE_INHERITANCE_RTP"] = rtp
        env["THE_INHERITANCE_RELEASE_BUILD_DIR"] = str(output_dir)
        run([pnpm, "--filter", "the-inheritance", "build"], WEB_DIR, env)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-web-builds", action="store_true")
    parser.add_argument("--web-builds-only", action="store_true")
    args = parser.parse_args()
    if not args.web_builds_only:
        for check in CHECKS:
            run([sys.executable, check], ROOT)
    if not args.skip_web_builds:
        build_frontends()
    print("The Inheritance release proof: OK", flush=True)


if __name__ == "__main__":
    main()
