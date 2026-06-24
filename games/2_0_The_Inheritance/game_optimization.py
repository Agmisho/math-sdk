"""Optimization setup for The Inheritance."""

from optimization_program.optimization_config import (
    ConstructScaling,
    ConstructParameters,
    ConstructConditions,
    ConstructFenceBias,
    verify_optimization_input,
)
from rtp_profiles import optimization_contributions


class OptimizationSetup:

    def __init__(self, game_config):
        self.game_config = game_config
        wincaps = {bm.get_name(): bm.get_wincap() for bm in game_config.bet_modes}
        base_rtp = optimization_contributions("base", game_config.rtp_profile)
        scatter_boost_rtp = optimization_contributions("scatter_boost", game_config.rtp_profile)
        bonus_rtp = optimization_contributions("bonus", game_config.rtp_profile)

        base_mode = {
            "conditions": {
                "wincap": ConstructConditions(
                    rtp=base_rtp["wincap"], av_win=wincaps["base"], search_conditions=wincaps["base"]
                ).return_dict(),
                "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                "freegame": ConstructConditions(
                    rtp=base_rtp["freegame"],
                    hr=255,
                    search_conditions={"symbol": "scatter"},
                ).return_dict(),
                "basegame": ConstructConditions(hr=3.5, rtp=base_rtp["basegame"]).return_dict(),
            },
            "scaling": ConstructScaling(
                [
                    {"criteria": "basegame", "scale_factor": 1.2, "win_range": (1, 2), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 1.5, "win_range": (10, 20), "probability": 1.0},
                    {"criteria": "freegame", "scale_factor": 0.8, "win_range": (1000, 2000), "probability": 1.0},
                    {"criteria": "freegame", "scale_factor": 1.2, "win_range": (3000, 4000), "probability": 1.0},
                ]
            ).return_dict(),
            "parameters": ConstructParameters(
                num_show=5000,
                num_per_fence=10000,
                min_m2m=4,
                max_m2m=8,
                pmb_rtp=1.0,
                sim_trials=5000,
                test_spins=[50, 100, 200],
                test_weights=[0.3, 0.4, 0.3],
                score_type="rtp",
            ).return_dict(),
            "distribution_bias": ConstructFenceBias(
                applied_criteria=["basegame"],
                bias_ranges=[(2.0, 3.0)],
                bias_weights=[0.5],
            ).return_dict(),
        }

        scatter_boost_mode = {
            "conditions": {
                "wincap": ConstructConditions(
                    rtp=scatter_boost_rtp["wincap"],
                    av_win=wincaps["scatter_boost"],
                    search_conditions=wincaps["scatter_boost"],
                ).return_dict(),
                "0": ConstructConditions(rtp=0, av_win=0, search_conditions=0).return_dict(),
                "freegame": ConstructConditions(
                    rtp=scatter_boost_rtp["freegame"],
                    hr=236,
                    search_conditions={"symbol": "scatter"},
                ).return_dict(),
                "basegame": ConstructConditions(
                    hr=3.5,
                    rtp=scatter_boost_rtp["basegame"],
                ).return_dict(),
            },
            "scaling": ConstructScaling(
                [
                    {"criteria": "basegame", "scale_factor": 1.2, "win_range": (1, 2), "probability": 1.0},
                    {"criteria": "basegame", "scale_factor": 1.5, "win_range": (10, 20), "probability": 1.0},
                    {"criteria": "freegame", "scale_factor": 0.8, "win_range": (1000, 2000), "probability": 1.0},
                    {"criteria": "freegame", "scale_factor": 1.2, "win_range": (3000, 4000), "probability": 1.0},
                ]
            ).return_dict(),
            "parameters": ConstructParameters(
                num_show=5000,
                num_per_fence=10000,
                min_m2m=4,
                max_m2m=8,
                pmb_rtp=1.0,
                sim_trials=5000,
                test_spins=[50, 100, 200],
                test_weights=[0.3, 0.4, 0.3],
                score_type="rtp",
            ).return_dict(),
            "distribution_bias": ConstructFenceBias(
                applied_criteria=["basegame"],
                bias_ranges=[(2.0, 3.0)],
                bias_weights=[0.5],
            ).return_dict(),
        }

        bonus_mode = {
            "conditions": {
                "wincap": ConstructConditions(
                    rtp=bonus_rtp["wincap"],
                    av_win=wincaps["bonus"],
                    search_conditions=wincaps["bonus"],
                ).return_dict(),
                "freegame": ConstructConditions(rtp=bonus_rtp["freegame"], hr="x").return_dict(),
            },
            "scaling": ConstructScaling(
                [
                    {"criteria": "freegame", "scale_factor": 1.2, "win_range": (1, 20), "probability": 1.0},
                    {"criteria": "freegame", "scale_factor": 0.5, "win_range": (20, 50), "probability": 1.0},
                    {"criteria": "freegame", "scale_factor": 1.8, "win_range": (50, 100), "probability": 1.0},
                    {"criteria": "freegame", "scale_factor": 0.8, "win_range": (1000, 2000), "probability": 1.0},
                    {"criteria": "freegame", "scale_factor": 1.2, "win_range": (3000, 4000), "probability": 1.0},
                ]
            ).return_dict(),
            "parameters": ConstructParameters(
                num_show=5000,
                num_per_fence=10000,
                min_m2m=4,
                max_m2m=8,
                pmb_rtp=1.0,
                sim_trials=5000,
                test_spins=[10, 20, 50],
                test_weights=[0.6, 0.2, 0.2],
                score_type="rtp",
            ).return_dict(),
            "distribution_bias": ConstructFenceBias(
                applied_criteria=["freegame"],
                bias_ranges=[(200.0, 350.0)],
                bias_weights=[0.3],
            ).return_dict(),
        }

        self.game_config.opt_params = {
            "base": base_mode,
            "scatter_boost": scatter_boost_mode,
            "bonus": bonus_mode,
        }

        verify_optimization_input(self.game_config, self.game_config.opt_params)
