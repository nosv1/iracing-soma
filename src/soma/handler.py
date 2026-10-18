
from soma.session import Session
from soma.snapshot import Snapshot


def handle_frame(old_session: Session | None, frame: Snapshot) -> Session:
    new_session = Session.from_frame(frame)
    if old_session is None:
        old_session = new_session

    if old_session.session_tick == new_session.session_tick:
        return old_session

    old_session.handle_frame(frame, new_session)
    # do stuff here?
    return old_session
