from soma.track_surface import TrackSurface


def test_is_not_in_world() -> None:
    for v in TrackSurface:
        if v.value == -1:
            assert v.is_not_in_world() is True
        else:
            assert v.is_not_in_world() is False
