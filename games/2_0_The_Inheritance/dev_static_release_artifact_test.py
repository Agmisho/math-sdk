"""Validate The Inheritance static release artifact package.

This check is intentionally deterministic. Run with ``--write`` after
regenerating RTP editions to refresh the committed manifest; run without
arguments in audit/CI to prove the tracked package still matches that manifest.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


GAME_DIR = Path(__file__).resolve().parent
LIBRARY_DIR = GAME_DIR / "library"
PUBLISH_DIR = LIBRARY_DIR / "publish_files"
PROFILE_ROOT = LIBRARY_DIR / "rtp_profiles"
CONFIG_DIR = LIBRARY_DIR / "configs"
RELEASE_DIR = GAME_DIR / "release"
DOCS_DIR = GAME_DIR / "docs"
RTP_VALIDATION_PATH = DOCS_DIR / "RTP_PROFILE_VALIDATION.json"
MANIFEST_PATH = DOCS_DIR / "STATIC_RELEASE_ARTIFACT_MANIFEST.json"

GAME_ID = "2_0_The_Inheritance"
MODES = ("base", "scatter_boost", "bonus")
PROFILES = tuple(range(92, 98))
MODE_COSTS = {"base": 1.0, "scatter_boost": 3.0, "bonus": 100.0}
MAX_PAYOUT_MULTIPLIER = 5000.0
RTP_TOLERANCE = 1e-8


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def required_file(path: Path) -> Path:
    if not path.is_file():
        raise AssertionError(f"Missing required release artifact: {path}")
    return path


def file_entry(path: Path) -> dict[str, Any]:
    required_file(path)
    return {
        "path": path.relative_to(GAME_DIR).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def read_json(path: Path) -> Any:
    required_file(path)
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def index_modes(index_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    modes = index_data.get("modes", [])
    result = {mode.get("name"): mode for mode in modes}
    missing = [mode for mode in MODES if mode not in result]
    if missing:
        raise AssertionError(f"Release index missing modes: {missing}")
    return result


def lookup_metrics(path: Path, cost: float) -> dict[str, float | int]:
    total_weight = 0
    weighted_payout = 0.0
    hit_weight = 0
    max_payout = 0.0
    rows = 0

    with required_file(path).open(newline="", encoding="utf-8") as handle:
        for book_id, weight, payout_cents in csv.reader(handle):
            del book_id
            parsed_weight = int(weight)
            payout = int(payout_cents) / 100
            total_weight += parsed_weight
            weighted_payout += parsed_weight * payout
            if payout > 0:
                hit_weight += parsed_weight
            max_payout = max(max_payout, payout)
            rows += 1

    if total_weight <= 0:
        raise AssertionError(f"Lookup table has no positive total weight: {path}")

    return {
        "rows": rows,
        "rtp": weighted_payout / total_weight / cost,
        "hitRate": hit_weight / total_weight,
        "maxPayoutMultiplier": max_payout,
        "totalWeight": total_weight,
    }


def assert_lookup_matches_report(profile: dict[str, Any], profile_dir: Path) -> None:
    for mode in MODES:
        mode_report = profile["modes"][mode]
        cost = MODE_COSTS[mode]
        metrics = lookup_metrics(profile_dir / f"lookUpTable_{mode}_0.csv", cost)

        if abs(float(metrics["rtp"]) - float(mode_report["rtp"])) > RTP_TOLERANCE:
            raise AssertionError(f"{profile['profile']} {mode} RTP differs from validation report.")
        if abs(float(mode_report["rtp"]) - float(mode_report["targetRtp"])) > RTP_TOLERANCE:
            raise AssertionError(f"{profile['profile']} {mode} does not match target RTP.")
        if float(metrics["maxPayoutMultiplier"]) > MAX_PAYOUT_MULTIPLIER:
            raise AssertionError(f"{profile['profile']} {mode} exceeds {MAX_PAYOUT_MULTIPLIER}x cap.")


def assert_profile_books(profile_name: str, profile_dir: Path) -> list[dict[str, Any]]:
    files = []
    for mode in MODES:
        book_name = f"books_{mode}.jsonl.zst"
        profile_book = profile_dir / book_name
        source_book = PUBLISH_DIR / book_name
        if sha256(profile_book) != sha256(source_book):
            raise AssertionError(f"{profile_name} {book_name} differs from shared source books.")
        files.append(file_entry(profile_book))
    return files


def assert_release_manifest() -> dict[str, Any]:
    manifest = read_json(RELEASE_DIR / "manifest.json")
    expected_profiles = [f"rtp_{percentage}" for percentage in PROFILES]
    if manifest.get("profiles") != expected_profiles:
        raise AssertionError("Release manifest does not list every RTP package in order.")
    return file_entry(RELEASE_DIR / "manifest.json")


def assert_release_package(profile_name: str, profile_dir: Path) -> dict[str, Any]:
    package_dir = RELEASE_DIR / profile_name
    package_index = read_json(package_dir / "index.json")
    package_manifest = read_json(package_dir / "manifest.json")
    profile_index = read_json(profile_dir / "index.json")
    if package_index != profile_index:
        raise AssertionError(f"{profile_name} release index does not match RTP profile index.")
    if package_manifest.get("profile") != profile_name:
        raise AssertionError(f"{profile_name} release manifest profile mismatch.")

    files = [file_entry(package_dir / "index.json"), file_entry(package_dir / "manifest.json")]
    expected_names = {"index.json", "manifest.json"}
    modes = index_modes(package_index)
    for mode in MODES:
        mode_entry = modes[mode]
        books_name = mode_entry["events"]
        lookup_name = mode_entry["weights"]
        for referenced_name in (books_name, lookup_name):
            if Path(referenced_name).name != referenced_name:
                raise AssertionError(
                    f"{profile_name} {mode} references a non-local artifact: {referenced_name}"
                )

        package_lookup = package_dir / lookup_name
        profile_lookup = profile_dir / lookup_name
        if sha256(package_lookup) != sha256(profile_lookup):
            raise AssertionError(f"{profile_name} {mode} release lookup differs from RTP profile.")

        package_books = package_dir / books_name
        source_books = PUBLISH_DIR / books_name
        if sha256(package_books) != sha256(source_books):
            raise AssertionError(f"{profile_name} {mode} release books differ from shared source books.")

        expected_names.update((lookup_name, books_name))
        files.append(file_entry(package_lookup))
        files.append(file_entry(package_books))

    actual_names = {path.name for path in package_dir.iterdir() if path.is_file()}
    if actual_names != expected_names:
        raise AssertionError(
            f"{profile_name} release folder must contain exactly {sorted(expected_names)}, "
            f"found {sorted(actual_names)}"
        )

    return {
        "profile": profile_name,
        "path": package_dir.relative_to(GAME_DIR).as_posix(),
        "files": files,
    }


def build_manifest() -> dict[str, Any]:
    rtp_validation = read_json(RTP_VALIDATION_PATH)
    profile_reports = {profile["profile"]: profile for profile in rtp_validation["profiles"]}
    active_profile = rtp_validation["activeProfile"]
    active_profile_dir = PROFILE_ROOT / active_profile

    if set(profile_reports) != {f"rtp_{percentage}" for percentage in PROFILES}:
        raise AssertionError("RTP validation report does not cover every required profile.")

    shared_books = [file_entry(PUBLISH_DIR / f"books_{mode}.jsonl.zst") for mode in MODES]
    publish_manifest = file_entry(PUBLISH_DIR / "index.json")
    active_publish_lookups = {
        mode: file_entry(PUBLISH_DIR / f"lookUpTable_{mode}_0.csv")
        for mode in MODES
    }

    profiles = []
    for percentage in PROFILES:
        profile_name = f"rtp_{percentage}"
        profile_dir = PROFILE_ROOT / profile_name
        profile_report = profile_reports[profile_name]
        assert_lookup_matches_report(profile_report, profile_dir)
        profile_books = assert_profile_books(profile_name, profile_dir)

        profiles.append(
            {
                "profile": profile_name,
                "targetRtp": profile_report["targetRtp"],
                "files": [
                    file_entry(profile_dir / "config.json"),
                    file_entry(profile_dir / f"config_fe_{GAME_ID}.json"),
                    file_entry(profile_dir / "math_config.json"),
                    file_entry(profile_dir / "index.json"),
                    file_entry(profile_dir / "profile.json"),
                    *[
                        file_entry(profile_dir / f"lookUpTable_{mode}_0.csv")
                        for mode in MODES
                    ],
                    *profile_books,
                ],
                "modes": profile_report["modes"],
            }
        )

    for mode in MODES:
        active_lookup = active_profile_dir / f"lookUpTable_{mode}_0.csv"
        publish_lookup = PUBLISH_DIR / f"lookUpTable_{mode}_0.csv"
        if sha256(active_lookup) != sha256(publish_lookup):
            raise AssertionError(
                f"Active publish lookup for {mode} does not match {active_profile}."
            )

    config_files = [
        file_entry(CONFIG_DIR / "config.json"),
        file_entry(CONFIG_DIR / f"config_fe_{GAME_ID}.json"),
        file_entry(CONFIG_DIR / "math_config.json"),
        *[file_entry(CONFIG_DIR / f"event_config_{mode}.json") for mode in MODES],
        *[file_entry(CONFIG_DIR / f"books_{mode}.verification.json") for mode in MODES],
    ]
    release_manifest = assert_release_manifest()
    release_packages = [
        assert_release_package(f"rtp_{percentage}", PROFILE_ROOT / f"rtp_{percentage}")
        for percentage in PROFILES
    ]

    return {
        "manifestVersion": 1,
        "gameId": GAME_ID,
        "activeProfile": active_profile,
        "rtpProfiles": [f"rtp_{percentage}" for percentage in PROFILES],
        "artifactPolicy": (
            "Compressed books are shared as canonical generation outputs, then "
            "intentionally duplicated into every library/rtp_profiles/rtp_* "
            "profile and release/rtp_* upload folder. Each RTP edition has "
            "distinct lookup weights and config files. The active publish "
            "lookups must match the active RTP profile, and every Stake upload "
            "folder must be self-contained."
        ),
        "maxPayoutMultiplier": MAX_PAYOUT_MULTIPLIER,
        "rtpValidation": file_entry(RTP_VALIDATION_PATH),
        "sharedBooks": shared_books,
        "publishManifest": publish_manifest,
        "activePublishLookups": active_publish_lookups,
        "configAndEventFiles": config_files,
        "profiles": profiles,
        "releaseManifest": release_manifest,
        "releasePackages": release_packages,
    }


def normalized_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Rewrite the committed static artifact manifest.")
    args = parser.parse_args()

    manifest = build_manifest()
    rendered = normalized_json(manifest)

    if args.write:
        with MANIFEST_PATH.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered)
        print(f"Wrote {MANIFEST_PATH}")
        return

    current = required_file(MANIFEST_PATH).read_text(encoding="utf-8")
    if current != rendered:
        raise AssertionError(
            f"{MANIFEST_PATH} is stale. Run this script with --write after regenerating artifacts."
        )
    print("The Inheritance static release artifact validation: OK")


if __name__ == "__main__":
    main()
