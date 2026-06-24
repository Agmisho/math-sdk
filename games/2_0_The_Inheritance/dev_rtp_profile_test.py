"""Development checks for The Inheritance RTP editions."""

from rtp_profiles import (
    SUPPORTED_RTP_PERCENTAGES,
    optimization_contributions,
    resolve_rtp_profile,
)


def main() -> None:
    assert resolve_rtp_profile("97").rtp == 0.97
    assert resolve_rtp_profile("96%").rtp == 0.96
    assert resolve_rtp_profile("0.92").rtp == 0.92

    for percentage in SUPPORTED_RTP_PERCENTAGES:
        profile = resolve_rtp_profile(percentage)
        for mode in ("base", "scatter_boost", "bonus"):
            contributions = optimization_contributions(mode, profile)
            assert round(sum(contributions.values()), 10) == profile.rtp
            assert contributions["wincap"] == 0.01

    try:
        resolve_rtp_profile("91")
    except ValueError:
        pass
    else:
        raise AssertionError("Unsupported RTP profile was accepted.")

    print("The Inheritance RTP profile checks passed.")


if __name__ == "__main__":
    main()
