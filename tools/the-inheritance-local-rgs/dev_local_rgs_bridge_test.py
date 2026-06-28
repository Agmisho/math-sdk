"""Focused checks for The Inheritance local RGS bridge.

Run from the repository root:

PYTHONPATH=. python tools/the-inheritance-local-rgs/dev_local_rgs_bridge_test.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


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
    rgs = module.LocalInheritanceRgs()
    result = rgs.play({"mode": "base", "amount": 1, "currency": "USD"})
    round_data = result["round"]
    replay = rgs.replay(str(round_data["roundID"]))

    assert replay["roundID"] == round_data["roundID"]
    assert replay["amount"] == round_data["amount"]
    assert replay["mode"] == round_data["mode"]
    assert replay["state"] == round_data["state"]
    assert rgs.replay("missing-round")["error"] == "REPLAY_NOT_FOUND"


if __name__ == "__main__":
    server_module = load_server_module()
    validate_payout_multiplier_scaling(server_module)
    validate_legacy_key_rewrite(server_module)
    validate_bonus_preserves_key_state(server_module)
    validate_replay_returns_stored_round(server_module)
    print("The Inheritance local RGS bridge validation: OK")
