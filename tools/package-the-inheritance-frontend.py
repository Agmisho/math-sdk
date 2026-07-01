"""Copy the generated The Inheritance static site into a standalone upload folder."""

from __future__ import annotations

import os
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "artifacts" / "the-inheritance-frontend-rtp96"


def main() -> None:
    source_value = os.getenv("THE_INHERITANCE_RELEASE_BUILD_DIR")
    if not source_value:
        raise RuntimeError("THE_INHERITANCE_RELEASE_BUILD_DIR is required")

    source = Path(source_value).resolve()
    if not (source / "index.html").is_file():
        raise RuntimeError("Generated frontend is missing index.html")
    if not (source / "_app").is_dir():
        raise RuntimeError("Generated frontend is missing _app")

    if TARGET.exists():
        shutil.rmtree(TARGET)
    TARGET.mkdir(parents=True)

    for item in source.iterdir():
        destination = TARGET / item.name
        if item.is_symlink():
            raise RuntimeError(f"Frontend must not contain symlinks: {item}")
        if item.is_dir():
            shutil.copytree(item, destination, symlinks=False)
        else:
            shutil.copy2(item, destination)

    print(f"Prepared frontend upload folder: {TARGET}")
    print("Top level: " + ", ".join(sorted(path.name for path in TARGET.iterdir())))


if __name__ == "__main__":
    main()
