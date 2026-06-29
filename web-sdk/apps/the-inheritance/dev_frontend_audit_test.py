"""Static frontend integration checks for The Inheritance.

These checks guard approval-critical wiring that is easy to regress in Svelte:
financial button gating, Legacy Key authority, RTP source-of-truth, and mounted
feature presentation components.
"""

from __future__ import annotations

from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
SRC_DIR = APP_DIR / "src"


def read(relative: str) -> str:
    return (SRC_DIR / relative).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, description: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {description}: {needle}")


def assert_not_contains(text: str, needle: str, description: str) -> None:
    if needle in text:
        raise AssertionError(f"Unexpected {description}: {needle}")


def validate_insufficient_balance_gate() -> None:
    ui = read("components/InheritanceUi.svelte")
    assert_contains(
        ui,
        "stateBet.balanceAmount > 0",
        "positive-balance requirement for Spin/Auto gating",
    )
    assert_contains(
        ui,
        "currentBetCost() <= stateBet.balanceAmount",
        "bet cost affordability requirement",
    )
    assert_not_contains(
        ui,
        "stateBet.balanceAmount <= 0 ||",
        "zero-balance affordability bypass",
    )


def validate_legacy_key_authority() -> None:
    handler = read("game/bookEventHandlerMap.ts")
    assert_contains(
        handler,
        "normalizeLegacyKeyCount(bookEvent.collected, target)",
        "collectionUpdate.collected authoritative meter update",
    )
    assert_contains(
        handler,
        "positions: bookEvent.positions",
        "Key positions reserved for animation/display",
    )


def validate_rtp_authority() -> None:
    config = read("game/config.ts")
    assert_not_contains(
        config,
        "PUBLIC_THE_INHERITANCE_RTP",
        "frontend-controlled RTP profile selector",
    )


def validate_feature_presenters() -> None:
    game = read("components/Game.svelte")
    assert_contains(game, "GlobalMultiplier from './GlobalMultiplier.svelte'", "GlobalMultiplier import")
    assert_contains(game, "<GlobalMultiplier />", "GlobalMultiplier mount")

    board = read("components/Board.svelte")
    assert_contains(
        board,
        "reel.reelState.motion === 'spinning'",
        "board click stop limited to actively spinning reels",
    )
    assert_not_contains(
        board,
        "const canStopByBoardClick = $derived(!context.stateXstateDerived.isIdle())",
        "idle-only board click stop gate",
    )

    free_spin_counter = read("components/FreeSpinCounter.svelte")
    assert_not_contains(
        free_spin_counter,
        "MainContainer",
        "free-spin counter generic desktop-only container dependency",
    )


def main() -> None:
    validate_insufficient_balance_gate()
    validate_legacy_key_authority()
    validate_rtp_authority()
    validate_feature_presenters()
    print("The Inheritance frontend audit validation: OK")


if __name__ == "__main__":
    main()
