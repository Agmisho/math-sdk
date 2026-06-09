from game_executables import GameExecutables


class GameStateOverride(GameExecutables):
    """Overrides and extension points for this title."""

    def reset_book(self):
        super().reset_book()
        self.collected_count = 0
        self.collection_target = 10
        self.mansion_level = 1
        self.display_multiplier = 1

    def assign_special_sym_function(self):
        self.special_symbol_functions = {
            "M2": [self.assign_fixed_mult_property],
            "M5": [self.assign_fixed_mult_property],
            "M10": [self.assign_fixed_mult_property],
            "M20": [self.assign_fixed_mult_property],
            "M100": [self.assign_fixed_mult_property],
        }

    def assign_fixed_mult_property(self, symbol) -> dict:
        multiplier_values = {
            "M2": 2,
            "M5": 5,
            "M10": 10,
            "M20": 20,
            "M100": 100,
        }
        symbol.assign_attribute({"multiplier": multiplier_values.get(symbol.name, 1)})

    def check_repeat(self):
        super().check_repeat()
        if self.repeat is False:
            win_criteria = self.get_current_betmode_distributions().get_win_criteria()
            if win_criteria is not None and self.final_win != win_criteria:
                self.repeat = True
                return
            if win_criteria is None and self.final_win == 0:
                self.repeat = True
                return
