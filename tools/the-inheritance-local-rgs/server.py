"""Development-only RGS bridge for The Inheritance.

The web client talks to this process through the same response contract it uses
for Stake Engine. Math stays in the Python SDK; the frontend receives only
settled books and never imports reel strips, probabilities, or payout logic.
"""

from __future__ import annotations

from bisect import bisect_right
import csv
from copy import deepcopy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import os
from pathlib import Path
import sys
import threading
import time
from urllib.parse import urlparse

import zstandard as zstd

from demo_settings import DEMO_CURRENCY, DEMO_STARTING_BALANCE_USD


REPO_ROOT = Path(__file__).resolve().parents[2]
GAME_DIR = REPO_ROOT / "games" / "2_0_The_Inheritance"
for import_path in (str(GAME_DIR), str(REPO_ROOT)):
    if import_path not in sys.path:
        sys.path.insert(0, import_path)

from game_config import GameConfig  # noqa: E402


API_AMOUNT_MULTIPLIER = 1_000_000
HOST = "127.0.0.1"
PORT = 3008
PUBLISH_DIR = GAME_DIR / "library" / "publish_files"
RTP_PROFILE_ROOT = GAME_DIR / "library" / "rtp_profiles"
ALLOW_PUBLISH_FALLBACK_ENV = "THE_INHERITANCE_ALLOW_PUBLISH_FALLBACK"


class PublishedMathLibrary:
    """Read settled books through the same lookup weights used by the RGS."""

    def __init__(self, modes: tuple[str, ...], books_dir: Path, weights_dir: Path) -> None:
        self.books_dir = books_dir
        self.weights_dir = weights_dir
        self.books = {mode: self.load_books(books_dir, mode) for mode in modes}
        self.weight_maps = {mode: self.load_weights(weights_dir, mode) for mode in modes}
        self.pools = {}
        for mode in modes:
            all_book_ids = list(self.books[mode])
            inactive_book_ids = [
                book_id for book_id in all_book_ids if not self.book_requires_active_legacy(self.books[mode][book_id])
            ]
            active_book_ids = [
                book_id for book_id in all_book_ids if self.book_requires_active_legacy(self.books[mode][book_id])
            ]
            if mode == "bonus":
                inactive_book_ids = all_book_ids
                active_book_ids = all_book_ids
            self.pools[mode] = {
                False: self.build_pool(mode, inactive_book_ids or all_book_ids),
                True: self.build_pool(mode, active_book_ids or all_book_ids),
            }

    @staticmethod
    def load_weights(weights_dir: Path, mode: str) -> dict[int, int]:
        weights = {}
        with (weights_dir / f"lookUpTable_{mode}_0.csv").open(newline="", encoding="utf-8") as handle:
            for book_id, weight, _payout in csv.reader(handle):
                weights[int(book_id)] = int(weight)
        return weights

    @staticmethod
    def load_books(books_dir: Path, mode: str) -> dict[int, dict]:
        path = books_dir / f"books_{mode}.jsonl.zst"
        books = {}
        with path.open("rb") as compressed:
            with zstd.ZstdDecompressor().stream_reader(compressed) as reader:
                text_reader = io.TextIOWrapper(reader, encoding="utf-8")
                for line in text_reader:
                    book = json.loads(line)
                    books[int(book["id"])] = book
        return books

    @staticmethod
    def book_requires_active_legacy(book: dict) -> bool:
        events = book.get("events", [])
        if any(event.get("type") == "legacyScatterCredit" and event.get("used") for event in events):
            return True

        collection_event = next(
            (
                event
                for event in events
                if event.get("type") == "collectionUpdate" and event.get("gameType") == "basegame"
            ),
            None,
        )
        if not collection_event:
            return False
        landed_keys = int(collection_event.get("landedKeys", len(collection_event.get("positions", []))))
        pre_spin_count = int(collection_event.get("collected", 0)) - landed_keys
        return pre_spin_count >= int(collection_event.get("target", 10))

    def build_pool(self, mode: str, book_ids: list[int]) -> tuple[list[tuple[int, int]], int]:
        cumulative = []
        running_total = 0
        for book_id in book_ids:
            weight = self.weight_maps[mode].get(book_id, 0)
            if weight <= 0:
                continue
            running_total += weight
            cumulative.append((running_total, book_id))
        if running_total <= 0:
            raise ValueError(f"No positive lookup weights for {mode}.")
        return cumulative, running_total

    def select_book(self, mode: str, roll: float, legacy_active: bool) -> dict:
        cumulative, total_weight = self.pools[mode][legacy_active]
        selected_weight = min(int(roll * total_weight), total_weight - 1)
        index = bisect_right(cumulative, (selected_weight, sys.maxsize))
        book_id = cumulative[index][1]
        return deepcopy(self.books[mode][book_id])


