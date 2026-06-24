"""Development-only RGS bridge for The Inheritance.

The web client talks to this process through the same response contract it uses
for Stake Engine. Math stays in the Python SDK; the frontend receives only
settled books and never imports reel strips, probabilities, or payout logic.
"""

from __future__ import annotations

from bisect import bisect_right
import csv
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
from pathlib import Path
import sys
import threading
import time
from urllib.parse import urlparse

import zstandard as zstd


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


class PublishedMathLibrary:
    """Read settled books through the same lookup weights used by the RGS."""

    def __init__(self, modes: tuple[str, ...]) -> None:
        self.books = {mode: self.load_books(mode) for mode in modes}
        self.cumulative_weights = {}
        self.total_weights = {}
        for mode in modes:
            cumulative = []
            running_total = 0
            with (PUBLISH_DIR / f"lookUpTable_{mode}_0.csv").open(
                newline="",
                encoding="utf-8",
            ) as handle:
                for book_id, weight, _payout in csv.reader(handle):
                    running_total += int(weight)
                    cumulative.append((running_total, int(book_id)))
            self.cumulative_weights[mode] = cumulative
            self.total_weights[mode] = running_total

    @staticmethod
    def load_books(mode: str) -> dict[int, dict]:
        path = PUBLISH_DIR / f"books_{mode}.jsonl.zst"
        books = {}
        with path.open("rb") as compressed:
            with zstd.ZstdDecompressor().stream_reader(compressed) as reader:
                text_reader = io.TextIOWrapper(reader, encoding="utf-8")
                for line in text_reader:
                    book = json.loads(line)
                    books[int(book["id"])] = book
        return books

    def select_book(self, mode: str, roll: float) -> dict:
        total_weight = self.total_weights[mode]
        selected_weight = min(int(roll * total_weight), total_weight - 1)
        cumulative = self.cumulative_weights[mode]
        index = bisect_right(cumulative, (selected_weight, sys.maxsize))
        book_id = cumulative[index][1]
        return self.books[mode][book_id]


class LocalInheritanceRgs:
    def __init__(self) -> None:
        self.config = GameConfig()
        self.bet_modes = {mode.get_name(): mode for mode in self.config.bet_modes}
        self.math_library = PublishedMathLibrary(tuple(self.bet_modes))
        self.balance = 1000 * API_AMOUNT_MULTIPLIER
        self.spin_index = 0
        self.lock = threading.Lock()

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

    def authenticate(self) -> dict:
        return {
            "status": {"statusCode": "SUCCESS", "statusMessage": "Local Math SDK bridge"},
            "balance": {"amount": self.balance, "currency": "USD"},
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
            book = self.math_library.select_book(mode, roll)
            payout_multiplier = float(book["payoutMultiplier"])
            payout_amount = amount * payout_multiplier
            payout_api_amount = round(payout_amount * API_AMOUNT_MULTIPLIER)
            self.balance = max(0, self.balance - cost_api_amount + payout_api_amount)
            round_id = int(time.time_ns())
            self.spin_index += 1

            return {
                "status": {"statusCode": "SUCCESS", "statusMessage": "Math SDK result"},
                "balance": {"amount": self.balance, "currency": currency},
                "round": {
                    "roundID": round_id,
                    "amount": cost_api_amount,
                    "payout": payout_amount,
                    "payoutMultiplier": payout_multiplier,
                    "active": False,
                    "mode": mode,
                    "event": "0",
                    "state": book["events"],
                },
            }

    def end_round(self) -> dict:
        return {
            "status": {"statusCode": "SUCCESS", "statusMessage": "Round closed"},
            "balance": {"amount": self.balance, "currency": "USD"},
        }


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
                }
            )
        elif path.startswith("/bet/replay/"):
            self.send_json({"error": "REPLAY_NOT_AVAILABLE", "message": "Local replay requires a stored round."}, 404)
        else:
            self.send_json({"error": "NOT_FOUND", "message": path}, 404)

    def log_message(self, message: str, *args: object) -> None:
        print(f"[local-rgs] {message % args}", flush=True)


if __name__ == "__main__":
    print(f"The Inheritance local Math SDK bridge: http://{HOST}:{PORT}", flush=True)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
