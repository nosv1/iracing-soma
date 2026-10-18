from soma.event import Event
from soma.session import Session
from soma.snapshot import Snapshot
from soma.speaker import Speaker


def handle_events(session: Session, speaker: Speaker | None) -> None:
    for car in session.cars.values():
        if Event.CAR_NEW_LAP not in car.events:
            continue
        # is new lap

        if car.idx != session.player_car_idx:
            continue
        # is player

        if len(car.laps) <= 1:
            continue
        # is past lap 1

        if car.position <= 1:
            continue
        # is not p1

        delta_gaps = car.get_delta_gaps_ahead(session.cars, session.positions)
        largest_delta_gap = delta_gaps[0]
        largest_delta_gap_car = session.cars[largest_delta_gap.car_idx]
        car_ahead = session.cars[session.positions[car.position - 1]]
        if largest_delta_gap.delta_gap <= 0:
            caught_str = f"Caught P{largest_delta_gap_car.position} by {abs(round(largest_delta_gap.delta_gap, 1))} seconds\n"
            gap_to = car.get_gap_to(session.cars[largest_delta_gap.car_idx])
            gap_to_str = (
                "" if gap_to is None else f"Gap is {abs(round(gap_to, 1))} seconds"
            )
            gap_to_ahead = car.get_gap_to(car_ahead)
            gap_to_ahead_str = (
                ""
                if car_ahead == largest_delta_gap_car
                else (
                    ""
                    if gap_to_ahead is None
                    else f" and {abs(round(gap_to_ahead, 1))} seconds to car ahead"
                )
            )
            if speaker:
                speaker.add_to_queue(f"{caught_str}{gap_to_str}{gap_to_ahead_str}")


def handle_frame(old_session: Session | None, frame: Snapshot) -> Session:
    new_session = Session.from_frame(frame)
    if old_session is None:
        old_session = new_session

    if old_session.session_tick == new_session.session_tick:
        return old_session

    old_session.handle_frame(frame, new_session)
    return old_session
