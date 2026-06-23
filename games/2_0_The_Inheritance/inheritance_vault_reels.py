"""Deterministic Legacy Key to Vault Reel feature resolver."""

from __future__ import annotations

import random

from src.calculations.lines import Lines


class VaultReelFeatureMixin:
    """Adds optional Vault Reel transformations without replacing base math."""

    def reset_vault_reel_state(self) -> None:
        self.vault_reel_multiplier_sources = []
        self.vault_reel_transformations = []

    def get_vault_reel_config(self) -> dict:
        return self.config.inheritance_feature_config["vault_reel"]

    def can_resolve_vault_reels(self) -> bool:
        config = self.get_vault_reel_config()
        return bool(config["enabled"] and self.gametype in config["eligible_game_types"])

    def get_vault_key_positions(self) -> list[dict]:
        key_symbol = self.get_vault_reel_config()["key_symbol"]
        positions = []
        for reel_index, reel in enumerate(self.board):
            for row_index, symbol in enumerate(reel):
                if symbol.name == key_symbol:
                    positions.append({"reel": reel_index, "row": row_index, "symbol": symbol.name})
        return positions

    def clone_board_with_wild_reel(self, target_reel: int) -> list[list]:
        wild_symbol = self.get_vault_reel_config()["wild_symbol"]
        board = [list(reel) for reel in self.board]
        board[target_reel] = [self.create_symbol(wild_symbol) for _ in range(self.config.num_rows[target_reel])]
        return board

    def evaluate_vault_candidate_board(self, board: list[list], multiplier: int = 1) -> dict:
        return Lines.get_lines(
            board,
            self.config,
            multiplier_method="global",
            global_multiplier=multiplier,
        )

    def wins_by_line(self, win_data: dict) -> dict[int, dict]:
        return {int(win["meta"]["lineIndex"]): win for win in win_data["wins"]}

    def get_improved_vault_lines(self, before_win_data: dict, after_win_data: dict) -> list[dict]:
        before_by_line = self.wins_by_line(before_win_data)
        improved = []
        for after_win in after_win_data["wins"]:
            line_index = int(after_win["meta"]["lineIndex"])
            before_win = before_by_line.get(line_index)
            before_amount = float(before_win["meta"]["winWithoutMult"]) if before_win else 0.0
            after_amount = float(after_win["meta"]["winWithoutMult"])
            if after_amount > before_amount:
                improved.append(
                    {
                        "lineIndex": line_index,
                        "symbol": after_win["symbol"],
                        "kind": int(after_win["kind"]),
                        "positions": after_win["positions"],
                        "lineWinBeforeTransform": before_amount,
                        "lineWinBeforeMultiplier": after_amount,
                    }
                )
        return improved

    def display_position(self, position: dict) -> dict:
        return {"reel": int(position["reel"]), "row": int(position["row"]) + 1}

    def display_positions(self, positions: list[dict]) -> list[dict]:
        return [self.display_position(position) for position in positions]

    def get_transformed_reel_symbols(self, target_reel: int) -> list[dict]:
        return [
            {"reel": int(target_reel), "row": int(row_index), "symbol": symbol.name}
            for row_index, symbol in enumerate(self.board[target_reel])
        ]

    def get_preserved_multiplier_sources(self, original_symbols: list[dict]) -> list[dict]:
        values = self.get_vault_reel_config()["multiplier_values"]
        preserved = []
        for symbol in original_symbols:
            symbol_id = symbol["symbol"]
            if symbol_id in values:
                preserved.append(
                    {
                        "reel": int(symbol["reel"]),
                        "row": int(symbol["row"]),
                        "symbol": symbol_id,
                        "multiplier": int(values[symbol_id]),
                        "source": "transformedReelPreserved",
                    }
                )
        return preserved

    def choose_vault_reel_multiplier_source(self, key_position: dict) -> dict | None:
        weights = self.get_vault_reel_config()["multiplier_weights_by_game_type"].get(self.gametype, {})
        if not weights:
            return None

        symbols = list(weights.keys())
        chosen_symbol = random.choices(symbols, weights=[weights[symbol] for symbol in symbols], k=1)[0]
        value = self.get_vault_reel_config()["multiplier_values"][chosen_symbol]
        return {
            "reel": int(key_position["reel"]),
            "row": int(key_position["row"]),
            "symbol": chosen_symbol,
            "multiplier": int(value),
            "source": "vaultReelReveal",
        }

    def get_vault_reel_multiplier_positions(self) -> list[dict]:
        return list(getattr(self, "vault_reel_multiplier_sources", []))

    def resolve_inheritance_multiplier_stack(self) -> dict:
        """Apply the current title rule: the highest Diamond Seal value wins."""
        natural_sources = self.get_natural_multiplier_positions()
        vault_sources = self.get_vault_reel_multiplier_positions()
        all_sources = natural_sources + vault_sources
        combined = max([int(source["multiplier"]) for source in all_sources], default=1)
        return {
            "stackingRule": self.get_vault_reel_config()["multiplier_stacking"],
            "naturalSources": natural_sources,
            "vaultSources": vault_sources,
            "combinedMultiplier": int(combined),
            "appliedGlobalMultiplier": int(combined),
        }

    def build_vault_reel_affected_paylines(self, improved_lines: list[dict], final_win_data: dict) -> list[dict]:
        final_by_line = self.wins_by_line(final_win_data)
        affected = []
        for line in improved_lines:
            final_win = final_by_line.get(line["lineIndex"])
            if not final_win:
                continue
            affected.append(
                {
                    **line,
                    "positions": line["positions"],
                    "displayPositions": self.display_positions(line["positions"]),
                    "multiplierStackResult": int(final_win["meta"]["multiplier"]),
                    "finalLineWin": float(final_win["win"]),
                }
            )
        return affected

    def emit_vault_reel_event(
        self,
        key_position: dict,
        target_reel: int,
        original_symbols: list[dict],
        transformed_positions: list[dict],
        multiplier_source: dict | None,
        multiplier_stack: dict,
        affected_paylines: list[dict],
        total_before: float,
        total_after: float,
    ) -> None:
        event = {
            "index": len(self.book.events),
            "type": "vaultReelResolved",
            "gameType": self.gametype,
            "sourceKeySymbol": key_position["symbol"],
            "sourceKeyPosition": {"reel": int(key_position["reel"]), "row": int(key_position["row"])},
            "sourceKeyDisplayPosition": self.display_position(key_position),
            "targetReel": int(target_reel),
            "originalSymbols": original_symbols,
            "transformedPositions": transformed_positions,
            "transformedDisplayPositions": self.display_positions(transformed_positions),
            "wildSymbolId": self.get_vault_reel_config()["wild_symbol"],
            "multiplierSymbolId": multiplier_source["symbol"] if multiplier_source else None,
            "multiplierValue": int(multiplier_source["multiplier"]) if multiplier_source else 1,
            "multiplierSourcePosition": (
                {"reel": int(multiplier_source["reel"]), "row": int(multiplier_source["row"])}
                if multiplier_source
                else None
            ),
            "multiplierSourceDisplayPosition": self.display_position(multiplier_source) if multiplier_source else None,
            "multiplierStack": multiplier_stack,
            "affectedPaylines": affected_paylines,
            "totalSpinWinBefore": float(total_before),
            "totalSpinWinAfter": float(total_after),
            "capStatus": {
                "isCapped": bool(total_after >= self.config.wincap),
                "winCap": float(self.config.wincap),
            },
        }
        self.book.add_event(event)

    def resolve_vault_reels_before_line_evaluation(self) -> None:
        """Transform eligible Key reels before normal line evaluation."""
        if not self.can_resolve_vault_reels():
            return

        key_positions = self.get_vault_key_positions()
        if not key_positions:
            return

        max_reels = int(self.get_vault_reel_config()["max_reels_per_spin"])
        transformed_reels = set()
        current_win_data = self.evaluate_vault_candidate_board(self.board, multiplier=1)

        for key_position in key_positions:
            target_reel = int(key_position["reel"])
            if target_reel in transformed_reels or len(transformed_reels) >= max_reels:
                continue

            candidate_board = self.clone_board_with_wild_reel(target_reel)
            candidate_win_data = self.evaluate_vault_candidate_board(candidate_board, multiplier=1)
            improved_lines = self.get_improved_vault_lines(current_win_data, candidate_win_data)
            if not improved_lines or candidate_win_data["totalWin"] <= current_win_data["totalWin"]:
                continue

            original_symbols = self.get_transformed_reel_symbols(target_reel)
            preserved_sources = self.get_preserved_multiplier_sources(original_symbols)
            multiplier_source = self.choose_vault_reel_multiplier_source(key_position)

            self.board = candidate_board
            transformed_positions = [
                {"reel": int(target_reel), "row": int(row_index), "symbol": self.board[target_reel][row_index].name}
                for row_index in range(self.config.num_rows[target_reel])
            ]
            self.vault_reel_multiplier_sources.extend(preserved_sources)
            if multiplier_source:
                self.vault_reel_multiplier_sources.append(multiplier_source)
            self.get_special_symbols_on_board()

            multiplier_stack = self.resolve_inheritance_multiplier_stack()
            final_win_data = self.evaluate_vault_candidate_board(
                self.board,
                multiplier=multiplier_stack["combinedMultiplier"],
            )
            affected_paylines = self.build_vault_reel_affected_paylines(improved_lines, final_win_data)
            self.emit_vault_reel_event(
                key_position=key_position,
                target_reel=target_reel,
                original_symbols=original_symbols,
                transformed_positions=transformed_positions,
                multiplier_source=multiplier_source,
                multiplier_stack=multiplier_stack,
                affected_paylines=affected_paylines,
                total_before=current_win_data["totalWin"],
                total_after=final_win_data["totalWin"],
            )
            self.record(
                {
                    "kind": "vaultReel",
                    "symbol": key_position["symbol"],
                    "reel": target_reel,
                    "gametype": self.gametype,
                }
            )

            self.vault_reel_transformations.append(
                {
                    "sourceKeyPosition": key_position,
                    "targetReel": target_reel,
                    "affectedPaylines": affected_paylines,
                }
            )
            transformed_reels.add(target_reel)
            current_win_data = self.evaluate_vault_candidate_board(self.board, multiplier=1)
