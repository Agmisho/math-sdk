"""Canonical symbol roles for The Inheritance math feature code."""

SYMBOL_ROLE_KEY = "key"
SYMBOL_ROLE_WILD = "wild"
SYMBOL_ROLE_MULTIPLIER = "multiplier"
SYMBOL_ROLE_MYSTERY = "mystery"
SYMBOL_ROLE_VAULT_TRIGGER = "vault_trigger"
SYMBOL_ROLE_HIGH_PREMIUM = "high_premium"
SYMBOL_ROLE_LOW_PAYING = "low_paying"

ROLE_SYMBOLS = {
    SYMBOL_ROLE_KEY: "H4",
    SYMBOL_ROLE_WILD: "W",
    SYMBOL_ROLE_MYSTERY: "H2",
    SYMBOL_ROLE_VAULT_TRIGGER: "S",
    SYMBOL_ROLE_MULTIPLIER: ["M2", "M5", "M10", "M20", "M100"],
    SYMBOL_ROLE_HIGH_PREMIUM: ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9"],
    SYMBOL_ROLE_LOW_PAYING: ["L1", "L2", "L3", "L4", "L5", "L6"],
}

MULTIPLIER_SYMBOL_VALUES = {
    "M2": 2,
    "M5": 5,
    "M10": 10,
    "M20": 20,
    "M100": 100,
}


def role_symbols(role: str) -> list[str]:
    symbols = ROLE_SYMBOLS[role]
    return symbols if isinstance(symbols, list) else [symbols]


def role_symbol(role: str) -> str:
    symbols = role_symbols(role)
    if len(symbols) != 1:
        raise ValueError(f"Role '{role}' maps to multiple symbols.")
    return symbols[0]


def symbol_has_role(symbol: str, role: str) -> bool:
    return symbol in role_symbols(role)
