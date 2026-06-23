"""Focused validation for The Inheritance Legacy Key / Vault Reel feature.

Run from repository root:
PYTHONPATH=. python games/2_0_The_Inheritance/dev_vault_reel_feature_test.py
"""

from __future__ import annotations

from pathlib import Path
import sys

GAME_DIR = Path(__file__).resolve().parent
REPO_ROOT = GAME_DIR.parents[1]
for import_path in (str(GAME_DIR), str(REPO_ROOT)):
    if import_path not in sys.path:
        sys.path.insert(0, import_path)

from game_config import GameConfig  # noqa: E402
from gamestate import GameState  # noqa: E402


def make_game() -> GameState:
    config = GameConfig()
    game = GameState(config)
    game.betmode = "base"
    game.criteria = "basegame"
    game.reset_seed(41)
    game.reset_book()
    game.betmode = "base"
    game.criteria = "basegame"
    game.gametype = config.basegame_type
    config.inheritance_feature_config["vault_reel"]["enabled"] = True
    config.inheritance_feature_config["vault_reel"]["multiplier_weights_by_game_type"][config.basegame_type] = {"M2": 1}
    return game


def set_board(game: GameState, reels: list[list[str]]) -> None:
    game.board = [[game.create_symbol(symbol) for symbol in reel] for reel in reels]
    game.get_special_symbols_on_board()


def get_events(game: GameState, event_type: str) -> list[dict]:
    return [event for event in game.book.events if event.get("type") == event_type]


def paying_key_board() -> list[list[str]]:
    return [
        ["H1", "L1", "L2", "L3", "L4"],
        ["H4", "L2", "L3", "M20", "L5"],
        ["H1", "L3", "L4", "L5", "L6"],
        ["H1", "L4", "L5", "L6", "H2"],
        ["H1", "L5", "L6", "H2", "H3"],
    ]


def non_paying_key_board() -> list[list[str]]:
    return [
        ["H1", "L1", "L2", "L3", "L4"],
        ["H4", "L2", "L3", "L4", "L5"],
        ["H2", "L3", "L4", "L5", "L6"],
        ["H3", "L4", "L5", "L6", "H2"],
        ["H5", "L5", "L6", "H2", "H3"],
    ]


def validate_vault_reel_activation() -> None:
    game = make_game()
    set_board(game, paying_key_board())

    before = game.evaluate_vault_candidate_board(game.board, multiplier=1)
    assert before["totalWin"] == 0

    game.resolve_vault_reels_before_line_evaluation()
    events = get_events(game, "vaultReelResolved")
    assert len(events) == 1

    event = events[0]
    assert event["sourceKeySymbol"] == "H4"
    assert event["sourceKeyPosition"] == {"reel": 1, "row": 0}
    assert event["targetReel"] == 1
    assert event["wildSymbolId"] == "W"
    assert event["multiplierSymbolId"] == "M2"
    assert event["multiplierValue"] == 2
    assert event["multiplierStack"]["stackingRule"] == "highest"
    assert event["multiplierStack"]["combinedMultiplier"] == 20
    assert any(source["symbol"] == "M20" for source in event["multiplierStack"]["vaultSources"])
    assert len(event["transformedPositions"]) == 5
    assert all(game.board[1][row].name == "W" for row in range(5))

    affected_line = next(line for line in event["affectedPaylines"] if line["lineIndex"] == 1)
    assert affected_line["lineIndex"] == 1
    assert affected_line["lineWinBeforeTransform"] == 0
    assert affected_line["lineWinBeforeMultiplier"] == 5
    assert affected_line["multiplierStackResult"] == 20
    assert affected_line["finalLineWin"] == 100
    assert sorted(line["lineIndex"] for line in event["affectedPaylines"]) == [1, 7, 8]
    assert event["totalSpinWinBefore"] == 0
    assert event["totalSpinWinAfter"] == 120
    assert event["capStatus"]["isCapped"] is False

    game.evaluate_lines_board()
    assert game.win_data["totalWin"] == 120
    assert get_events(game, "multiplierUpdate")[-1]["appliedMultiplier"] == 20


def validate_no_activation_without_improved_payline() -> None:
    game = make_game()
    set_board(game, non_paying_key_board())

    game.resolve_vault_reels_before_line_evaluation()
    assert get_events(game, "vaultReelResolved") == []
    assert game.board[1][0].name == "H4"

    game.evaluate_lines_board()
    assert game.win_data["totalWin"] == 0.5


def main() -> int:
    validate_vault_reel_activation()
    validate_no_activation_without_improved_payline()
    print("Vault Reel feature validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
