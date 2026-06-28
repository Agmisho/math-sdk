"""Validate confirmed product rules against the active Math SDK config."""

from __future__ import annotations

from game_config import GameConfig
from inheritance_symbol_roles import MULTIPLIER_SYMBOL_VALUES
from rtp_profiles import DEFAULT_RTP_PERCENTAGE, SUPPORTED_RTP_PERCENTAGES


def get_mode(config: GameConfig, name: str):
    return next(mode for mode in config.bet_modes if mode.get_name() == name)


def main() -> None:
    config = GameConfig()

    assert config.num_reels == 5
    assert config.num_rows == [5, 5, 5, 5, 5]
    assert len(config.paylines) == 15
    assert config.win_type == "lines"
    assert config.wincap == 5000.0

    assert SUPPORTED_RTP_PERCENTAGES == (92, 93, 94, 95, 96, 97)
    assert DEFAULT_RTP_PERCENTAGE == 97

    assert get_mode(config, "base").get_cost() == 1.0
    assert get_mode(config, "scatter_boost").get_cost() == 3.0
    assert get_mode(config, "bonus").get_cost() == 100.0
    assert get_mode(config, "bonus").get_buybonus() is True

    assert config.bonus_buy_free_spins == 10
    assert config.freespin_triggers[config.basegame_type] == {3: 8, 4: 12, 5: 15}
    assert config.freespin_triggers[config.freegame_type] == {2: 3, 3: 5, 4: 8, 5: 12}

    assert config.legacy_key_collection_target == 10
    assert config.special_symbols["wild"] == ["W"]
    assert config.special_symbols["scatter"] == ["S"]
    assert config.wild_substitution_blocked_symbols == [
        "H4",
        "S",
        "M2",
        "M5",
        "M10",
        "M20",
        "M100",
    ]
    assert MULTIPLIER_SYMBOL_VALUES == {
        "M2": 2,
        "M5": 5,
        "M10": 10,
        "M20": 20,
        "M100": 100,
    }

    print("The Inheritance design contract validation: OK")


if __name__ == "__main__":
    main()
