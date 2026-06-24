from game_calculations import GameCalculations
from inheritance_symbol_roles import MULTIPLIER_SYMBOL_VALUES, SYMBOL_ROLE_KEY, role_symbol
from inheritance_vault_reels import VaultReelFeatureMixin
from src.calculations.lines import Lines


class GameExecutables(VaultReelFeatureMixin, GameCalculations):

    multiplier_symbol_values = MULTIPLIER_SYMBOL_VALUES

    collection_symbol = role_symbol(SYMBOL_ROLE_KEY)

    def get_landed_multiplier(self) -> int:
        """Return the highest visible Diamond Seal multiplier for this spin."""
        landed_values = [position["multiplier"] for position in self.get_landed_multiplier_positions()]
        return max(landed_values) if landed_values else 1

    def get_natural_multiplier_positions(self) -> list:
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

    def get_landed_multiplier_positions(self) -> list:
        """Return natural and Vault Reel multiplier sources for this spin."""
        return self.get_natural_multiplier_positions() + self.get_vault_reel_multiplier_positions()

    def emit_multiplier_update_event(
        self,
        applied_multiplier: int,
        landed_multiplier: int,
        positions: list,
    ) -> None:
        """Emit current-spin multiplier state for frontend animation."""
        event = {
            "index": len(self.book.events),
            "type": "multiplierUpdate",
            "multiplier": int(applied_multiplier),
            "appliedMultiplier": int(applied_multiplier),
            "landedMultiplier": int(landed_multiplier),
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
        if collected_count >= 8:
            return 4
        if collected_count >= 5:
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

    def can_collect_legacy_keys(self) -> bool:
        """Legacy Keys are collected only on paid base/scatter_boost spins."""
        if self.gametype != self.config.basegame_type:
            return False
        if getattr(self, "betmode", None) == "bonus":
            return False
        return True

    def update_collection_state(self) -> None:
        """Collect Legacy Keys and emit a frontend state event."""
        positions = self.get_collection_positions() if self.can_collect_legacy_keys() else []
        if positions:
            self.collected_count = min(self.collection_target, self.collected_count + len(positions))
        self.mansion_level = self.calculate_mansion_level(self.collected_count)
        self.display_multiplier = self.calculate_display_multiplier(self.collected_count)

        event = {
            "index": len(self.book.events),
            "type": "collectionUpdate",
            "collected": int(self.collected_count),
            "target": int(self.collection_target),
            "landedKeys": len(positions),
            "mansionLevel": int(self.mansion_level),
            "displayMultiplier": int(self.display_multiplier),
            "positions": positions,
            "gameType": self.gametype,
        }
        self.book.add_event(event)

    def evaluate_lines_board(self):
        """Populate win data, record wins, apply current-spin multipliers, and emit events."""
        spin_multiplier = 1
        landed_multiplier = 1
        multiplier_positions = self.get_landed_multiplier_positions()

        if multiplier_positions or self.gametype == self.config.freegame_type:
            landed_multiplier = self.get_landed_multiplier()
            spin_multiplier = landed_multiplier
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
