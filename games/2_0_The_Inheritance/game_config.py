"""Configuration for The Inheritance math model."""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "2_0_The_Inheritance"
        self.provider_number = 2
        self.working_name = "The Inheritance"
        self.wincap = 5000.0
        self.win_type = "lines"
        self.rtp = 0.9700
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 5
        self.num_rows = [5] * self.num_reels

        # Board and Symbol Properties
        self.paytable = {
            (5, "W"): 50,
            (4, "W"): 20,
            (3, "W"): 10,
            (5, "H1"): 80,
            (4, "H1"): 25,
            (3, "H1"): 12,
            (5, "H2"): 60,
            (4, "H2"): 20,
            (3, "H2"): 10,
            (5, "H3"): 45,
            (4, "H3"): 15,
            (3, "H3"): 8,
            (5, "H4"): 35,
            (4, "H4"): 12,
            (3, "H4"): 6,
            (5, "H5"): 25,
            (4, "H5"): 10,
            (3, "H5"): 5,
            (5, "H6"): 20,
            (4, "H6"): 8,
            (3, "H6"): 4,
            (5, "H7"): 15,
            (4, "H7"): 6,
            (3, "H7"): 3,
            (5, "H8"): 12,
            (4, "H8"): 5,
            (3, "H8"): 2,
            (5, "H9"): 10,
            (4, "H9"): 4,
            (3, "H9"): 1.5,
            (5, "L1"): 5,
            (4, "L1"): 1,
            (3, "L1"): 0.5,
            (5, "L2"): 4,
            (4, "L2"): 0.8,
            (3, "L2"): 0.4,
            (5, "L3"): 3,
            (4, "L3"): 0.7,
            (3, "L3"): 0.3,
            (5, "L4"): 2.5,
            (4, "L4"): 0.6,
            (3, "L4"): 0.25,
            (5, "L5"): 2,
            (4, "L5"): 0.5,
            (3, "L5"): 0.2,
            (5, "L6"): 1.5,
            (4, "L6"): 0.4,
            (3, "L6"): 0.15,
        }

        # 15 paylines from the supplied 5x5 layout image.
        # Row index 0 is the top row; row index 4 is the bottom row.
        self.paylines = {
            1: [0, 0, 0, 0, 0],
            2: [1, 1, 1, 1, 1],
            3: [2, 2, 2, 2, 2],
            4: [3, 3, 3, 3, 3],
            5: [4, 4, 4, 4, 4],
            6: [0, 1, 2, 3, 4],
            7: [4, 3, 2, 1, 0],
            8: [0, 1, 0, 1, 0],
            9: [1, 0, 1, 0, 1],
            10: [1, 2, 1, 2, 1],
            11: [2, 1, 2, 1, 2],
            12: [2, 3, 2, 3, 2],
            13: [3, 2, 3, 2, 3],
            14: [3, 4, 3, 4, 3],
            15: [4, 3, 4, 3, 4],
        }

        self.include_padding = True
        self.special_symbols = {
            "wild": ["W"],
            "scatter": ["S"],
            "multiplier": ["M2", "M5", "M10", "M20", "M100"],
        }

        self.freespin_triggers = {
            self.basegame_type: {3: 8, 4: 12, 5: 15},
            self.freegame_type: {2: 3, 3: 5, 4: 8, 5: 12},
        }
        self.anticipation_triggers = {
            self.basegame_type: min(self.freespin_triggers[self.basegame_type].keys()) - 1,
            self.freegame_type: min(self.freespin_triggers[self.freegame_type].keys()) - 1,
        }

        # Reels
        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv", "WCAP": "FRWCAP.csv"}
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))

        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]
        self.padding_symbol_values = {
            "M2": {"multiplier": {2: 1}},
            "M5": {"multiplier": {5: 1}},
            "M10": {"multiplier": {10: 1}},
            "M20": {"multiplier": {20: 1}},
            "M100": {"multiplier": {100: 1}},
        }

        freegame_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR0": 1},
            },
            "scatter_triggers": {3: 50, 4: 20, 5: 5},
            "mult_values": {
                self.basegame_type: {1: 1},
                self.freegame_type: {2: 70, 5: 45, 10: 20, 20: 8, 100: 1},
            },
            "force_wincap": False,
            "force_freegame": True,
        }

        basegame_condition = {
            "reel_weights": {self.basegame_type: {"BR0": 1}},
            "mult_values": {self.basegame_type: {1: 1}},
            "force_wincap": False,
            "force_freegame": False,
        }

        wincap_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR0": 1, "WCAP": 5},
            },
            "scatter_triggers": {4: 1, 5: 2},
            "mult_values": {
                self.basegame_type: {1: 1},
                self.freegame_type: {2: 70, 5: 45, 10: 20, 20: 8, 100: 1},
            },
            "force_wincap": True,
            "force_freegame": True,
        }

        zerowin_condition = {
            "reel_weights": {self.basegame_type: {"BR0": 1}},
            "mult_values": {
                self.basegame_type: {1: 1},
                self.freegame_type: {2: 100, 5: 40, 10: 10, 20: 2, 100: 1},
            },
            "force_wincap": False,
            "force_freegame": False,
        }

        mode_maxwins = {"base": 5000, "bonus": 5000}
        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=mode_maxwins["base"],
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwins["base"],
                        conditions=wincap_condition,
                    ),
                    Distribution(criteria="freegame", quota=0.1, conditions=freegame_condition),
                    Distribution(criteria="0", quota=0.4, win_criteria=0.0, conditions=zerowin_condition),
                    Distribution(criteria="basegame", quota=0.5, conditions=basegame_condition),
                ],
            ),
            BetMode(
                name="bonus",
                cost=100.0,
                rtp=self.rtp,
                max_win=mode_maxwins["bonus"],
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=True,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwins["bonus"],
                        conditions=wincap_condition,
                    ),
                    Distribution(criteria="freegame", quota=0.1, conditions=freegame_condition),
                ],
            ),
        ]