class LocalInheritanceRgs:
    def __init__(self) -> None:
        self.config = GameConfig()
        self.bet_modes = {mode.get_name(): mode for mode in self.config.bet_modes}
        self.books_dir = self.resolve_books_dir()
        self.weights_dir = self.resolve_weights_dir()
        self.math_library = PublishedMathLibrary(tuple(self.bet_modes), self.books_dir, self.weights_dir)
        self.currency = DEMO_CURRENCY
        self.starting_balance_usd = DEMO_STARTING_BALANCE_USD
        self.balance = self.to_api_amount(self.starting_balance_usd)
        self.spin_index = 0
        self.key_count = 0
        self.key_target = int(self.config.legacy_key_collection_target)
        self.rounds: dict[str, dict] = {}
        self.lock = threading.Lock()

    def resolve_weights_dir(self) -> Path:
        profile_dir = RTP_PROFILE_ROOT / self.config.rtp_profile.slug
        if profile_dir.exists():
            return profile_dir
        if os.getenv(ALLOW_PUBLISH_FALLBACK_ENV) != "1":
            raise FileNotFoundError(
                f"Missing RTP profile artifacts for {self.config.rtp_profile.slug}: {profile_dir}. "
                f"Generate profiles or set {ALLOW_PUBLISH_FALLBACK_ENV}=1 for legacy fallback."
            )
        print(
            f"[local-rgs] RTP profile {profile_dir} not found; falling back to {PUBLISH_DIR}",
            flush=True,
        )
        return PUBLISH_DIR

    @staticmethod
    def resolve_books_dir() -> Path:
        if not PUBLISH_DIR.exists():
            raise FileNotFoundError(f"Missing shared published book artifacts: {PUBLISH_DIR}")
        return PUBLISH_DIR

    @staticmethod
    def to_api_amount(amount: float) -> int:
        return round(float(amount) * API_AMOUNT_MULTIPLIER)

    @staticmethod
    def normalize_mode(mode: str) -> str:
        normalized = (mode or "base").lower().replace("-", "_")
        if normalized in {"scatterboost", "scatter_boost"}:
            return "scatter_boost"
        if normalized in {"bonus", "bonus_buy"}:
            return "bonus"
        return "base"

    def mode_cost(self, mode: str) -> float:
        bet_mode = self.bet_modes.get(mode)
        if bet_mode is None:
            raise ValueError(f"Unknown bet mode: {mode}")
        return float(bet_mode.get_cost())

    @staticmethod
    def deterministic_roll(index: int) -> float:
        value = (index + 1) * 1_103_515_245 + 12_345
        return (value & 0x7FFFFFFF) / 0x80000000

    @staticmethod
    def visible_board(reveal_event: dict) -> list[list[dict]]:
        visible = []
        for reel in reveal_event.get("board", []):
            visible.append(reel[1:-1] if len(reel) > 5 else reel)
        return visible

    @staticmethod
    def symbol_positions(board: list[list[dict]], symbol_name: str) -> list[dict]:
        return [
            {"reel": reel_index, "row": row_index}
            for reel_index, reel in enumerate(board)
            for row_index, symbol in enumerate(reel)
            if symbol.get("name") == symbol_name
        ]

    def apply_legacy_session_state(self, book: dict, mode: str) -> dict:
        events = book.get("events", [])

        if mode == "bonus":
            self.rewrite_collection_events(
                events,
                collected=self.key_count,
                landed_keys=0,
                positions=[],
            )
            return book

        reveal_event = next(
            (
                event
                for event in events
                if event.get("type") == "reveal" and event.get("gameType") == "basegame"
            ),
            None,
        )
        if not reveal_event:
            self.rewrite_collection_events(
                events,
                collected=self.key_count,
                landed_keys=0,
                positions=[],
            )
            return book

        board = self.visible_board(reveal_event)
        key_positions = self.symbol_positions(board, "H4")
        natural_scatters = len(self.symbol_positions(board, "S"))
        legacy_active = self.key_count >= self.key_target
        collected_after_spin = min(self.key_target, self.key_count + len(key_positions))
        legacy_event = next(
            (event for event in events if event.get("type") == "legacyScatterCredit" and event.get("used")),
            None,
        )
        legacy_used = bool(legacy_active and natural_scatters >= 2 and legacy_event)

        displayed_count = 0 if legacy_used else collected_after_spin
        self.rewrite_collection_events(
            events,
            collected=displayed_count,
            landed_keys=len(key_positions),
            positions=key_positions,
            collecting_game_type="basegame",
        )

        if legacy_event:
            legacy_event["collected"] = self.key_target
            legacy_event["target"] = self.key_target
            legacy_event["virtualScatters"] = 1
            legacy_event["naturalScatters"] = natural_scatters
            legacy_event["effectiveScatters"] = natural_scatters + 1
            legacy_event["used"] = legacy_used

        trigger_event = next((event for event in events if event.get("type") == "freeSpinTrigger"), None)
        if trigger_event:
            trigger_event["naturalScatters"] = natural_scatters
            trigger_event["effectiveScatters"] = natural_scatters + int(legacy_used)
            trigger_event["legacyCredit"] = int(legacy_used)

        self.key_count = 0 if legacy_used else collected_after_spin
        return book

    def rewrite_collection_events(
        self,
        events: list[dict],
        collected: int,
        landed_keys: int,
        positions: list[dict],
        collecting_game_type: str | None = None,
    ) -> None:
        """Mirror the authoritative session Key state onto every display event."""
        for event in events:
            if event.get("type") != "collectionUpdate":
                continue

            is_collecting_event = collecting_game_type is not None and event.get("gameType") == collecting_game_type
            event["collected"] = collected
            event["target"] = self.key_target
            event["landedKeys"] = landed_keys if is_collecting_event else 0
            event["positions"] = positions if is_collecting_event else []

    def authenticate(self) -> dict:
        return {
            "status": {"statusCode": "SUCCESS", "statusMessage": "Local Math SDK bridge"},
            "balance": {"amount": self.balance, "currency": self.currency},
            "config": {
                "jurisdiction": {
                    "socialCasino": False,
                    "disabledFullscreen": False,
                    "disabledTurbo": False,
                    "disabledSuperTurbo": False,
                    "disabledAutoplay": False,
                    "disabledSlamstop": False,
                    "disabledSpacebar": False,
                    "disabledBuyFeature": False,
                    "displayNetPosition": False,
                    "displayRTP": False,
                    "displaySessionTimer": False,
                    "minimumRoundDuration": 0,
                }
            },
        }

    def play(self, payload: dict) -> dict:
        with self.lock:
            mode = self.normalize_mode(str(payload.get("mode", "base")))
            currency = str(payload.get("currency", "USD"))
            amount = float(payload.get("amount", 0))
            cost_multiplier = self.mode_cost(mode)
            cost_api_amount = round(amount * cost_multiplier * API_AMOUNT_MULTIPLIER)
            if amount <= 0:
                return {"error": "INVALID_BET", "message": "Bet amount must be positive."}
            if self.balance < cost_api_amount:
                return {
                    "error": "INSUFFICIENT_BALANCE",
                    "message": f"Insufficient balance for {mode}.",
                }

            roll = self.deterministic_roll(self.spin_index)
            legacy_active = self.key_count >= self.key_target
            book = self.math_library.select_book(mode, roll, legacy_active)
            book = self.apply_legacy_session_state(book, mode)
            payout_multiplier = float(book["payoutMultiplier"]) / 100
            payout_amount = amount * payout_multiplier
            payout_api_amount = round(payout_amount * API_AMOUNT_MULTIPLIER)
            self.balance = max(0, self.balance - cost_api_amount + payout_api_amount)
            round_id = int(time.time_ns())
            self.spin_index += 1

            round_data = {
                "roundID": round_id,
                "amount": cost_api_amount,
                "payout": payout_amount,
                "payoutMultiplier": payout_multiplier,
                "active": False,
                "mode": mode,
                "event": "0",
                "state": book["events"],
            }
            self.rounds[str(round_id)] = deepcopy(round_data)

            return {
                "status": {"statusCode": "SUCCESS", "statusMessage": "Math SDK result"},
                "balance": {"amount": self.balance, "currency": currency},
                "round": round_data,
            }

    def end_round(self) -> dict:
        return {
            "status": {"statusCode": "SUCCESS", "statusMessage": "Round closed"},
            "balance": {"amount": self.balance, "currency": self.currency},
        }

    def replay(self, round_id: str) -> dict:
        round_data = self.rounds.get(str(round_id))
        if round_data is None:
            return {"error": "REPLAY_NOT_FOUND", "message": f"No local round found for {round_id}."}
        return deepcopy(round_data)


