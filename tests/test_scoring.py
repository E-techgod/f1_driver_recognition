from scoring import compute_fantasy_score


def test_score_increases_with_wins():
    s1 = compute_fantasy_score(wins=5, podiums=5, races=20, points=200, dnfs=1)
    s2 = compute_fantasy_score(wins=10, podiums=5, races=20, points=200, dnfs=1)
    assert s2 > s1


def test_dnf_penalty_reduces_score():
    clean = compute_fantasy_score(wins=8, podiums=10, races=20, points=250, dnfs=0)
    messy = compute_fantasy_score(wins=8, podiums=10, races=20, points=250, dnfs=5)
    assert clean > messy


def test_handles_zero_races_without_crashing():
    s = compute_fantasy_score(wins=3, podiums=4, races=0, points=100, dnfs=1)
    assert isinstance(s, float)


def test_negative_inputs_are_clamped():
    s = compute_fantasy_score(wins=-1, podiums=-2, races=-3, points=-100, dnfs=-1)
    assert s == compute_fantasy_score()  # all clamped to zero
