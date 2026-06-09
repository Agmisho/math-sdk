"""Development test for The Inheritance natural multiplier behavior.

This script is intentionally lightweight. It validates the free-spin Diamond
Seal multiplier model without running full SDK book generation.
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
EXPECTED_MULTIPLIERS = {1, 2, 5, 10, 20, 100}


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

    blocked_text = "M" + "50"
    if blocked_text in game_text:
        errors.append("Unexpected fifty-times multiplier text exists in source files.")

    blocked_terms = [
        "current" + "_bonus" + "_multiplier",
        "highest" + "_bonus" + "_multiplier",
        "inject" + "_controlled" + "_multiplier" + "_symbol",
        "multiplier" + "_target" + "_weights",
    ]
    for forbidden in blocked_terms:
        if forbidden in game_text:
            errors.append(f"Unexpected controlled or persistent multiplier logic found: {forbidden}")

    br0_symbols = read_csv_symbols(GAME_DIR / "reels" / "BR0.csv")
    fr0_symbols = read_csv_symbols(GAME_DIR / "reels" / "FR0.csv")
    wcap_symbols = read_csv_symbols(GAME_DIR / "reels" / "FRWCAP.csv")

    if br0_symbols.intersection(MULTIPLIER_SYMBOLS):
        errors.append("BR0.csv should not contain Diamond Seal multipliers.")
    if not fr0_symbols.intersection(MULTIPLIER_SYMBOLS):
        errors.append("FR0.csv must contain natural Diamond Seal multipliers.")
    if not wcap_symbols.intersection(MULTIPLIER_SYMBOLS):
        errors.append("FRWCAP.csv must contain natural Diamond Seal multipliers.")

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


def make_board(game: GameState, symbol_name: str = "L1") -> None:
    game.board = [
        [game.create_symbol(symbol_name) for _ in range(game.config.num_rows[reel])]
        for reel in range(game.config.num_reels)
    ]
    game.get_special_symbols_on_board()


def run_forced_reset_demo() -> None:
    config = GameConfig()
    game = GameState(config)
    setup_free_spin(game, config, 0)

    sequence = [
        [(0, 0, "M20"), (2, 1, "M5")],
        [],
        [(1, 3, "M2")],
        [],
        [(3, 2, "M100"), (4, 4, "M10")],
        [],
    ]

    print("Forced current-spin reset examples:")
    for index, placements in enumerate(sequence, start=1):
        game.reset_book()
        game.betmode = "bonus"
        game.criteria = "freegame"
        game.gametype = config.freegame_type
        make_board(game)
        for reel, row, symbol_name in placements:
            game.board[reel][row] = game.create_symbol(symbol_name)
        game.get_special_symbols_on_board()
        game.evaluate_lines_board()
        event = get_latest_multiplier_event(game)
        print({"spin": index, "placements": placements, "event": event})


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

    print("Multiplier frequency from", samples, "natural free-spin samples:")
    print(dict(sorted(counts.items())))
    print("Multiplier event examples:")
    for event in examples:
        print(event)

    unexpected = set(counts.keys()).difference(EXPECTED_MULTIPLIERS)
    if unexpected:
        print("WARNING: Unexpected applied multiplier values:", sorted(unexpected))

    return counts


def main() -> int:
    errors = check_static_rules()
    if errors:
        print("Static rule check failed:")
        for error in errors:
            print("-", error)
        return 1

    print("Static rule check passed.")
    run_forced_reset_demo()
    run_frequency_test()
    print("Multiplier development test complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
