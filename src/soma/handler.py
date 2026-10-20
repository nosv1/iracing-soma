from soma.event import Event
from soma.event_fact import CaughtFact, EventFact, GapFact
from soma.session import Session
from soma.snapshot import Snapshot
from soma.speaker import Speaker


def handle_event_facts(event_facts: list[EventFact], speaker: Speaker):
    for event_fact in event_facts:
        speaker.add_to_queue(event_fact.to_str())


def handle_events(session: Session) -> list[EventFact]:
    event_facts: list[EventFact] = []

    for car in session.cars.values():
        if Event.CAR_NEW_LAP not in car.events:
            continue
        # is new lap

        if car.idx != session.player_car_idx:
            continue
        # is player

        if len(car.laps[car.session_num]) <= 1:
            continue
        # is past lap 1

        if session.is_race():
            if car.position <= 1:
                continue
            # is not p1

            delta_gaps = car.get_delta_gaps_ahead(session.cars, session.positions)
            if len(delta_gaps) == 0:
                continue
            # delta gaps exist

            largest_delta_gap = delta_gaps[0]
            largest_delta_gap_car = session.cars[largest_delta_gap.car_idx]
            car_ahead = session.cars[session.positions[car.position - 1]]
            if largest_delta_gap.delta_gap <= 0:
                gap_to_largest_delta_gap_car = car.get_gap_to(largest_delta_gap_car)
                if gap_to_largest_delta_gap_car is not None:
                    event_facts.append(
                        CaughtFact(
                            # caught slow guy
                            pos=largest_delta_gap_car.position,
                            # by seconds
                            gain_s_as_positive=abs(largest_delta_gap.delta_gap),
                            # current gap
                            gap_fact=GapFact(
                                pos=largest_delta_gap_car.position,
                                gap_s_as_positive=abs(gap_to_largest_delta_gap_car),
                            ),
                        )
                    )
                if car_ahead.idx != largest_delta_gap_car.idx:
                    gap_to_car_ahead = car.get_gap_to(car_ahead)
                    if gap_to_car_ahead is not None:
                        event_facts.append(
                            # gap to car ahead
                            GapFact(
                                pos=car_ahead.position,
                                gap_s_as_positive=abs(gap_to_car_ahead),
                            )
                        )
        # is not race

    return event_facts


def handle_frame(old_session: Session | None, frame: Snapshot) -> Session:
    new_session = Session.from_frame(frame)
    if old_session is None:
        old_session = new_session

    if old_session.session_tick == new_session.session_tick:
        return old_session

    old_session.handle_frame(frame, new_session)
    return old_session
