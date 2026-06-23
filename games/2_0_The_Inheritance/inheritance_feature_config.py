"""Feature configuration helpers for The Inheritance.

The values here describe added mechanics without replacing the existing math.
Multiplier availability is derived from current reel strips so the feature keeps
using the title's real Diamond Seal symbols and values.
"""

from collections import Counter

from inheritance_symbol_roles import (
    MULTIPLIER_SYMBOL_VALUES,
    SYMBOL_ROLE_KEY,
    SYMBOL_ROLE_MULTIPLIER,
    SYMBOL_ROLE_VAULT_TRIGGER,
    SYMBOL_ROLE_WILD,
    role_symbol,
    role_symbols,
)


def count_symbols_on_reels(reels: list[list[str]], symbols: list[str]) -> dict[str, int]:
    counts = Counter()
    symbol_set = set(symbols)
    for reel in reels:
        counts.update(symbol for symbol in reel if symbol in symbol_set)
    return {symbol: int(counts[symbol]) for symbol in symbols if counts[symbol] > 0}


def build_inheritance_feature_config(config) -> dict:
    multiplier_symbols = role_symbols(SYMBOL_ROLE_MULTIPLIER)

    return {
        "vault_reel": {
            "enabled": False,
            "eligible_game_types": [config.basegame_type, config.freegame_type],
            "key_symbol": role_symbol(SYMBOL_ROLE_KEY),
            "vault_symbol": role_symbol(SYMBOL_ROLE_VAULT_TRIGGER),
            "wild_symbol": role_symbol(SYMBOL_ROLE_WILD),
            "multiplier_symbols": multiplier_symbols,
            "multiplier_values": dict(MULTIPLIER_SYMBOL_VALUES),
            "multiplier_stacking": "highest",
            "multiplier_weights_by_game_type": {
                config.basegame_type: count_symbols_on_reels(config.reels["BR0"], multiplier_symbols),
                config.freegame_type: count_symbols_on_reels(config.reels["FR0"], multiplier_symbols),
            },
            "activate_only_on_improved_line_win": True,
            "max_reels_per_spin": config.num_reels,
        },
        "vault_free_spins": {
            "enabled": False,
            "free_spins_awarded": config.freespin_triggers[config.basegame_type][3],
            "sticky_wilds": True,
            "retrigger_enabled": True,
        },
        "high_volatility_feature": {
            "enabled": False,
            "free_spins_awarded": config.freespin_triggers[config.basegame_type][5],
        },
        "sealed_will_collection": {
            "enabled": False,
            "collection_respins": 3,
            "showdown_spins": 3,
        },
        "portrait_mystery": {
            "enabled": False,
            "symbol": "H2",
            "reveal_pools": {
                config.basegame_type: ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9"],
                config.freegame_type: ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9"],
            },
        },
    }
