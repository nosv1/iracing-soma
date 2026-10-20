import pytest

# Seen live 10-20, recording 20261020-112829 (gitignored): two impossible catches.
# Cause unknown (pit lap in the other car's lap? lap pairing by list index?).


def test_no_catch_of_60_seconds() -> None:
    pytest.fail("TODO: 'Caught P8 by 60.9 s' (gap 55.8) -> no CaughtFact")


def test_no_catch_of_7_seconds() -> None:
    pytest.fail("TODO: 'Caught P9 by 7.4 s' (gap 0.6) -> no CaughtFact")