RGS = LocalInheritanceRgs()


class Handler(BaseHTTPRequestHandler):
    def send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_json({})

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        payload = self.read_json()
        try:
            if path == "/wallet/authenticate":
                self.send_json(RGS.authenticate())
            elif path == "/wallet/play":
                self.send_json(RGS.play(payload))
            elif path in {"/wallet/end-round", "/bet/event"}:
                self.send_json(RGS.end_round())
            else:
                self.send_json({"error": "NOT_FOUND", "message": path}, 404)
        except Exception as exc:
            self.send_json({"error": "LOCAL_MATH_ERROR", "message": str(exc)}, 500)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/health":
            self.send_json(
                {
                    "status": "ok",
                    "game": "2_0_The_Inheritance",
                    "rtp": RGS.config.rtp,
                    "profile": RGS.config.rtp_profile.slug,
                    "booksPath": str(RGS.books_dir),
                    "weightsPath": str(RGS.weights_dir),
                    "profileSelection": "server-side THE_INHERITANCE_RTP",
                    "sessionStateModel": "development-only process-local state",
                    "demo": True,
                    "startingBalance": RGS.starting_balance_usd,
                    "currency": RGS.currency,
                    "legacyKeys": RGS.key_count,
                    "legacyTarget": RGS.key_target,
                }
            )
        elif path.startswith("/bet/replay/"):
            round_id = path.rstrip("/").split("/")[-1]
            data = RGS.replay(round_id)
            self.send_json(data, 404 if data.get("error") else 200)
        else:
            self.send_json({"error": "NOT_FOUND", "message": path}, 404)

    def log_message(self, message: str, *args: object) -> None:
        print(f"[local-rgs] {message % args}", flush=True)


if __name__ == "__main__":
    print(f"The Inheritance local Math SDK bridge: http://{HOST}:{PORT}", flush=True)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
