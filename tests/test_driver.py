from soma.driver import Driver


def test_valid_driver_dict(valid_driver_dict: dict[int, Driver]) -> None:
    assert valid_driver_dict.keys() == {0, 1}
    assert len(valid_driver_dict) == 2
