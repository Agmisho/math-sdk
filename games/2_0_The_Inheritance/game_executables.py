import random

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

    multiplier_target_weights = {
        None: 709,
        "M2": 90,
        "M5": 80,
        "M10": 70,
        "M20": 50,
        "M100": 1,
    }

    collection_symbol = "H4"  # Legacy Key

    def choose_controlled_multiplier_symbol(self):
        """Choose a free-spin multiplier symbol using the target hit-rate model."""
        total_weight = sum(self.multiplier_target_weights.values())
        roll = random.randint(1, total_weight)
        cumulative = 0
        for symbol_name, weight in self.multiplier_target_weights.items():
            cumulative += weight
            if roll <= cumulative:
                return symbol_name
        return None

    def inject_controlled_multiplier_symbol(self) -> list:
        """Inject the selected multiplier symbol into one actual board position."""
        symbol_name = self.choose_controlled_multiplier_symbol()
        if symbol_name is None:
            return []

        reel_index = random.randint(0, self.config.num_reels - 1)
        board_row_index = random.randint(0, len(self.board[reel_index]) - 1)

        self.board[reel_index][board_row_index] = self.symbol_storage.create_symbol(symbol_name)

        return [
            {
                "reel": reel_index,
                "row": board_row_index,
                "symbol": symbol_name,
                "multiplier": self.multiplier_symbol_values[symbol_name],
            }
        ]

    def get_landed_multiplier(self) -> int:
        """Return the highest Diamond Seal multiplier visible on the board."""
        landed_values = []
        for reel in self.board:
            for symbol in reel:
                if symbol.name in self.multiplier_symbol_values:
                    landed_values.append(self.multiplier_symbol_values[symbol.name])
        return max(landed_values) if landed_values else 1

    def update_bonus_multiplier_state(self, landed_multiplier: int) -> int:
        """Upgrade the persistent bonus multiplier without ever reducing it."""
        if not hasattr(self, "current_bonus_multiplier"):
            self.current_bonus_multiplier = 1
        if not hasattr(self, "highest_bonus_multiplier"):
            self.highest_bonus_multiplier = 1

        if landed_multiplier > self.current_bonus_multiplier:
            self.current_bonus_multiplier = landed_multiplier
        if self.current_bonus_multiplier > self.highest_bonus_multiplier:
            self.highest_bonus_multiplier = self.current_bonus_multiplier
        return self.current_bonus_multiplier

    def get_landed_multiplier_positions(self) -> list:
        """Return all visible Diamond Seal multiplier positions on the current board."""
        positions = []
        for reel_index, reel in enumerate(self.board):
            for row_index, symbol in enumerate(reel):
                if symbol.name in self.multiplier_symbol_values:
                    positions.append(
                        {
                            "reel": reel_index,
                            "row": row_index,
                            "symbol": symbol.name,
                            "multiplier": self.multiplier_symbol_values[symbol.name],
                        }
                    )
        return positions

    def emit_multiplier_update_event(
        self,
        applied_multiplier: int,
        landed_multiplier: int,
        positions: list,
    ) -> None:
        """Emit multiplier state for frontend animation during free spins."""
        event = {
            "index": len(self.book.events),
            "type": "multiplierUpdate",
            "appliedMultiplier": int(applied_multiplier),
            "landedMultiplier": int(landed_multiplier),
            "highestMultiplier": int(getattr(self, "highest_bonus_multiplier", applied_multiplier)),
            "positions": positions,
            "gameType": self.gametype,
        }
        self.book.add_event(event)

    def get_collection_positions(self) -> list:
        """Return all visible Legacy Key positions on the current board."""
        positions = []
        for reel_index, reel in enumerate(self.board):
            for row_index, symbol in enumerate(reel):
                if symbol.name == self.collection_symbol:
                    positions.append({"reel": reel_index, "row": row_index})
        return positions

    def calculate_mansion_level(self, collected_count: int) -> int:
        """Map collection progress to the mansion level display."""
        if collected_count >= 10:
            return 5
        if collected_count >= 9:
            return 4
        if collected_count >= 6:
            return 3
        if collected_count >= 3:
            return 2
        return 1

    def calculate_display_multiplier(self, collected_count: int) -> int:
        """Map collection progress to the side-panel multiplier display."""
        if collected_count >= 10:
            return 10
        if collected_count >= 9:
            return 7
        if collected_count >= 7:
            return 5
        if collected_count >= 5:
            return 4
        if collected_count >= 3:
            return 3
        if collected_count >= 1:
            return 2
        return 1

    def update_collection_state(self) -> None:
        """Collect Legacy Keys and emit a frontend state event."""
        positions = self.get_collection_positions()
        if positions:
            self.collected_count = min(self.collection_target, self.collected_count + len(positions))
        self.mansion_level = self.calculate_mansion_level(self.collected_count)
        self.display_multiplier = self.calculate_display_multiplier(self.collected_count)

        event = {
            "index": len(self.book.events),
            "type": "collectionUpdate",
            "collected": int(self.collected_count),
            "target": int(self.collection_target),
            "mansionLevel": int(self.mansion_level),
            "displayMultiplier": int(self.display_multiplier),
            "positions": positions,
            "gameType": self.gametype,
        }
        self.book.add_event(event)

    def evaluate_lines_board(self):
        """Populate win data, record wins, apply bonus multipliers, and emit events."""
        spin_multiplier = 1
        multiplier_positions = []
        landed_multiplier = 1

        if self.gametype == self.config.freegame_type:
            multiplier_positions = self.inject_controlled_multiplier_symbol()
            landed_multiplier = self.get_landed_multiplier()
            spin_multiplier = self.update_bonus_multiplier_state(landed_multiplier)
            self.emit_multiplier_update_event(spin_multiplier, landed_multiplier, multiplier_positions)

        self.win_data = Lines.get_lines(
            self.board,
            self.config,
            multiplier_method="global",
            global_multiplier=spin_multiplier,
        )
        Lines.record_lines_wins(self)
        self.win_manager.update_spinwin(self.win_data["totalWin"])
        Lines.emit_linewin_events(self)
