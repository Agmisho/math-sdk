"""Fast development runner for The Inheritance.

This runner does not run full book generation. Use full_generate.py later when
feature logic is stable and ready for production-style SDK output.
"""

from collections import Counter

from gamestate import GameState
from game_config import GameConfig


def latest_event(game, event_type):
    events = [event for event in game.book.events if event.get("type") == event_type]
    return events[-1] if events else None


def run_single_check(game, sim, gametype, betmode, criteria):
    game.betmode = betmode
    game.criteria = criteria
    game.reset_seed(sim)
    game.reset_book()
    game.betmode = betmode
    game.criteria = criteria
    game.gametype = gametype

    game.draw_board()
    game.update_collection_state()
    game.evaluate_lines_board()
    game.win_manager.update_gametype_wins(game.gametype)
    game.evaluate_finalwin()

    multiplier_event = latest_event(game, "multiplierUpdate")
    collection_event = latest_event(game, "collectionUpdate")

    return {
        "sim": sim,
        "gameType": game.gametype,
        "criteria": criteria,
        "finalWin": game.final_win,
        "eventCount": len(game.book.events),
        "collected": collection_event.get("collected") if collection_event else None,
        "mansionLevel": collection_event.get("mansionLevel") if collection_event else None,
        "appliedMultiplier": multiplier_event.get("appliedMultiplier") if multiplier_event else 1,
        "landedMultiplier": multiplier_event.get("landedMultiplier") if multiplier_event else 1,
    }


if __name__ == "__main__":
    config = GameConfig()
    game = GameState(config)

    print("The Inheritance fast development check")
    print({
        "gameId": config.game_id,
        "name": config.working_name,
        "wincap": config.wincap,
        "reels": config.num_reels,
        "rows": config.num_rows,
        "paylines": len(config.paylines),
        "paytableEntries": len(config.paytable),
    })

    print("BASE checks")
    for sim in range(5):
        print(run_single_check(game, sim, config.basegame_type, "base", "basegame"))

    print("BONUS checks")
    bonus_results = []
    for sim in range(1000, 1020):
        result = run_single_check(game, sim, config.freegame_type, "bonus", "freegame")
        bonus_results.append(result)
        print(result)

    print("BONUS multiplier summary")
    print(dict(sorted(Counter(result["appliedMultiplier"] for result in bonus_results).items())))

    print("The Inheritance fast development check complete")
