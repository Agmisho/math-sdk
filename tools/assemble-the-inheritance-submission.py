"""Create the complete RTP 96 Stake submission bundle for The Inheritance."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = ROOT / "games" / "2_0_The_Inheritance"
MATH_SOURCE = GAME_DIR / "release" / "rtp_96"
ARTIFACT_ROOT = ROOT / "artifacts" / "the-inheritance-submission-rtp96"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def directory_index(directory: Path) -> list[dict[str, int | str]]:
    files = []
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise RuntimeError(f"Submission bundle cannot contain symlinks: {path}")
        if path.is_file():
            files.append(
                {
                    "path": path.relative_to(directory).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
    return files


def verify_math_source(manifest: dict) -> None:
    if manifest.get("gameId") != "2_0_The_Inheritance":
        raise RuntimeError("Unexpected math game ID")
    if manifest.get("gameName") != "The Inheritance":
        raise RuntimeError("Unexpected math game name")
    if manifest.get("profile") != "rtp_96" or manifest.get("rtp") != 96:
        raise RuntimeError("Submission math package is not rtp_96")
    for relative_path, details in manifest["files"].items():
        source = MATH_SOURCE / relative_path
        if not source.is_file() or sha256_file(source) != details["sha256"]:
            raise RuntimeError(f"Math package hash validation failed: {relative_path}")


def main() -> None:
    frontend_value = os.getenv("THE_INHERITANCE_RELEASE_BUILD_DIR")
    if not frontend_value:
        raise RuntimeError("THE_INHERITANCE_RELEASE_BUILD_DIR is required")
    frontend_source = Path(frontend_value).resolve()
    if not (frontend_source / "index.html").is_file() or not (frontend_source / "_app").is_dir():
        raise RuntimeError("Generated rtp_96 frontend is incomplete")

    with (MATH_SOURCE / "manifest.json").open(encoding="utf-8") as source:
        math_manifest = json.load(source)
    verify_math_source(math_manifest)

    if ARTIFACT_ROOT.exists():
        shutil.rmtree(ARTIFACT_ROOT)
    math_target = ARTIFACT_ROOT / "math"
    frontend_target = ARTIFACT_ROOT / "frontend"
    shutil.copytree(MATH_SOURCE, math_target, symlinks=False)
    shutil.copytree(frontend_source, frontend_target, symlinks=False)

    bundle_manifest = {
        "schemaVersion": 1,
        "gameId": "2_0_The_Inheritance",
        "gameName": "The Inheritance",
        "profile": "rtp_96",
        "rtp": 96,
        "commit": os.getenv("GITHUB_SHA", "local"),
        "math": directory_index(math_target),
        "frontend": directory_index(frontend_target),
    }
    with (ARTIFACT_ROOT / "submission-manifest.json").open("w", encoding="utf-8", newline="\n") as target:
        json.dump(bundle_manifest, target, indent=2, sort_keys=True)
        target.write("\n")

    (ARTIFACT_ROOT / "README.txt").write_text(
        "The Inheritance — Stake submission bundle\n\n"
        "math/ contains the rtp_96 Math SDK release package.\n"
        "frontend/ contains the matching generated static frontend.\n"
        "submission-manifest.json records hashes for both deliverables.\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Created {ARTIFACT_ROOT}")


if __name__ == "__main__":
    main()
