import pytest


def test_delta_gap_no_laps_either_car() -> None:
    pytest.fail("TODO: no laps this session, either car -> None")


def test_delta_gap_self_has_no_laps() -> None:
    pytest.fail("TODO: other has laps, self has none -> None, not KeyError")


def test_delta_gap_unequal_lap_counts() -> None:
    pytest.fail("TODO: 3 laps vs 2 -> compares laps 1 and 2 (last shared)")
