"""Release proof that produces the RTP 97 static frontend for Stake upload."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "web-sdk" / "apps" / "the-inheritance"
REQUIRED_ASSETS = (
    Path("assets/the-inheritance/ui/loader.png"),
    Path("assets/the-inheritance/audio/main-theme.mp3"),
    Path("assets/the-inheritance/audio/spin.mp3"),
    Path("assets/the-inheritance/audio/scatter-landing.mp3"),
)
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


def run(command: list[str], timeout: int = 300) -> None:
    print("$ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True, timeout=timeout)


def static_output() -> Path:
    value = os.environ.get("THE_INHERITANCE_RELEASE_BUILD_DIR")
    if not value:
        raise RuntimeError("THE_INHERITANCE_RELEASE_BUILD_DIR is required")
    output = Path(value).resolve()
    if not output.is_relative_to((APP_DIR / "build-release").resolve()):
        raise RuntimeError("Release output must remain inside the game build-release directory")
    return output


def validate_output(output: Path) -> None:
    if not (output / "index.html").is_file():
        raise RuntimeError("Generated frontend is missing index.html")
    if not (output / "_app").is_dir() or not any((output / "_app").rglob("*.js")):
        raise RuntimeError("Generated frontend is missing compiled app JavaScript")
    for relative in REQUIRED_ASSETS:
        asset = output / relative
        if not asset.is_file() or asset.stat().st_size <= 1024:
            raise RuntimeError(f"Generated frontend is missing required asset: {relative}")
    if any(path.is_symlink() for path in output.rglob("*")):
        raise RuntimeError("Generated frontend contains a symlink")

    (output / "release-proof.json").write_text(
        json.dumps(
            {
                "gameName": "The Inheritance",
                "profile": "rtp_97",
                "rtp": 0.97,
                "validated": True,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    for check in CHECKS:
        run([sys.executable, check])
    run([sys.executable, "tools/the-inheritance-runtime-build.py"], timeout=780)
    validate_output(static_output())
    print("The Inheritance release proof: OK", flush=True)


if __name__ == "__main__":
    main()
