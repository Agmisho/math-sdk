"""Validate self-contained The Inheritance RTP release packages.

Run from the repository root:

    python games/2_0_The_Inheritance/tools/validate_release_packages.py
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path
import sys
from typing import Any

import zstandard as zstd


GAME_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = GAME_DIR.parents[1]
for import_path in (str(GAME_DIR), str(REPO_ROOT)):
    if import_path not in sys.path:
        sys.path.insert(0, import_path)

from rtp_profiles import SUPPORTED_RTP_PERCENTAGES  # noqa: E402


GAME_ID = "2_0_The_Inheritance"
GAME_NAME = "The Inheritance"
RELEASE_DIR = GAME_DIR / "release"
LIBRARY_PROFILE_ROOT = GAME_DIR / "library" / "rtp_profiles"
MODES = ("base", "scatter_boost", "bonus")
MODE_COSTS = {"base": 1, "scatter_boost": 3, "bonus": 100}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    assert_regular_file(path)
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def assert_regular_file(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f"Missing release file: {path}")
    if path.is_symlink():
        raise AssertionError(f"Release file must not be a symlink: {path}")
    if not path.is_file():
        raise AssertionError(f"Release path is not a regular file: {path}")
    if path.stat().st_size <= 0:
        raise AssertionError(f"Release file is empty: {path}")


def assert_local_file_name(file_name: str, *, context: str) -> None:
    if Path(file_name).name != file_name:
        raise AssertionError(f"{context} references a file outside its package: {file_name}")


def manifest_file_entry(manifest: dict[str, Any], file_name: str) -> dict[str, Any]:
    files = manifest.get("files", {})
    if file_name not in files:
        raise AssertionError(f"{manifest.get('profile')} manifest missing file entry: {file_name}")
    return files[file_name]


def validate_manifest_file_hash(package_dir: Path, manifest: dict[str, Any], file_name: str) -> None:
    path = package_dir / file_name
    assert_regular_file(path)
    entry = manifest_file_entry(manifest, file_name)
    if int(entry.get("bytes", -1)) != path.stat().st_size:
        raise AssertionError(f"{package_dir.name} {file_name} byte count differs from manifest.")
    if entry.get("sha256") != sha256(path):
        raise AssertionError(f"{package_dir.name} {file_name} sha256 differs from manifest.")


def load_books(path: Path) -> dict[int, int]:
    assert_regular_file(path)
    books = {}
    with path.open("rb") as compressed:
        with zstd.ZstdDecompressor().stream_reader(compressed) as reader:
            text_reader = io.TextIOWrapper(reader, encoding="utf-8")
            for line in text_reader:
                book = json.loads(line)
                books[int(book["id"])] = int(book["payoutMultiplier"])
    if not books:
        raise AssertionError(f"No books found in {path}")
    return books


def validate_lookup(path: Path, books: dict[int, int]) -> None:
    assert_regular_file(path)
    positive_weight_seen = False
    with path.open(newline="", encoding="utf-8") as handle:
        for row_number, row in enumerate(csv.reader(handle), start=1):
            if len(row) != 3:
                raise AssertionError(f"{path} row {row_number} must have 3 columns.")
            book_id = int(row[0])
            weight = int(row[1])
            payout_multiplier = int(row[2])
            if book_id not in books:
                raise AssertionError(f"{path} references unknown book id {book_id}.")
            if payout_multiplier != books[book_id]:
                raise AssertionError(
                    f"{path} payout mismatch for book {book_id}: "
                    f"lookup={payout_multiplier}, book={books[book_id]}"
                )
            if weight < 0:
                raise AssertionError(f"{path} has negative weight for book {book_id}.")
            positive_weight_seen = positive_weight_seen or weight > 0
    if not positive_weight_seen:
        raise AssertionError(f"{path} has no positive lookup weights.")


def index_modes(index_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    modes = {mode.get("name"): mode for mode in index_data.get("modes", [])}
    missing = [mode for mode in MODES if mode not in modes]
    if missing:
        raise AssertionError(f"index.json missing modes: {missing}")
    return modes


def validate_profile_package(percentage: int) -> dict[str, Any]:
    profile = f"rtp_{percentage}"
    package_dir = RELEASE_DIR / profile
    if not package_dir.is_dir():
        raise AssertionError(f"Missing release profile folder: {package_dir}")

    index_path = package_dir / "index.json"
    manifest_path = package_dir / "manifest.json"
    index_data = read_json(index_path)
    manifest = read_json(manifest_path)
    modes = index_modes(index_data)

    if manifest.get("schemaVersion") != 1:
        raise AssertionError(f"{profile} manifest schemaVersion must be 1.")
    if manifest.get("gameId") != GAME_ID or manifest.get("gameName") != GAME_NAME:
        raise AssertionError(f"{profile} manifest game identity is incorrect.")
    if manifest.get("profile") != profile or int(manifest.get("rtp", -1)) != percentage:
        raise AssertionError(f"{profile} manifest profile/RTP mismatch.")

    expected_names = {"index.json", "manifest.json"}
    validate_manifest_file_hash(package_dir, manifest, "index.json")

    library_profile = LIBRARY_PROFILE_ROOT / profile
    if library_profile.is_dir():
        library_profile_data = read_json(library_profile / "profile.json")
        library_rtp = round(float(library_profile_data.get("targetRtp", -1)) * 100)
        if library_profile_data.get("profile") != profile or library_rtp != percentage:
            raise AssertionError(f"{profile} library profile.json disagrees with release package.")

    for mode in MODES:
        index_mode = modes[mode]
        manifest_mode = manifest.get("modes", {}).get(mode)
        if not manifest_mode:
            raise AssertionError(f"{profile} manifest missing mode {mode}.")
        if float(index_mode.get("cost")) != float(MODE_COSTS[mode]):
            raise AssertionError(f"{profile} {mode} index cost must be {MODE_COSTS[mode]}.")
        if float(manifest_mode.get("cost")) != float(MODE_COSTS[mode]):
            raise AssertionError(f"{profile} {mode} manifest cost must be {MODE_COSTS[mode]}.")

        books_name = index_mode["events"]
        lookup_name = index_mode["weights"]
        if manifest_mode.get("books") != books_name or manifest_mode.get("weights") != lookup_name:
            raise AssertionError(f"{profile} {mode} manifest/index file references disagree.")
        for file_name in (books_name, lookup_name):
            assert_local_file_name(file_name, context=f"{profile} {mode}")
            validate_manifest_file_hash(package_dir, manifest, file_name)

        books = load_books(package_dir / books_name)
        validate_lookup(package_dir / lookup_name, books)
        expected_names.update((books_name, lookup_name))

    actual_names = {path.name for path in package_dir.iterdir() if path.is_file()}
    if actual_names != expected_names:
        raise AssertionError(
            f"{profile} release folder must contain exactly {sorted(expected_names)}, "
            f"found {sorted(actual_names)}"
        )

    return {
        "profile": profile,
        "rtp": percentage,
        "manifestSha256": sha256(manifest_path),
        "files": sorted(expected_names),
    }


def main() -> None:
    results = [validate_profile_package(percentage) for percentage in SUPPORTED_RTP_PERCENTAGES]
    print(
        json.dumps(
            {
                "gameId": GAME_ID,
                "profiles": results,
                "status": "ok",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
