"""Assemble self-contained Stake upload folders for each RTP edition."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
from typing import Any


GAME_DIR = Path(__file__).resolve().parent
REPO_ROOT = GAME_DIR.parents[1]
for import_path in (str(GAME_DIR), str(REPO_ROOT)):
    if import_path not in sys.path:
        sys.path.insert(0, import_path)

from rtp_profiles import SUPPORTED_RTP_PERCENTAGES  # noqa: E402


GAME_ID = "2_0_The_Inheritance"
GAME_NAME = "The Inheritance"
MODES = ("base", "scatter_boost", "bonus")
MODE_COSTS = {"base": 1, "scatter_boost": 3, "bonus": 100}
LIBRARY_DIR = GAME_DIR / "library"
PUBLISH_DIR = LIBRARY_DIR / "publish_files"
PROFILE_ROOT = LIBRARY_DIR / "rtp_profiles"
RELEASE_DIR = GAME_DIR / "release"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with required_file(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def required_file(path: Path) -> Path:
    if not path.is_file():
        raise FileNotFoundError(f"Missing required release source file: {path}")
    return path


def relative(path: Path) -> str:
    return path.relative_to(GAME_DIR).as_posix()


def file_entry(path: Path) -> dict[str, Any]:
    required_file(path)
    return {
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def root_file_entry(path: Path) -> dict[str, Any]:
    return {"path": relative(path), **file_entry(path)}


def assert_inside_release(path: Path) -> None:
    resolved = path.resolve()
    release_root = RELEASE_DIR.resolve()
    if resolved != release_root and release_root not in resolved.parents:
        raise ValueError(f"Refusing to write outside release directory: {path}")


def clean_directory(path: Path) -> None:
    assert_inside_release(path)
    if path.exists():
        shutil.rmtree(path)


def index_modes(index_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    modes = index_data.get("modes", [])
    result = {mode.get("name"): mode for mode in modes}
    missing = [mode for mode in MODES if mode not in result]
    if missing:
        raise ValueError(f"Release index missing modes: {missing}")
    return result


def copy_required(source: Path, destination: Path) -> dict[str, Any]:
    required_file(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    if destination.is_symlink():
        raise ValueError(f"Release package file must be a real copy, not a symlink: {destination}")
    return root_file_entry(destination)


def validate_index_references(package_dir: Path, modes: dict[str, dict[str, Any]]) -> None:
    for mode_name, mode_entry in modes.items():
        for key in ("events", "weights"):
            referenced_name = mode_entry[key]
            if Path(referenced_name).name != referenced_name:
                raise ValueError(f"{package_dir.name} {mode_name} references a non-local file: {referenced_name}")
            path = package_dir / referenced_name
            if not path.is_file():
                raise FileNotFoundError(f"{package_dir.name} {mode_name} missing referenced file: {path}")
            if path.is_symlink():
                raise ValueError(f"{package_dir.name} {mode_name} referenced file is a symlink: {path}")


def build_profile_manifest(
    percentage: int,
    package_dir: Path,
    modes: dict[str, dict[str, Any]],
    core_file_names: set[str],
) -> dict[str, Any]:
    files = {file_name: file_entry(package_dir / file_name) for file_name in sorted(core_file_names)}
    return {
        "schemaVersion": 1,
        "gameId": GAME_ID,
        "gameName": GAME_NAME,
        "profile": f"rtp_{percentage}",
        "rtp": percentage,
        "modes": {
            mode: {
                "cost": MODE_COSTS[mode],
                "books": modes[mode]["events"],
                "weights": modes[mode]["weights"],
            }
            for mode in MODES
        },
        "files": files,
    }


def assemble_profile(percentage: int, *, clean: bool) -> dict[str, Any]:
    profile_name = f"rtp_{percentage}"
    profile_dir = PROFILE_ROOT / profile_name
    package_dir = RELEASE_DIR / profile_name

    if clean:
        clean_directory(package_dir)
    package_dir.mkdir(parents=True, exist_ok=True)

    index_data = read_json(profile_dir / "index.json")
    modes = index_modes(index_data)

    files = [copy_required(profile_dir / "index.json", package_dir / "index.json")]
    for mode in MODES:
        mode_entry = modes[mode]
        if float(mode_entry.get("cost")) != float(MODE_COSTS[mode]):
            raise ValueError(
                f"{profile_name} {mode} cost must be {MODE_COSTS[mode]}, got {mode_entry.get('cost')}"
            )
        books_name = mode_entry["events"]
        lookup_name = mode_entry["weights"]
        files.append(copy_required(profile_dir / lookup_name, package_dir / lookup_name))
        files.append(copy_required(PUBLISH_DIR / books_name, package_dir / books_name))

    expected_names = {"index.json"}
    for mode in MODES:
        expected_names.add(modes[mode]["events"])
        expected_names.add(modes[mode]["weights"])
    validate_index_references(package_dir, modes)
    profile_manifest = build_profile_manifest(percentage, package_dir, modes, expected_names)
    manifest_path = package_dir / "manifest.json"
    with manifest_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(profile_manifest, indent=2, sort_keys=True) + "\n")
    files.append(root_file_entry(manifest_path))

    expected_names.add("manifest.json")
    actual_names = {path.name for path in package_dir.iterdir() if path.is_file()}
    if actual_names != expected_names:
        raise ValueError(
            f"{relative(package_dir)} must contain exactly {sorted(expected_names)}, "
            f"found {sorted(actual_names)}"
        )
    if any((package_dir / file_name).is_symlink() for file_name in expected_names):
        raise ValueError(f"{relative(package_dir)} contains symlinks; release packages must use real files.")

    return {
        "profile": profile_name,
        "path": relative(package_dir),
        "rtp": percentage,
        "manifestSha256": sha256(manifest_path),
        "files": files,
    }


def assemble_release_packages(profiles: tuple[int, ...], *, clean: bool) -> dict[str, Any]:
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    packages = [assemble_profile(profile, clean=clean) for profile in profiles]
    manifest = {
        "manifestVersion": 1,
        "gameId": GAME_ID,
        "gameName": GAME_NAME,
        "profiles": [package["profile"] for package in packages],
        "sourceBooks": relative(PUBLISH_DIR),
        "sourceProfiles": relative(PROFILE_ROOT),
        "packages": packages,
    }
    manifest_path = RELEASE_DIR / "manifest.json"
    with manifest_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profiles",
        nargs="+",
        type=int,
        default=list(SUPPORTED_RTP_PERCENTAGES),
        choices=SUPPORTED_RTP_PERCENTAGES,
        help="RTP percentages to assemble. Defaults to every supported edition.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing selected release folders before assembling.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = assemble_release_packages(tuple(args.profiles), clean=args.clean)
    print(f"Wrote {relative(RELEASE_DIR / 'manifest.json')}")
    for package in manifest["packages"]:
        print(f"Assembled {package['path']}")


if __name__ == "__main__":
    main()
