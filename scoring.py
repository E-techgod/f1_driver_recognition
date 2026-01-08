# scoring.py
"""
Pure (testable) fantasy scoring functions.
Keep this file free of Streamlit / plotting side-effects.
"""

from __future__ import annotations


def safe_div(n: float, d: float) -> float:
    return (n / d) if d else 0.0


def compute_fantasy_score(
    *,
    wins: int = 0,
    podiums: int = 0,
    races: int = 0,
    poles: int = 0,
    points: float = 0.0,
    fastest_laps: int = 0,
    dnfs: int = 0,
) -> float:
    """
    Returns an unnormalized fantasy score.
    You can tweak weights later — tests ensure behavior doesn't break.
    """
    wins = max(0, int(wins))
    podiums = max(0, int(podiums))
    races = max(0, int(races))
    poles = max(0, int(poles))
    points = max(0.0, float(points))
    fastest_laps = max(0, int(fastest_laps))
    dnfs = max(0, int(dnfs))

    win_rate = safe_div(wins, races)
    podium_rate = safe_div(podiums, races)
    pole_to_win = safe_div(wins, poles)
    points_per_race = safe_div(points, races)
    fl_rate = safe_div(fastest_laps, races)
    dnf_rate = safe_div(dnfs, races)

    # Simple, interpretable weights (adjust later)
    score = 0.0
    score += wins * 10
    score += podiums * 6
    score += points_per_race * 2.5
    score += win_rate * 40
    score += podium_rate * 25
    score += pole_to_win * 10
    score += fl_rate * 15
    score -= dnf_rate * 30  # penalty

    return float(score)

