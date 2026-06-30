"""Static release QA checks for The Inheritance frontend assets.

This complements browser/manual QA by proving the submission build has the
theme loader, custom audio files, and RTP binding required for repeatable test
passes.
"""

from __future__ import annotations

from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
SRC_DIR = APP_DIR / "src"


REQUIRED_ASSETS = {
    "loader": STATIC_DIR / "assets" / "the-inheritance" / "ui" / "loader.png",
    "main background music": STATIC_DIR / "assets" / "the-inheritance" / "audio" / "main-theme.mp3",
    "spin sound": STATIC_DIR / "assets" / "the-inheritance" / "audio" / "spin.mp3",
    "scatter landing sound": STATIC_DIR / "assets" / "the-inheritance" / "audio" / "scatter-landing.mp3",
}


def assert_asset(path: Path, label: str) -> None:
    if not path.is_file():
        raise AssertionError(f"Missing {label}: {path}")
    if path.stat().st_size <= 1024:
        raise AssertionError(f"{label} is unexpectedly small: {path}")


def assert_source_contains(relative_path: str, needle: str, label: str) -> None:
    text = (SRC_DIR / relative_path).read_text(encoding="utf-8")
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def main() -> None:
    for label, path in REQUIRED_ASSETS.items():
        assert_asset(path, label)

    assert_source_contains(
        "game/assets.ts",
        "inheritanceAsset('ui/loader.png')",
        "themed loader image binding",
    )
    assert_source_contains(
        "components/Sound.svelte",
        "/assets/the-inheritance/audio/main-theme.mp3",
        "main background music registration",
    )
    assert_source_contains(
        "components/Sound.svelte",
        "/assets/the-inheritance/audio/scatter-landing.mp3",
        "scatter landing sound registration",
    )
    assert_source_contains(
        "components/Sound.svelte",
        "/assets/the-inheritance/audio/spin.mp3",
        "spin sound registration",
    )
    assert_source_contains(
        "game/config.ts",
        "PUBLIC_THE_INHERITANCE_RTP",
        "build-time RTP display binding",
    )

    print("The Inheritance static release asset QA: OK")


if __name__ == "__main__":
    main()
