from dataclasses import dataclass

from soma.event import Event
from soma.session import Session
from soma.snapshot import Snapshot


def handle_events(session: Session) -> None:
    for car in session.cars.values():
        if Event.CAR_NEW_LAP in car.events:
            if car.idx == session.player_car_idx:
                delta_gaps = car.get_delta_gaps_ahead(session.cars, session.positions)

    pass


def handle_frame(old_session: Session | None, frame: Snapshot) -> Session:
    new_session = Session.from_frame(frame)
    if old_session is None:
        old_session = new_session

    if old_session.session_tick == new_session.session_tick:
        return old_session

    old_session.handle_frame(frame, new_session)
    handle_events(old_session)
    return old_session
