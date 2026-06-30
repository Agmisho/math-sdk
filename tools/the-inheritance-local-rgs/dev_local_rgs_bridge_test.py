"""Focused checks for The Inheritance local RGS bridge.

Run from the repository root:

PYTHONPATH=. python tools/the-inheritance-local-rgs/dev_local_rgs_bridge_test.py
"""

from __future__ import annotations

from contextlib import contextmanager
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
from urllib.error import HTTPError
from urllib.request import urlopen


REPO_ROOT = Path(__file__).resolve().parents[2]
SERVER_PATH = REPO_ROOT / "tools" / "the-inheritance-local-rgs" / "server.py"


def load_server_module():
    sys.path.insert(0, str(SERVER_PATH.parent))
    spec = importlib.util.spec_from_file_location("the_inheritance_local_rgs_server", SERVER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load local RGS server module.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def balance_usd(module, rgs) -> float:
    return rgs.balance / module.API_AMOUNT_MULTIPLIER


def reset_game_config_singleton(module) -> None:
    module.GameConfig._instance = None


@contextmanager
def temporary_replay_db():
    original_value = os.environ.get("THE_INHERITANCE_REPLAY_DB")
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ["THE_INHERITANCE_REPLAY_DB"] = str(Path(temp_dir) / "inheritance_replays.sqlite3")
        try:
            yield
        finally:
            if original_value is None:
                os.environ.pop("THE_INHERITANCE_REPLAY_DB", None)
            else:
                os.environ["THE_INHERITANCE_REPLAY_DB"] = original_value


def validate_rtp_profile_binding(module) -> None:
    original_value = os.environ.get("THE_INHERITANCE_RTP")
    try:
        for percentage in range(92, 98):
            os.environ["THE_INHERITANCE_RTP"] = str(percentage)
            reset_game_config_singleton(module)
            rgs = module.LocalInheritanceRgs()

            assert rgs.config.rtp == percentage / 100
            assert rgs.config.rtp_profile.slug == f"rtp_{percentage}"
            assert rgs.books_dir == rgs.weights_dir == module.RELEASE_ROOT / f"rtp_{percentage}"
            assert rgs.profile_dir == module.RELEASE_ROOT / f"rtp_{percentage}"
            assert rgs.manifest["profile"] == f"rtp_{percentage}"
            assert rgs.manifest["rtp"] == percentage
            assert len(rgs.manifest_sha256) == 64
            for mode in ("base", "scatter_boost", "bonus"):
                assert (rgs.books_dir / f"books_{mode}.jsonl.zst").is_file()
                assert (rgs.weights_dir / f"lookUpTable_{mode}_0.csv").is_file()
    finally:
        if original_value is None:
            os.environ.pop("THE_INHERITANCE_RTP", None)
        else:
            os.environ["THE_INHERITANCE_RTP"] = original_value
        reset_game_config_singleton(module)


def validate_payout_multiplier_scaling(module) -> None:
    rgs = module.LocalInheritanceRgs()
    previous_balance = balance_usd(module, rgs)

    for _spin in range(50):
        result = rgs.play({"mode": "base", "amount": 1, "currency": "USD"})
        cost = result["round"]["amount"] / module.API_AMOUNT_MULTIPLIER
        payout_multiplier = result["round"]["payoutMultiplier"]
        expected_balance = previous_balance - cost + payout_multiplier
        actual_balance = result["balance"]["amount"] / module.API_AMOUNT_MULTIPLIER
        assert abs(expected_balance - actual_balance) < 1e-9

        if payout_multiplier > 0:
            assert payout_multiplier < 50, "Book payoutMultiplier must be unscaled before balance math."
            return

        previous_balance = actual_balance

    raise AssertionError("No winning base spin found in first 50 deterministic bridge spins.")


def validate_legacy_key_rewrite(module) -> None:
    rgs = module.LocalInheritanceRgs()
    legacy_reset_seen = False
    original_symbol_positions = rgs.symbol_positions

    def reject_key_recount(board, symbol_name):
        if symbol_name == "H4":
            raise AssertionError("Local RGS must not recount H4 symbols from the reveal board.")
        return original_symbol_positions(board, symbol_name)

    rgs.symbol_positions = reject_key_recount

    for _spin in range(350):
        result = rgs.play({"mode": "base", "amount": 1, "currency": "USD"})
        events = result["round"]["state"]

        for event in events:
            if event.get("type") != "collectionUpdate":
                continue

            if event.get("gameType") != "basegame":
                assert event.get("landedKeys", 0) == 0
                assert event.get("positions", []) == []

        if any(event.get("type") == "legacyScatterCredit" and event.get("used") for event in events):
            collection_events = [event for event in events if event.get("type") == "collectionUpdate"]
            assert collection_events
            assert all(event.get("collected") == 0 for event in collection_events)
            legacy_reset_seen = True
            break

    assert legacy_reset_seen, "Expected deterministic bridge sequence to consume Legacy credit."


def validate_collection_update_is_authoritative(module) -> None:
    rgs = module.LocalInheritanceRgs()
    key_board = [[{"name": "H4"} for _row in range(5)] for _reel in range(5)]
    book = {
        "events": [
            {
                "type": "reveal",
                "gameType": "basegame",
                "board": key_board,
            },
            {
                "type": "collectionUpdate",
                "collected": 7,
                "target": 10,
                "landedKeys": 1,
                "positions": [{"reel": 2, "row": 3}],
                "gameType": "basegame",
            },
        ]
    }

    rgs.apply_legacy_session_state(book, "base")
    collection_event = next(event for event in book["events"] if event["type"] == "collectionUpdate")

    assert rgs.key_count == 1
    assert collection_event["collected"] == 1
    assert collection_event["landedKeys"] == 1
    assert collection_event["positions"] == [{"reel": 2, "row": 3}]


def validate_bonus_preserves_key_state(module) -> None:
    rgs = module.LocalInheritanceRgs()
    rgs.key_count = 4
    result = rgs.play({"mode": "bonus", "amount": 1, "currency": "USD"})
    collection_events = [event for event in result["round"]["state"] if event.get("type") == "collectionUpdate"]

    assert rgs.key_count == 4
    assert collection_events
    assert all(event.get("collected") == 4 for event in collection_events)
    assert all(event.get("landedKeys", 0) == 0 for event in collection_events)
    assert all(event.get("positions", []) == [] for event in collection_events)


def validate_replay_returns_stored_round(module) -> None:
    with temporary_replay_db():
        rgs = module.LocalInheritanceRgs()
        result = rgs.play({"mode": "base", "amount": 1, "currency": "USD"})
        round_data = result["round"]
        replay = rgs.replay(str(round_data["roundID"]))

        assert replay["roundID"] == round_data["roundID"]
        assert replay["amount"] == round_data["amount"]
        assert replay["mode"] == round_data["mode"]
        assert replay["state"] == round_data["state"]
        assert replay["rtpProfile"] == rgs.config.rtp_profile.slug
        assert replay["manifestSha256"] == rgs.manifest_sha256
        assert rgs.replay("missing-round")["error"] == "REPLAY_NOT_FOUND"


def validate_persistent_replay_survives_restart(module) -> None:
    with temporary_replay_db():
        rgs = module.LocalInheritanceRgs()
        original_payloads = []
        for mode in ("base", "scatter_boost", "bonus"):
            result = rgs.play({"mode": mode, "amount": 1, "currency": "USD"})
            original_payloads.append(result["round"])

        balance_before_replay = rgs.balance
        key_count_before_replay = rgs.key_count
        restarted_rgs = module.LocalInheritanceRgs()
        restarted_balance_before_replay = restarted_rgs.balance
        restarted_key_count_before_replay = restarted_rgs.key_count

        for round_data in original_payloads:
            replay = restarted_rgs.replay(str(round_data["roundID"]))
            assert replay["roundID"] == round_data["roundID"]
            assert replay["mode"] == round_data["mode"]
            assert replay["state"] == round_data["state"]
            assert replay["payoutMultiplier"] == round_data["payoutMultiplier"]
            assert replay["replay"]["noBet"] is True

        assert rgs.balance == balance_before_replay
        assert rgs.key_count == key_count_before_replay
        assert restarted_rgs.balance == restarted_balance_before_replay
        assert restarted_rgs.key_count == restarted_key_count_before_replay


def validate_http_replay_route(module) -> None:
    original_rgs = module.RGS
    with temporary_replay_db():
        rgs = module.LocalInheritanceRgs()
        result = rgs.play({"mode": "base", "amount": 1, "currency": "USD"})
        round_data = result["round"]
        module.RGS = rgs

        server = module.ThreadingHTTPServer(("127.0.0.1", 0), module.Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base_url = f"http://127.0.0.1:{server.server_port}"

        try:
            with urlopen(f"{base_url}/health", timeout=10) as response:
                health = json.loads(response.read().decode("utf-8"))
            with urlopen(f"{base_url}/game/session-config", timeout=10) as response:
                session_config = json.loads(response.read().decode("utf-8"))
            assert health["profile"] == session_config["profile"]
            assert health["rtpPercentage"] == session_config["rtp"]
            assert health["manifestSha256"] == session_config["manifestSha256"]
            assert health["booksPath"] == health["weightsPath"] == session_config["releasePackagePath"]

            path_url = (
                f"{base_url}/bet/replay/2_0_The_Inheritance/1/base/"
                f"{round_data['roundID']}"
            )
            with urlopen(path_url, timeout=10) as response:
                replay = json.loads(response.read().decode("utf-8"))
            assert replay["roundID"] == round_data["roundID"]
            assert replay["state"] == round_data["state"]
            assert replay["rtpProfile"] == session_config["profile"]
            assert replay["manifestSha256"] == session_config["manifestSha256"]

            query_url = f"{base_url}/bet/replay?roundID={round_data['roundID']}"
            with urlopen(query_url, timeout=10) as response:
                replay = json.loads(response.read().decode("utf-8"))
            assert replay["roundID"] == round_data["roundID"]

            try:
                urlopen(f"{base_url}/bet/replay/2_0_The_Inheritance/1/base/missing-round", timeout=10)
            except HTTPError as error:
                assert error.code == 404
                missing = json.loads(error.read().decode("utf-8"))
                assert missing["error"] == "REPLAY_NOT_FOUND"
            else:
                raise AssertionError("Missing replay round must return HTTP 404.")
        finally:
            server.shutdown()
            server.server_close()
            module.RGS = original_rgs


def validate_insufficient_balance_rejects_without_state_change(module) -> None:
    with temporary_replay_db():
        rgs = module.LocalInheritanceRgs()
        rgs.balance = 0
        before_spin_index = rgs.spin_index
        before_key_count = rgs.key_count

        result = rgs.play({"mode": "base", "amount": 1, "currency": "USD"})

        assert result["error"] == "INSUFFICIENT_BALANCE"
        assert rgs.balance == 0
        assert rgs.spin_index == before_spin_index
        assert rgs.key_count == before_key_count
        assert rgs.replay_store.count() == 0

        rgs.balance = rgs.to_api_amount(10)
        result = rgs.play({"mode": "bonus", "amount": 1, "currency": "USD"})

        assert result["error"] == "INSUFFICIENT_BALANCE"
        assert rgs.balance == rgs.to_api_amount(10)
        assert rgs.spin_index == before_spin_index
        assert rgs.key_count == before_key_count
        assert rgs.replay_store.count() == 0


if __name__ == "__main__":
    server_module = load_server_module()
    validate_rtp_profile_binding(server_module)
    validate_payout_multiplier_scaling(server_module)
    validate_legacy_key_rewrite(server_module)
    validate_collection_update_is_authoritative(server_module)
    validate_bonus_preserves_key_state(server_module)
    validate_replay_returns_stored_round(server_module)
    validate_persistent_replay_survives_restart(server_module)
    validate_http_replay_route(server_module)
    validate_insufficient_balance_rejects_without_state_change(server_module)
    print("The Inheritance local RGS bridge validation: OK")
