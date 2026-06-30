"""Write a machine-readable release proof summary for CI artifacts."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
GAME_DIR = REPO_ROOT / "games" / "2_0_The_Inheritance"
RELEASE_DIR = GAME_DIR / "release"
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
SUMMARY_PATH = ARTIFACTS_DIR / "the-inheritance-ci-summary.json"


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    root_manifest = read_json(RELEASE_DIR / "manifest.json")
    profiles = []
    for profile in root_manifest["profiles"]:
        manifest = read_json(RELEASE_DIR / profile / "manifest.json")
        root_package = next(
            entry
            for entry in root_manifest["packages"]
            if entry["profile"] == profile
        )
        profiles.append(
            {
                "profile": profile,
                "rtp": manifest["rtp"],
                "manifestSha256": root_package["manifestSha256"],
                "files": sorted(manifest["files"]),
            }
        )

    summary = {
        "gameId": root_manifest["gameId"],
        "gameName": root_manifest["gameName"],
        "status": "release-proof-passed",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "commit": os.getenv("GITHUB_SHA", "local"),
        "runId": os.getenv("GITHUB_RUN_ID", "local"),
        "profiles": profiles,
        "proofCommands": [
            "python games/2_0_The_Inheritance/tools/validate_release_packages.py",
            "python games/2_0_The_Inheritance/dev_static_release_artifact_test.py",
            "python tools/the-inheritance-local-rgs/dev_local_rgs_bridge_test.py",
            "python web-sdk/apps/the-inheritance/dev_frontend_audit_test.py",
            "python tools/the-inheritance-release-check.py",
        ],
    }

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    with SUMMARY_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"Wrote {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
