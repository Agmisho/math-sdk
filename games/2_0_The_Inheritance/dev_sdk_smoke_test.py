"""Lightweight SDK smoke checks for The Inheritance.

This script avoids full book generation. It instantiates the game, runs small
base/free samples, and prints event/state summaries for development.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

GAME_DIR = Path(__file__).resolve().parent
REPO_ROOT = GAME_DIR.parents[1]
for import_path in (str(GAME_DIR), str(REPO_ROOT)):
    if import_path not in sys.path:
        sys.path.insert(0, import_path)

from game_config import GameConfig  # noqa: E402
from gamestate import GameState  # noqa: E402

FORBIDDEN_TERMS = [
    "M" + "50",
    "current" + "_bonus" + "_multiplier",
    "highest" + "_bonus" + "_multiplier",
]


def scan_static_rules() -> list[str]:
    errors: list[str] = []
    allowed_suffixes = {".py", ".md", ".txt", ".csv", ".json"}
    ignored_dirs = {"library", "__pycache__", ".pytest_cache"}
    for path in GAME_DIR.rglob("*"):
        if not path.is_file() or path.suffix not in allowed_suffixes:
            continue
        if any(part in ignored_dirs for part in path.parts):
            continue
        text = path.read_text(errors="ignore")
        for term in FORBIDDEN_TERMS:
            if term in text:
                errors.append(f"Forbidden term found: {term} in {path.relative_to(GAME_DIR)}")
    return errors


def reset_for_spin(game: GameState, config: GameConfig, sim: int, betmode: str, criteria: str, gametype: str) -> None:
    game.betmode = betmode
    game.criteria = criteria
    game.reset_seed(sim)
    game.reset_book()
    game.betmode = betmode
    game.criteria = criteria
    game.gametype = gametype


def run_single_spin(game: GameState, config: GameConfig, sim: int, betmode: str, criteria: str, gametype: str) -> dict:
    reset_for_spin(game, config, sim, betmode, criteria, gametype)
    game.draw_board()
    game.update_collection_state()
    game.evaluate_lines_board()
    game.win_manager.update_gametype_wins(game.gametype)
    game.evaluate_finalwin()

    event_counts = Counter(event.get("type") for event in game.book.events)
    multiplier_events = [event for event in game.book.events if event.get("type") == "multiplierUpdate"]
    collection_events = [event for event in game.book.events if event.get("type") == "collectionUpdate"]
    return {
        "sim": sim,
        "betmode": betmode,
        "criteria": criteria,
        "gametype": gametype,
        "final_win": game.final_win,
        "events": len(game.book.events),
        "event_counts": dict(event_counts),
        "collection_state": {
            "collected": game.collected_count,
            "mansionLevel": game.mansion_level,
            "displayMultiplier": game.display_multiplier,
            "latestEvent": collection_events[-1] if collection_events else None,
        },
        "multiplier_state": multiplier_events[-1] if multiplier_events else {"appliedMultiplier": 1, "positions": []},
    }


def run_checks() -> int:
    errors = scan_static_rules()
    config = GameConfig()
    game = GameState(config)

    print("config", {"rtp": config.rtp, "wincap": config.wincap, "rows": config.num_rows, "paylines": len(config.paylines)})
    print("bet_modes", [(mode.get_name(), mode.get_cost(), mode.get_wincap()) for mode in config.bet_modes])

    summaries = []
    for sim in range(20):
        summaries.append(run_single_spin(game, config, sim, "base", "basegame", config.basegame_type))
    for sim in range(20, 40):
        summaries.append(run_single_spin(game, config, sim, "bonus", "freegame", config.freegame_type))

    final_wins = [summary["final_win"] for summary in summaries]
    multiplier_events = sum(1 for summary in summaries if summary["multiplier_state"].get("positions"))
    collection_events = sum(1 for summary in summaries if "collectionUpdate" in summary["event_counts"])

    print("smoke_totals", dict(Counter(summary["gametype"] for summary in summaries)))
    print("final_win", {"min": min(final_wins), "max": max(final_wins), "sum": round(sum(final_wins), 4)})
    print("events", {"spins": len(summaries), "withMultiplier": multiplier_events, "withCollectionUpdate": collection_events})
    print("collection state", summaries[-1]["collection_state"])
    print("multiplier state", summaries[-1]["multiplier_state"])
    print("example", summaries[0])

    if config.wincap != 5000.0:
        errors.append(f"Expected wincap 5000.0, got {config.wincap}")
    mode_costs = {mode.get_name(): mode.get_cost() for mode in config.bet_modes}
    if mode_costs.get("bonus") != 100.0:
        errors.append(f"Expected bonus cost 100.0, got {mode_costs.get('bonus')}")
    if mode_costs.get("scatter_boost") != 3.0:
        errors.append(f"Expected scatter_boost cost 3.0, got {mode_costs.get('scatter_boost')}")

    if errors:
        print("Smoke check failed:")
        for error in errors:
            print("-", error)
        return 1

    print("SDK smoke test complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_checks())
