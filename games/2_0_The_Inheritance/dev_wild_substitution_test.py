"""Focused validation for The Inheritance Wild substitution restrictions.

Run from repository root:
PYTHONPATH=. python games/2_0_The_Inheritance/dev_wild_substitution_test.py
"""

from __future__ import annotations

import sys
from pathlib import Path


GAME_DIR = Path(__file__).resolve().parent
if str(GAME_DIR) not in sys.path:
    sys.path.insert(0, str(GAME_DIR))

from game_config import GameConfig  # noqa: E402
from gamestate import GameState  # noqa: E402


def make_game() -> GameState:
    return GameState(GameConfig())


def build_board(game: GameState, row_zero: list[str]) -> list[list]:
    sym = game.symbol_storage.create_symbol
    filler_rows = [
        ["H1", "H2", "H3", "H5", "H6"],
        ["L2", "L3", "L4", "L5", "L6"],
        ["H7", "H8", "H9", "L1", "L2"],
        ["L3", "L4", "L5", "L6", "H1"],
    ]
    return [[sym(row_zero[reel]), *[sym(row[reel]) for row in filler_rows]] for reel in range(5)]


def line_symbols(win_data: dict) -> list[tuple[str, int]]:
    return [(win["symbol"], int(win["kind"])) for win in win_data["wins"]]


def evaluate_row_zero(row_zero: list[str]) -> dict:
    game = make_game()
    game.board = build_board(game, row_zero)
    game.evaluate_lines_board()
    return game.win_data


def validate_wild_still_substitutes_regular_low_symbols() -> None:
    win_data = evaluate_row_zero(["W", "L1", "L1", "L1", "L2"])
    assert ("L1", 4) in line_symbols(win_data)


def validate_wild_does_not_substitute_legacy_key() -> None:
    win_data = evaluate_row_zero(["W", "H4", "H4", "H4", "H4"])
    assert ("H4", 5) not in line_symbols(win_data)
    assert ("H4", 4) not in line_symbols(win_data)
    assert ("H4", 3) not in line_symbols(win_data)


def validate_exact_legacy_key_still_pays() -> None:
    win_data = evaluate_row_zero(["H4", "H4", "H4", "W", "H4"])
    assert ("H4", 3) in line_symbols(win_data)
    assert ("H4", 4) not in line_symbols(win_data)
    assert ("H4", 5) not in line_symbols(win_data)


def main() -> None:
    validate_wild_still_substitutes_regular_low_symbols()
    validate_wild_does_not_substitute_legacy_key()
    validate_exact_legacy_key_still_pays()
    print("The Inheritance Wild substitution validation: OK")


if __name__ == "__main__":
    main()
