"""Fast development runner for The Inheritance.

This runner intentionally bypasses the full SDK book-generation distribution loop.
Use it while feature logic is being built and validated.
"""

from collections import Counter

from gamestate import GameState
from game_config import GameConfig


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
    landed_multiplier = game.get_landed_multiplier()
    game.evaluate_lines_board()
    game.win_manager.update_gametype_wins(game.gametype)
    game.evaluate_finalwin()

    return {
        "sim": sim,
        "game_type": game.gametype,
        "final_win": game.final_win,
        "events": len(game.book.events),
        "collected": game.collected_count,
        "mansion_level": game.mansion_level,
        "display_multiplier": game.display_multiplier,
        "landed_multiplier": landed_multiplier,
    }


if __name__ == "__main__":
    config = GameConfig()
    game = GameState(config)

    print("Running The Inheritance BASE fast feature check...")
    for sim in range(20):
        print(run_single_check(game, sim, config.basegame_type, "base", "basegame"))

    print("Running The Inheritance BONUS fast feature check...")
    bonus_results = []
    for sim in range(20, 40):
        result = run_single_check(game, sim, config.freegame_type, "bonus", "freegame")
        bonus_results.append(result)
        print(result)

    print("Multiplier frequency summary from visible bonus samples:")
    print(dict(sorted(Counter(result["landed_multiplier"] for result in bonus_results).items())))

    print("The Inheritance fast feature check complete.")
