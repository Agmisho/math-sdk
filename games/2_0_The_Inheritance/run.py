"""Main file for generating results for The Inheritance."""

import json
import os

from gamestate import GameState
from game_config import GameConfig
from game_optimization import OptimizationSetup
from optimization_program.run_script import OptimizationExecution
from utils.game_analytics.run_analysis import create_stat_sheet
from utils.rgs_verification import execute_all_tests
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs


def ensure_legacy_scatter_credit_event_configs(gamestate):
    """Ensure persistent-player-state event schema exists in generated configs.

    The event is only emitted when the player starts a paid spin with 10 stored
    Legacy Keys. Random book generation starts with empty player state, so the
    event may not naturally appear in sampled books. Frontend still needs the
    event schema for live persistent-state play.
    """
    event_template = {
        "type": "legacyScatterCredit",
        "collected": 10,
        "target": 10,
        "virtualScatters": 1,
        "naturalScatters": 2,
        "effectiveScatters": 3,
        "used": True,
        "gameType": "basegame",
    }
    for mode in ["base", "scatter_boost"]:
        path = os.path.join(gamestate.output_files.config_path, f"event_config_{mode}.json")
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="UTF-8") as file:
            data = json.load(file)
        data.setdefault("legacyScatterCredit", event_template)
        with open(path, "w", encoding="UTF-8") as file:
            json.dump(data, file, indent=4)


if __name__ == "__main__":

    num_threads = 10
    rust_threads = 20
    batching_size = 5000
    compression = True
    profiling = False

    num_sim_args = {
        "base": int(1e4),
        "scatter_boost": int(1e4),
        "bonus": int(1e4),
    }

    run_conditions = {
        "run_sims": True,
        "run_optimization": True,
        "run_analysis": True,
        "run_format_checks": True,
    }
    target_modes = list(num_sim_args.keys())

    config = GameConfig()
    gamestate = GameState(config)
    if run_conditions["run_optimization"] or run_conditions["run_analysis"]:
        OptimizationSetup(config)

    if run_conditions["run_sims"]:
        create_books(
            gamestate,
            config,
            num_sim_args,
            batching_size,
            num_threads,
            compression,
            profiling,
        )

    generate_configs(gamestate)
    ensure_legacy_scatter_credit_event_configs(gamestate)

    if run_conditions["run_optimization"]:
        OptimizationExecution().run_all_modes(config, target_modes, rust_threads)
        generate_configs(gamestate)
        ensure_legacy_scatter_credit_event_configs(gamestate)

    if run_conditions["run_analysis"]:
        custom_keys = [{"symbol": "scatter"}]
        create_stat_sheet(gamestate, custom_keys=custom_keys)

    if run_conditions["run_format_checks"]:
        execute_all_tests(config)
