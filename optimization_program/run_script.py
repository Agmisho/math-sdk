import json
import toml
import subprocess
import os
import shutil
from src.config.paths import PATH_TO_GAMES, SETUP_PATH, OPTIMIZATION_PATH, PROJECT_PATH


class OptimizationExecution:
    """Handles execution of Rust optimization algorithm from python."""

    @staticmethod
    def load_math_config(filename: str) -> dict:
        """Load optimization parameter config file."""
        with open(filename, "r", encoding="UTF-8") as f:
            data = json.load(f)
        return data

    @staticmethod
    def run_opt_single_mode(game_config, mode, threads):
        """Create setup txt file for a single mode and run Rust executable binary."""
        os.chdir(PROJECT_PATH)
        filename = os.path.join(PATH_TO_GAMES, game_config.game_id, "library", "configs", "math_config.json")
        opt_config = OptimizationExecution.load_math_config(filename)

        opt_config = game_config.opt_params
        params = None
        for idx, obj in opt_config.items():
            if idx == mode:
                params = obj["parameters"]
        params["game_name"] = game_config.game_id
        params["path_to_games"] = "../games/"
        params["run_1000_batch"] = False
        params["bet_type"] = mode
        params["threads_for_fence_construction"] = threads
        params["threads_for_show_construction"] = threads

        assert params is not None, "Could not load optimization parameters."

        with open(SETUP_PATH, "w", encoding="UTF-8") as f:
            toml.dump(params, f)
        print(f"Running optimization for mode: {mode}")
        OptimizationExecution.run_rust_script()

    @staticmethod
    def run_all_modes(game_config, modes_to_run, rust_threads):
        """Loop through all game modes to run"""
        for mode in modes_to_run:
            OptimizationExecution.run_opt_single_mode(game_config, mode, rust_threads)

    @staticmethod
    def run_rust_script():
        """Run compiled binary and pip results to terminal."""
        binary_name = "PigFarmRust.exe" if os.name == "nt" else "PigFarmRust"
        binary_path = os.path.join(OPTIMIZATION_PATH, "target", "release", binary_name)
        use_cargo = os.environ.get("MATH_SDK_OPTIMIZER_USE_CARGO") == "1"

        if os.path.exists(binary_path) and not use_cargo:
            command = [binary_path]
            env = os.environ.copy()
        else:
            cargo = shutil.which("cargo")
            if cargo is None:
                raise RuntimeError(
                    "The optimizer requires either the bundled release binary or a working cargo installation."
                )
            command = [cargo, "run", "--release"]
            env = os.environ.copy()

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=OPTIMIZATION_PATH,
            check=True,
            env=env,
        )
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Error in optimization program.")
            print(result.stderr)
