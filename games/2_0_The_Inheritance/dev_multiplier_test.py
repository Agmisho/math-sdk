"""Development test for The Inheritance multiplier behavior.

This script is intentionally lightweight. It validates the controlled free-spin
Diamond Seal multiplier model without running full SDK book generation.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import csv
import sys

GAME_DIR = Path(__file__).resolve().parent
REPO_ROOT = GAME_DIR.parents[1]
for path in (str(GAME_DIR), str(REPO_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

from gamestate import GameState  # noqa: E402
from game_config import GameConfig  # noqa: E402

MULTIPLIER_SYMBOLS = {"M2", "M5", "M10", "M20", "M100"}
EXPECTED_COUNTS = {
    1: 70900,
    2: 9000,
    5: 8000,
    10: 7000,
    20: 5000,
    100: 100,
}
TOLERANCE = {
    1: 1000,
    2: 500,
    5: 500,
    10: 500,
    20: 400,
    100: 60,
}


def read_csv_symbols(path: Path) -> set[str]:
    symbols: set[str] = set()
    with path.open(newline="") as handle:
        for row in csv.reader(handle):
            for cell in row:
                value = cell.strip()
                if value:
                    symbols.add(value)
    return symbols


def iter_source_files():
    ignored_dirs = {
        "assets",
        "library",
        "__pycache__",
        ".pytest_cache",
    }
    allowed_suffixes = {".py", ".md", ".txt", ".csv", ".json"}
    self_file = Path(__file__).resolve()

    for path in GAME_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.resolve() == self_file:
            continue
        if path.suffix not in allowed_suffixes:
            continue
        if any(part in ignored_dirs for part in path.parts):
            continue
        yield path


def check_static_rules() -> list[str]:
    errors: list[str] = []
    game_text = "\n".join(path.read_text(errors="ignore") for path in iter_source_files())

    blocked_m50 = "M" + "50"
    if blocked_m50 in game_text:
        errors.append("Unexpected M50-style multiplier text exists in source files.")

    persistent_terms = [
        "current" + "_bonus" + "_multiplier",
        "highest" + "_bonus" + "_multiplier",
    ]
    for forbidden in persistent_terms:
        if forbidden in game_text:
            errors.append(f"Persistent multiplier variable found: {forbidden}")

    fr0_symbols = read_csv_symbols(GAME_DIR / "reels" / "FR0.csv")
    natural_multipliers = sorted(fr0_symbols.intersection(MULTIPLIER_SYMBOLS))
    if natural_multipliers:
        errors.append(f"FR0.csv contains natural multiplier symbols: {natural_multipliers}")

    return errors


def setup_free_spin(game: GameState, config: GameConfig, seed: int) -> None:
    game.betmode = "bonus"
    game.criteria = "freegame"
    game.reset_seed(seed)
    game.reset_book()
    game.betmode = "bonus"
    game.criteria = "freegame"
    game.gametype = config.freegame_type


def get_latest_multiplier_event(game: GameState) -> dict:
    events = [event for event in game.book.events if event.get("type") == "multiplierUpdate"]
    if not events:
        raise RuntimeError("No multiplierUpdate event emitted.")
    return events[-1]


def run_frequency_test(samples: int = 100_000) -> Counter:
    config = GameConfig()
    game = GameState(config)
    counts: Counter = Counter()
    examples: list[dict] = []

    for seed in range(1000, 1000 + samples):
        setup_free_spin(game, config, seed)
        game.draw_board()
        game.evaluate_lines_board()
        event = get_latest_multiplier_event(game)
        multiplier = int(event["appliedMultiplier"])
        counts[multiplier] += 1
        if multiplier > 1 and len(examples) < 5:
            examples.append(event)

    print("Multiplier frequency from", samples, "bonus/free-spin samples:")
    print(dict(sorted(counts.items())))
    print("Multiplier event examples:")
    for event in examples:
        print(event)

    for multiplier, expected in EXPECTED_COUNTS.items():
        observed = counts.get(multiplier, 0)
        allowed = TOLERANCE[multiplier]
        if abs(observed - expected) > allowed:
            print(
                f"WARNING: multiplier x{multiplier} observed {observed}, "
                f"expected around {expected} (+/- {allowed})."
            )

    return counts


def run_reset_sequence() -> None:
    config = GameConfig()
    game = GameState(config)
    print("20-spin current-spin multiplier reset check:")

    previous_applied = 1
    saw_reset_after_multiplier = False

    for spin in range(20):
        setup_free_spin(game, config, 1000 + spin)
        game.draw_board()
        game.evaluate_lines_board()
        event = get_latest_multiplier_event(game)
        applied = int(event["appliedMultiplier"])
        landed = int(event["landedMultiplier"])
        print({"spin": spin + 1, "landed": landed, "applied": applied})

        if previous_applied > 1 and applied == 1:
            saw_reset_after_multiplier = True
        previous_applied = applied

    if not saw_reset_after_multiplier:
        print("WARNING: This 20-spin seed range did not show a multiplier followed by x1 reset.")


def main() -> int:
    errors = check_static_rules()
    if errors:
        print("Static rule check failed:")
        for error in errors:
            print("-", error)
        return 1

    print("Static rule check passed.")
    run_reset_sequence()
    run_frequency_test()
    print("Multiplier development test complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
