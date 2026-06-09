from game_executables import GameExecutables
from src.events.events import fs_trigger_event


class GameStateOverride(GameExecutables):
    """Overrides and extension points for this title."""

    def reset_book(self):
        super().reset_book()
        if not hasattr(self, "collection_target"):
            self.collection_target = 10
        if not hasattr(self, "collected_count"):
            self.collected_count = 0

        # Credit is only available if the player had already collected all keys
        # before this paid spin/book started. Keys collected on the current spin
        # become available on the next eligible paid spin.
        self.legacy_scatter_credit_available = self.collected_count >= self.collection_target
        self.legacy_scatter_credit_used = False
        self.legacy_scatter_credit_event_emitted = False
        self.mansion_level = self.calculate_mansion_level(self.collected_count)
        self.display_multiplier = self.calculate_display_multiplier(self.collected_count)

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

    def is_legacy_scatter_credit_eligible(self, scatter_key: str = "scatter") -> bool:
        """Return whether the persistent key credit can help trigger free spins."""
        if self.gametype != self.config.basegame_type:
            return False
        if self.betmode == "bonus":
            return False
        if not getattr(self, "legacy_scatter_credit_available", False):
            return False
        return self.count_special_symbols(scatter_key) == 2

    def get_effective_scatter_count(self, scatter_key: str = "scatter") -> int:
        """Natural scatter count plus the virtual scatter credit when eligible."""
        natural_scatters = self.count_special_symbols(scatter_key)
        if self.is_legacy_scatter_credit_eligible(scatter_key):
            return natural_scatters + 1
        return natural_scatters

    def emit_legacy_scatter_credit_event(
        self,
        natural_scatters: int,
        effective_scatters: int,
        used: bool,
    ) -> None:
        """Emit virtual scatter-credit state for frontend animation."""
        if self.legacy_scatter_credit_event_emitted:
            return

        event = {
            "index": len(self.book.events),
            "type": "legacyScatterCredit",
            "collected": int(self.collected_count),
            "target": int(self.collection_target),
            "virtualScatters": 1,
            "naturalScatters": int(natural_scatters),
            "effectiveScatters": int(effective_scatters),
            "used": bool(used),
            "gameType": self.gametype,
        }
        self.book.add_event(event)
        self.legacy_scatter_credit_event_emitted = True

    def reset_legacy_collection_after_credit_use(self) -> None:
        """Reset key collection after the virtual scatter credit wins free games."""
        self.collected_count = 0
        self.legacy_scatter_credit_available = False
        self.legacy_scatter_credit_used = False
        self.mansion_level = self.calculate_mansion_level(self.collected_count)
        self.display_multiplier = self.calculate_display_multiplier(self.collected_count)
        event = {
            "index": len(self.book.events),
            "type": "collectionUpdate",
            "collected": int(self.collected_count),
            "target": int(self.collection_target),
            "mansionLevel": int(self.mansion_level),
            "displayMultiplier": int(self.display_multiplier),
            "positions": [],
            "gameType": self.gametype,
        }
        self.book.add_event(event)

    def check_fs_condition(self, scatter_key: str = "scatter") -> bool:
        """Check natural scatters plus any eligible Legacy Key virtual scatter credit."""
        min_trigger = min(self.config.freespin_triggers[self.gametype].keys())
        if self.get_effective_scatter_count(scatter_key) >= min_trigger and not self.repeat:
            return True
        return False

    def check_freespin_entry(self, scatter_key: str = "scatter") -> bool:
        """Allow forced freegame entry using natural scatters or the virtual credit."""
        if self.get_current_distribution_conditions()["force_freegame"] and self.get_effective_scatter_count(scatter_key) >= min(
            self.config.freespin_triggers[self.gametype].keys()
        ):
            return True
        self.repeat = True
        return False

    def run_freespin_from_base(self, scatter_key: str = "scatter") -> None:
        """Trigger free spins and reset Legacy Keys if the virtual scatter credit was used."""
        effective_scatters = self.get_effective_scatter_count(scatter_key)
        self.record(
            {
                "kind": effective_scatters,
                "symbol": scatter_key,
                "gametype": self.gametype,
                "legacyCredit": int(self.is_legacy_scatter_credit_eligible(scatter_key)),
            }
        )
        self.update_freespin_amount(scatter_key)
        if self.legacy_scatter_credit_used:
            self.reset_legacy_collection_after_credit_use()
        self.run_freespin()

    def update_freespin_amount(self, scatter_key: str = "scatter") -> None:
        """Set initial or retrigger free spins using effective scatter count when eligible."""
        natural_scatters = self.count_special_symbols(scatter_key)
        effective_scatters = self.get_effective_scatter_count(scatter_key)
        self.legacy_scatter_credit_used = effective_scatters > natural_scatters

        if self.legacy_scatter_credit_used:
            self.emit_legacy_scatter_credit_event(natural_scatters, effective_scatters, used=True)

        self.tot_fs = self.config.freespin_triggers[self.gametype][effective_scatters]
        if self.gametype == self.config.basegame_type:
            basegame_trigger, freegame_trigger = True, False
        else:
            basegame_trigger, freegame_trigger = False, True
        fs_trigger_event(self, basegame_trigger=basegame_trigger, freegame_trigger=freegame_trigger)

    def check_repeat(self):
        self.repeat_count += 1
        self.check_current_repeat_count()
