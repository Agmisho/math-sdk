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
        "stateBet.balanceAmount > 0 &&\n\t\tcurrentBetCost() <= stateBet.balanceAmount",
        "positive affordable cost requirement for Spin/Auto gating",
    )
    assert_contains(
        ui,
        "if (!canPayForBet()) return;",
        "handler-level insufficient-balance guard",
    )
    if ui.count("if (!canPayForBet()) return;") < 2:
        raise AssertionError("Spin and Auto handlers must both guard with canPayForBet().")
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
    if handler.count("stateGame.keyCounter =") != 1:
        raise AssertionError("Only collectionUpdate.collected may assign stateGame.keyCounter.")
    assert_not_contains(
        handler,
        "stateGame.keyCounter = 0",
        "legacyScatterCredit direct key meter reset",
    )
    assert_not_contains(
        handler,
        "stateGame.keyCounter = normalizeLegacyKeyCount(bookEvent.collected, stateGame.keyTarget)",
        "legacyScatterCredit direct key meter assignment",
    )
    assert_contains(
        handler,
        "positions: bookEvent.positions",
        "Key positions reserved for animation/display",
    )

    legacy_counter = read("components/LegacyKeyCounter.svelte")
    assert_not_contains(
        legacy_counter,
        "legacyScatterCredit: ({ used })",
        "LegacyKeyCounter display reset outside collectionUpdate.collected",
    )

    rgs = (APP_DIR.parents[2] / "tools" / "the-inheritance-local-rgs" / "server.py").read_text(
        encoding="utf-8",
    )
    assert_contains(
        rgs,
        "collection_event = self.collection_event_for_game(events, \"basegame\")",
        "local RGS reads Math SDK collectionUpdate event",
    )
    assert_not_contains(
        rgs,
        "key_positions = self.symbol_positions(board, \"H4\")",
        "local RGS reveal-board H4 recount for permanent Key state",
    )


def validate_rtp_authority() -> None:
    config = read("game/config.ts")
    session = read("components/TheInheritanceSession.svelte")
    game = read("components/Game.svelte")
    assert_contains(
        config,
        "PUBLIC_THE_INHERITANCE_RTP",
        "build-time RTP display binding",
    )
    assert_contains(
        config,
        "supportedRtpPercentages = [92, 93, 94, 95, 96, 97]",
        "approved RTP edition allow-list",
    )
    assert_not_contains(
        config,
        "const rtp = 0.97;",
        "hardcoded 97% frontend RTP",
    )
    assert_contains(
        session,
        "const requestSessionConfig = async () =>",
        "local RGS session-config verification",
    )
    assert_contains(
        session,
        "sessionConfig.rtp !== expectedRtp",
        "frontend/server RTP mismatch fail-closed check",
    )
    assert_contains(
        game,
        "DEV MATH ${stateMathSession.config.profile}",
        "local development RTP profile diagnostic label",
    )


def validate_replay_round_guard() -> None:
    state_url = (APP_DIR.parents[1] / "packages" / "state-shared" / "src" / "stateUrl.svelte.ts").read_text(
        encoding="utf-8",
    )
    local_client = (APP_DIR.parents[1] / "packages" / "rgs-requests" / "src" / "local-rgs-client.ts").read_text(
        encoding="utf-8",
    )
    session = read("components/TheInheritanceSession.svelte")
    ui = read("components/InheritanceUi.svelte")
    xstate = (APP_DIR.parents[1] / "packages" / "utils-xstate" / "src" / "createPrimaryMachines.ts").read_text(
        encoding="utf-8",
    )
    book_utils = (APP_DIR.parents[1] / "packages" / "utils-book" / "src" / "utils.ts").read_text(
        encoding="utf-8",
    )

    assert_contains(state_url, "| 'replayRound'", "local replay round URL parameter")
    assert_contains(state_url, "const isReplayMode = () => replay() || replayRound().length > 0", "combined replay mode helper")
    assert_contains(local_client, "path: `/bet/replay?roundID=${encodeURIComponent(options.roundID)}`", "local replayRound endpoint")
    assert_contains(session, "requestReplayRound", "app-local replayRound loader")
    assert_contains(ui, "const isReplayMode = () => stateUi.config.mode === 'replay'", "UI replay mode guard")
    assert_contains(xstate, "REPLAY_NO_BET", "xstate bet creation replay guard")
    assert_contains(book_utils, "stateUrlDerived.isReplayMode()", "end-event replay guard")


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
    validate_replay_round_guard()
    validate_feature_presenters()
    print("The Inheritance frontend audit validation: OK")


if __name__ == "__main__":
    main()
