from copy import deepcopy

from soma.do_stuff import Packet, do_stuff
from soma.event import FlagsChanged
from soma.event_fact import FlagsChangedFact
from soma.handler import handle_session_events
from soma.session import Session
from soma.session_flag import SessionFlag
from soma.session_type import SessionType
from soma.snapshot import Snapshot


def create_session_with_session_flags(session_flags: set[SessionFlag]) -> Session:
    return Session(
        session_id=0,
        session_num=0,
        session_time=0,
        session_tick=0,
        session_type=SessionType.RACE,
        player_car_idx=0,
        session_flags=session_flags,
    )


def test_from_frame_decodes_named_flags() -> None:
    session_flags = SessionFlag.get_flags_from_int(0x10040004)
    assert session_flags == {SessionFlag.GREEN}


def test_no_event_when_flags_unchanged(rolling_start_snapshots: list[Snapshot]) -> None:
    session: Session | None = None
    packet: Packet | None = None
    captured_sessions: list[Session] = []
    for frame in rolling_start_snapshots:
        packet = do_stuff(session=session, frame=frame, speaker=None)
        session = packet.session
        if 70.0 <= session.session_time <= 74.8:
            captured_sessions.append(deepcopy(session))
        elif session.session_time > 74.8:
            break
    assert len(captured_sessions) == 49
    for session in captured_sessions:
        for event in session.events:
            assert not isinstance(event, FlagsChanged)
    # # recording: tests/recordings/rolling_start (no change 70.0-74.8 s)
    # pytest.fail("TODO: frames with identical SessionFlags -> no FlagsChanged event")


def test_green_at_start_spoken_once(rolling_start_snapshots: list[Snapshot]) -> None:
    session: Session | None = None
    packet: Packet | None = None
    green_flags_changed_facts: list[FlagsChangedFact] = []
    for frame in rolling_start_snapshots:
        packet = do_stuff(session=session, frame=frame, speaker=None)
        session = packet.session
        for event_fact in packet.event_facts:
            if isinstance(event_fact, FlagsChangedFact):
                if event_fact.new_flag is SessionFlag.GREEN:
                    green_flags_changed_facts.append(event_fact)

    assert len(green_flags_changed_facts) == 1
    assert green_flags_changed_facts[0].new_flag is SessionFlag.GREEN
    # # recording: tests/recordings/rolling_start (green + start_go on at 83.88 s)
    # pytest.fail("TODO: whole fixture -> exactly one FlagsChangedFact(GREEN)")


def test_flag_turning_off_not_spoken(rolling_start_snapshots: list[Snapshot]) -> None:
    session: Session | None = None
    prev_session: Session | None = session
    packet: Packet | None = None
    for frame in rolling_start_snapshots:
        packet = do_stuff(session=session, frame=frame, speaker=None)
        session = packet.session
        if session.session_time >= 112.48:
            break
        prev_session = deepcopy(session)

    assert prev_session is not None
    assert session is not None

    green_flag = SessionFlag.GREEN
    assert green_flag in prev_session.session_flags
    assert green_flag not in session.session_flags
    if isinstance(packet, Packet):
        for event_fact in packet.event_facts:
            assert not isinstance(event_fact, FlagsChangedFact)
    # # recording: tests/recordings/rolling_start (green off at 112.48 s)
    # pytest.fail("TODO: green turns off -> no FlagsChangedFact")


def test_only_newly_on_flags_spoken() -> None:
    session = create_session_with_session_flags(session_flags={SessionFlag.GREEN})
    new_session = create_session_with_session_flags(
        session_flags={SessionFlag.GREEN, SessionFlag.YELLOW}
    )
    session.handle_frame(Snapshot({}, {}), new_session)
    event_facts = handle_session_events([], session)
    flag_changed_fact_found = False
    for event in event_facts:
        if isinstance(event, FlagsChangedFact):
            flag_changed_fact_found = True
            assert event.new_flag == SessionFlag.YELLOW
    assert flag_changed_fact_found is True
