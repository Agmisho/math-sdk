"""Development test for The Inheritance natural multiplier behavior.

This script is intentionally lightweight. It validates the Diamond Seal
multiplier model without running full SDK book generation.
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


def read_csv_cells(path: Path) -> list[str]:
    cells: list[str] = []
    with path.open(newline="") as handle:
        for row in csv.reader(handle):
            for cell in row:
                value = cell.strip()
                if value:
                    cells.append(value)
    return cells


def read_csv_symbols(path: Path) -> set[str]:
    return set(read_csv_cells(path))


def count_csv_multipliers(path: Path) -> int:
    return sum(1 for symbol in read_csv_cells(path) if symbol in MULTIPLIER_SYMBOLS)


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

    br0_path = GAME_DIR / "reels" / "BR0.csv"
    fr0_path = GAME_DIR / "reels" / "FR0.csv"
    wcap_path = GAME_DIR / "reels" / "FRWCAP.csv"

    br0_symbols = read_csv_symbols(br0_path)
    fr0_symbols = read_csv_symbols(fr0_path)
    wcap_symbols = read_csv_symbols(wcap_path)
    br0_multiplier_count = count_csv_multipliers(br0_path)
    fr0_multiplier_count = count_csv_multipliers(fr0_path)

    if not br0_symbols.intersection(MULTIPLIER_SYMBOLS):
        errors.append("BR0.csv must contain low-frequency Diamond Seal multipliers.")
    if not fr0_symbols.intersection(MULTIPLIER_SYMBOLS):
        errors.append("FR0.csv must contain natural Diamond Seal multipliers.")
    if not wcap_symbols.intersection(MULTIPLIER_SYMBOLS):
        errors.append("FRWCAP.csv must contain natural Diamond Seal multipliers.")
    if br0_multiplier_count >= fr0_multiplier_count:
        errors.append(
            f"BR0 multiplier count ({br0_multiplier_count}) must be below FR0 count ({fr0_multiplier_count})."
        )

    return errors


def setup_spin(game: GameState, config: GameConfig, seed: int, gametype: str) -> None:
    game.betmode = "bonus" if gametype == config.freegame_type else "base"
    game.criteria = "freegame" if gametype == config.freegame_type else "basegame"
    game.reset_seed(seed)
    game.reset_book()
    game.betmode = "bonus" if gametype == config.freegame_type else "base"
    game.criteria = "freegame" if gametype == config.freegame_type else "basegame"
    game.gametype = gametype


def get_latest_multiplier_event(game: GameState) -> dict | None:
    events = [event for event in game.book.events if event.get("type") == "multiplierUpdate"]
    return events[-1] if events else None


def make_board(game: GameState, symbol_name: str = "L1") -> None:
    game.board = [
        [game.create_symbol(symbol_name) for _ in range(game.config.num_rows[reel])]
        for reel in range(game.config.num_reels)
    ]
    game.get_special_symbols_on_board()


def run_forced_reset_demo() -> None:
    config = GameConfig()
    game = GameState(config)
    setup_spin(game, config, 0, config.freegame_type)

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


def run_frequency_test(gametype: str, samples: int = 100_000) -> Counter:
    config = GameConfig()
    game = GameState(config)
    counts: Counter = Counter()
    examples: list[dict] = []

    for seed in range(1000, 1000 + samples):
        setup_spin(game, config, seed, gametype)
        game.draw_board()
        game.evaluate_lines_board()
        event = get_latest_multiplier_event(game)
        multiplier = int(event["appliedMultiplier"]) if event else 1
        counts[multiplier] += 1
        if event and multiplier > 1 and len(examples) < 5:
            examples.append(event)

    print("Multiplier frequency from", samples, gametype, "natural samples:")
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
    config = GameConfig()
    run_frequency_test(config.basegame_type, samples=20_000)
    run_frequency_test(config.freegame_type)
    print("Multiplier development test complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
