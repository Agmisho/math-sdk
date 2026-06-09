from game_calculations import GameCalculations
from src.calculations.lines import Lines


class GameExecutables(GameCalculations):

    multiplier_symbol_values = {
        "M2": 2,
        "M5": 5,
        "M10": 10,
        "M20": 20,
        "M100": 100,
    }

    def get_landed_multiplier(self) -> int:
        """Return the highest Diamond Seal multiplier visible on the board."""
        landed_values = []
        for reel in self.board:
            for symbol in reel:
                if symbol.name in self.multiplier_symbol_values:
                    landed_values.append(self.multiplier_symbol_values[symbol.name])
        return max(landed_values) if landed_values else 1

    def evaluate_lines_board(self):
        """Populate win data, record wins, apply bonus multipliers, and emit events."""
        spin_multiplier = 1
        if self.gametype == self.config.freegame_type:
            spin_multiplier = self.get_landed_multiplier()

        self.win_data = Lines.get_lines(
            self.board,
            self.config,
            multiplier_method="global",
            global_multiplier=spin_multiplier,
        )
        Lines.record_lines_wins(self)
        self.win_manager.update_spinwin(self.win_data["totalWin"])
        Lines.emit_linewin_events(self)
