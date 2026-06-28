"""Configuration for The Inheritance math model."""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode
from inheritance_feature_config import build_inheritance_feature_config
from rtp_profiles import resolve_rtp_profile


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
        self.rtp_profile = resolve_rtp_profile()
        self.rtp = self.rtp_profile.rtp
        self.allow_stateful_feature_from_base = True
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 5
        self.num_rows = [5] * self.num_reels

        # Board and Symbol Properties
        self.paytable = {
            (5, "W"): 20,
            (5, "H1"): 5,
            (4, "H1"): 2.5,
            (3, "H1"): 0.5,
            (5, "H2"): 5,
            (4, "H2"): 2.5,
            (3, "H2"): 0.5,
            (5, "H3"): 10,
            (4, "H3"): 5,
            (3, "H3"): 1,
            (5, "H4"): 10,
            (4, "H4"): 5,
            (3, "H4"): 1,
            (5, "H5"): 20,
            (4, "H5"): 1,
            (3, "H5"): 2,
            (5, "H6"): 20,
            (4, "H6"): 1,
            (3, "H6"): 2,
            (5, "H7"): 15,
            (4, "H7"): 6,
            (3, "H7"): 3,
            (5, "H8"): 12,
            (4, "H8"): 5,
            (3, "H8"): 2,
            (5, "H9"): 10,
            (4, "H9"): 4,
            (3, "H9"): 1.5,
            (5, "L1"): 1,
            (4, "L1"): 0.5,
            (3, "L1"): 0.1,
            (5, "L2"): 1,
            (4, "L2"): 0.5,
            (3, "L2"): 0.1,
            (5, "L3"): 1,
            (4, "L3"): 0.5,
            (3, "L3"): 0.1,
            (5, "L4"): 1,
            (4, "L4"): 0.5,
            (3, "L4"): 0.1,
            (5, "L5"): 1,
            (4, "L5"): 0.5,
            (3, "L5"): 0.1,
            (5, "L6"): 1.5,
            (4, "L6"): 0.4,
            (3, "L6"): 0.1,
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
        self.wild_substitution_blocked_symbols = [
            "H4",
            "S",
            "M2",
            "M5",
            "M10",
            "M20",
            "M100",
        ]

        self.freespin_triggers = {
            self.basegame_type: {3: 8, 4: 12, 5: 15},
            self.freegame_type: {2: 3, 3: 5, 4: 8, 5: 12},
        }
        self.legacy_key_collection_target = 10
        self.bonus_buy_free_spins = 10
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
        self.inheritance_feature_config = build_inheritance_feature_config(self)

        freegame_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR0": 1},
            },
            "scatter_triggers": {3: 50, 4: 20, 5: 5},
            "force_wincap": False,
            "force_freegame": True,
        }

        scatter_boost_freegame_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR0": 1},
            },
            # 8% relative lift over the normal 3-scatter trigger target.
            # Normal design reference: 3-scatter trigger ~= 1 in 255.
            # Boosted target reference: ~= 1 in 236 before final tuning.
            "scatter_triggers": {3: 50, 4: 20, 5: 5},
            "force_wincap": False,
            "force_freegame": True,
        }

        basegame_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR0": 1},
            },
            "force_wincap": False,
            "force_freegame": False,
        }

        wincap_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR0": 1, "WCAP": 8},
            },
            "scatter_triggers": {4: 1, 5: 2},
            "force_wincap": True,
            "force_freegame": True,
        }

        zerowin_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR0": 1},
            },
            "force_wincap": False,
            "force_freegame": False,
        }

        mode_maxwins = {"base": 5000, "scatter_boost": 5000, "bonus": 5000}
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
                    Distribution(criteria="basegame", quota=0.499, conditions=basegame_condition),
                ],
            ),
            BetMode(
                name="scatter_boost",
                cost=3.0,
                rtp=self.rtp,
                max_win=mode_maxwins["scatter_boost"],
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=mode_maxwins["scatter_boost"],
                        conditions=wincap_condition,
                    ),
                    Distribution(criteria="freegame", quota=0.108, conditions=scatter_boost_freegame_condition),
                    Distribution(criteria="0", quota=0.392, win_criteria=0.0, conditions=zerowin_condition),
                    Distribution(criteria="basegame", quota=0.499, conditions=basegame_condition),
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
                    Distribution(criteria="freegame", quota=0.999, conditions=freegame_condition),
                ],
            ),
        ]
