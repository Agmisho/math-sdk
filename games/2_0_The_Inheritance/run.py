"""Fast development runner for The Inheritance.

This runner intentionally bypasses the full SDK book-generation distribution loop.
Use it while feature logic is being built and validated.
"""

from gamestate import GameState
from game_config import GameConfig


if __name__ == "__main__":
    config = GameConfig()
    game = GameState(config)

    print("Running The Inheritance fast feature check...")

    for sim in range(20):
        game.betmode = "base"
        game.criteria = "basegame"
        game.reset_seed(sim)
        game.reset_book()
        game.betmode = "base"
        game.criteria = "basegame"

        game.draw_board()
        game.update_collection_state()
        game.evaluate_lines_board()
        game.win_manager.update_gametype_wins(game.gametype)
        game.evaluate_finalwin()

        print(
            {
                "sim": sim,
                "final_win": game.final_win,
                "events": len(game.book.events),
                "collected": game.collected_count,
                "mansion_level": game.mansion_level,
                "display_multiplier": game.display_multiplier,
            }
        )

    print("The Inheritance fast feature check complete.")
