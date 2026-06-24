"""RTP edition configuration for The Inheritance."""

from __future__ import annotations

from dataclasses import dataclass
import os


RTP_ENV_VAR = "THE_INHERITANCE_RTP"
SUPPORTED_RTP_PERCENTAGES = tuple(range(92, 98))
DEFAULT_RTP_PERCENTAGE = 97
WINCAP_RTP_CONTRIBUTION = 0.01

REFERENCE_CONTRIBUTIONS = {
    "base": {"freegame": 0.37, "basegame": 0.59},
    "scatter_boost": {"freegame": 0.39, "basegame": 0.57},
    "bonus": {"freegame": 0.96},
}


@dataclass(frozen=True)
class RtpProfile:
    percentage: int

    @property
    def rtp(self) -> float:
        return self.percentage / 100

    @property
    def slug(self) -> str:
        return f"rtp_{self.percentage}"


def parse_rtp_percentage(raw_value: str | float | int | None) -> int:
    """Normalize an RTP value expressed as 97, 97%, or 0.97."""
    if raw_value is None or str(raw_value).strip() == "":
        return DEFAULT_RTP_PERCENTAGE

    normalized = str(raw_value).strip().lower().removesuffix("%")
    try:
        numeric_value = float(normalized)
    except ValueError as exc:
        raise ValueError(f"Invalid {RTP_ENV_VAR} value: {raw_value!r}") from exc

    if numeric_value <= 1:
        numeric_value *= 100

    percentage = round(numeric_value)
    if abs(numeric_value - percentage) > 1e-9 or percentage not in SUPPORTED_RTP_PERCENTAGES:
        supported = ", ".join(f"{value}%" for value in SUPPORTED_RTP_PERCENTAGES)
        raise ValueError(f"{RTP_ENV_VAR} must be one of: {supported}")
    return percentage


def resolve_rtp_profile(raw_value: str | float | int | None = None) -> RtpProfile:
    if raw_value is None:
        raw_value = os.getenv(RTP_ENV_VAR)
    return RtpProfile(parse_rtp_percentage(raw_value))


def optimization_contributions(mode: str, profile: RtpProfile) -> dict[str, float]:
    """Scale the 97% design split while preserving feature/base proportions."""
    if mode not in REFERENCE_CONTRIBUTIONS:
        raise ValueError(f"Unknown bet mode for RTP profile: {mode}")

    reference = REFERENCE_CONTRIBUTIONS[mode]
    reference_remainder = sum(reference.values())
    target_remainder = profile.rtp - WINCAP_RTP_CONTRIBUTION
    scale = target_remainder / reference_remainder

    scaled = {
        criterion: round(contribution * scale, 10)
        for criterion, contribution in reference.items()
    }
    final_criterion = next(reversed(scaled))
    subtotal = WINCAP_RTP_CONTRIBUTION + sum(scaled.values())
    scaled[final_criterion] = round(
        scaled[final_criterion] + profile.rtp - subtotal,
        10,
    )
    return {"wincap": WINCAP_RTP_CONTRIBUTION, **scaled}
