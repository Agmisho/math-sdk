"""Focused validation for The Inheritance Legacy Key virtual scatter credit.

Run from repository root:
PYTHONPATH=. python3 games/2_0_The_Inheritance/dev_legacy_key_credit_test.py
"""

import sys
from pathlib import Path

GAME_DIR = Path(__file__).resolve().parent
if str(GAME_DIR) not in sys.path:
    sys.path.insert(0, str(GAME_DIR))

from game_config import GameConfig  # noqa: E402
from gamestate import GameState  # noqa: E402

LEGACY_KEY_TARGET = 20


def make_game(mode="base", criteria="freegame", collected_count=LEGACY_KEY_TARGET):
    config = GameConfig()
    game = GameState(config)
    game.betmode = mode
    game.criteria = criteria
    game.collected_count = collected_count
    game.collection_target = LEGACY_KEY_TARGET
    game.reset_book()
    return game


def inject_two_scatter_board(game):
    sym = game.symbol_storage.create_symbol
    game.board = [
        [sym("S"), sym("L1"), sym("L2"), sym("L3"), sym("L4")],
        [sym("L1"), sym("L1"), sym("L2"), sym("L3"), sym("L4")],
        [sym("S"), sym("L1"), sym("L2"), sym("L3"), sym("L4")],
        [sym("L1"), sym("L1"), sym("L2"), sym("L3"), sym("L4")],
        [sym("L1"), sym("L1"), sym("L2"), sym("L3"), sym("L4")],
    ]
    game.special_syms_on_board = {
        "scatter": [{"reel": 0, "row": 0}, {"reel": 2, "row": 0}],
    }


def get_events(game, event_type):
    return [event for event in game.book.events if event.get("type") == event_type]


def validate_base_credit_trigger():
    game = make_game(mode="base", criteria="freegame", collected_count=LEGACY_KEY_TARGET)
    inject_two_scatter_board(game)

    assert game.collected_count == LEGACY_KEY_TARGET
    assert game.count_special_symbols("scatter") == 2
    assert game.get_effective_scatter_count("scatter") == 3
    assert game.check_fs_condition("scatter") is True

    game.run_freespin_from_base("scatter")

    legacy_events = get_events(game, "legacyScatterCredit")
    trigger_events = get_events(game, "freeSpinTrigger")
    collection_events = get_events(game, "collectionUpdate")

    assert len(legacy_events) == 1
    assert legacy_events[0]["collected"] == LEGACY_KEY_TARGET
    assert legacy_events[0]["target"] == LEGACY_KEY_TARGET
    assert legacy_events[0]["virtualScatters"] == 1
    assert legacy_events[0]["naturalScatters"] == 2
    assert legacy_events[0]["effectiveScatters"] == 3
    assert legacy_events[0]["used"] is True
    assert legacy_events[0]["gameType"] == "basegame"

    assert len(trigger_events) == 1
    assert trigger_events[0]["totalFs"] == 8
    assert len(trigger_events[0]["positions"]) == 2

    assert game.collected_count == 0
    assert collection_events, "Expected collectionUpdate reset/freegame events."
    assert collection_events[0]["collected"] == 0

    freegame_collection_events = [
        event for event in collection_events if event.get("gameType") == "freegame"
    ]
    assert freegame_collection_events, "Expected freegame collectionUpdate events."
    assert all(event["positions"] == [] for event in freegame_collection_events)
    assert all(event["collected"] == 0 for event in freegame_collection_events)


def validate_scatter_boost_credit_trigger():
    game = make_game(mode="scatter_boost", criteria="freegame", collected_count=LEGACY_KEY_TARGET)
    inject_two_scatter_board(game)

    assert game.count_special_symbols("scatter") == 2
    assert game.get_effective_scatter_count("scatter") == 3
    assert game.check_fs_condition("scatter") is True

    game.run_freespin_from_base("scatter")

    assert len(get_events(game, "legacyScatterCredit")) == 1
    assert len(get_events(game, "freeSpinTrigger")) == 1
    assert game.collected_count == 0


def validate_no_credit_without_target_keys():
    game = make_game(mode="base", criteria="freegame", collected_count=LEGACY_KEY_TARGET - 1)
    inject_two_scatter_board(game)

    assert game.count_special_symbols("scatter") == 2
    assert game.get_effective_scatter_count("scatter") == 2
    assert game.check_fs_condition("scatter") is False
    assert get_events(game, "legacyScatterCredit") == []


def validate_bonus_does_not_use_credit():
    game = make_game(mode="bonus", criteria="freegame", collected_count=LEGACY_KEY_TARGET)
    inject_two_scatter_board(game)

    assert game.count_special_symbols("scatter") == 2
    assert game.get_effective_scatter_count("scatter") == 2
    assert game.check_fs_condition("scatter") is False


def validate_freegame_does_not_use_credit():
    game = make_game(mode="base", criteria="freegame", collected_count=LEGACY_KEY_TARGET)
    inject_two_scatter_board(game)
    game.gametype = game.config.freegame_type

    assert game.count_special_symbols("scatter") == 2
    assert game.get_effective_scatter_count("scatter") == 2
    assert game.check_fs_condition("scatter") is True  # natural freegame retrigger threshold is 2
    assert get_events(game, "legacyScatterCredit") == []


def main():
    validate_base_credit_trigger()
    validate_scatter_boost_credit_trigger()
    validate_no_credit_without_target_keys()
    validate_bonus_does_not_use_credit()
    validate_freegame_does_not_use_credit()
    print("Legacy Key virtual scatter credit validation: OK")


if __name__ == "__main__":
    main()
