import pytest


def test_from_frame_decodes_named_flags() -> None:
    # recording: none
    pytest.fail(
        "TODO: SessionFlags 0x10040004 (green, servicible, start_hidden) -> {GREEN}"
    )


def test_no_event_when_flags_unchanged() -> None:
    # recording: tests/recordings/rolling_start (no change 70.0-74.8 s)
    pytest.fail("TODO: frames with identical SessionFlags -> no FlagsChanged event")


def test_green_at_start_spoken_once() -> None:
    # recording: tests/recordings/rolling_start (green + start_go on at 83.88 s)
    pytest.fail("TODO: whole fixture -> exactly one FlagsChangedFact(GREEN)")


def test_flag_turning_off_not_spoken() -> None:
    # recording: tests/recordings/rolling_start (green off at 112.48 s)
    pytest.fail("TODO: green turns off -> no FlagsChangedFact")


def test_only_newly_on_flags_spoken() -> None:
    # recording: none; rolling_start shows it once BLUE is a member
    #   (blue on at 91.88 s while green is still on)
    pytest.fail("TODO: {GREEN} -> {GREEN, YELLOW} -> one FlagsChangedFact(YELLOW)")
