import logging
from dataclasses import dataclass

from soma.car import Car, CarDeltaGap
from soma.event import FlagsChanged, SessionChanged
from soma.event_fact import (
    CaughtFact,
    EventFact,
    FlagsChangedFact,
    GapFact,
    SessionChangedFact,
)
from soma.player import Player
from soma.session import Session
from soma.snapshot import Snapshot
from soma.speaker import Speaker

logger = logging.getLogger(__file__)


@dataclass
class FramePacket:
    session: Session
    player: Player | None


def handle_event_facts(event_facts: list[EventFact], speaker: Speaker) -> None:
    for event_fact in event_facts:
        speaker.add_to_queue(event_fact.to_str())


def handle_delta_gaps_exist(
    event_facts: list[EventFact],
    delta_gaps: list[CarDeltaGap],
    session: Session,
    player_car: Car,
) -> list[EventFact]:
    largest_delta_gap = delta_gaps[0]
    largest_delta_gap_car = session.cars[largest_delta_gap.car_idx]
    car_ahead = session.cars[session.positions[player_car.position - 1]]
    if largest_delta_gap.delta_gap <= 0:
        gap_to_largest_delta_gap_car = player_car.get_gap_to(largest_delta_gap_car)

        if gap_to_largest_delta_gap_car is not None:
            caught_fact = CaughtFact(
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
            event_facts.append(caught_fact)

        if car_ahead.idx != largest_delta_gap_car.idx:
            gap_to_car_ahead = player_car.get_gap_to(car_ahead)
            if gap_to_car_ahead is not None:
                event_facts.append(
                    # gap to car ahead
                    GapFact(
                        pos=car_ahead.position,
                        gap_s_as_positive=abs(gap_to_car_ahead),
                    )
                )

    return event_facts


def handle_session_events(session: Session) -> list[EventFact]:
    event_facts: list[EventFact] = []
    for event in session.events:
        if isinstance(event, FlagsChanged):
            for flag in event.new_flags:
                flags_changed_fact = FlagsChangedFact(flag)
                event_facts.append(flags_changed_fact)
            continue

        if isinstance(event, SessionChanged):
            session_changed_fact = SessionChangedFact()
            event_facts.append(session_changed_fact)
            continue
    return event_facts


def handle_car_events(session: Session) -> list[EventFact]:
    event_facts: list[EventFact] = []
    if not session.is_race():
        return event_facts

    for car in session.cars.values():
        if not car.new_lap_detected():
            continue

    return event_facts


def handle_player_events(session: Session, player: Player) -> list[EventFact]:
    event_facts: list[EventFact] = []
    if not session.is_race():
        return event_facts

    if session.player_car.is_p1():
        return event_facts

    if not session.player_car.new_lap_detected():
        return event_facts

    if not session.player_car.is_past_lap_one():
        return event_facts

    delta_gaps = session.player_car.get_delta_gaps_ahead(
        session.cars, session.positions
    )
    if len(delta_gaps) == 0:
        return event_facts
    # delta gaps exist

    event_facts = handle_delta_gaps_exist(
        event_facts=event_facts,
        delta_gaps=delta_gaps,
        session=session,
        player_car=session.player_car,
    )
    return event_facts


def handle_frame(
    old_session: Session | None, player: Player | None, frame: Snapshot
) -> FramePacket:
    new_session = Session.from_frame(frame)
    if old_session is None:
        old_session = new_session

    old_session.handle_frame(frame, new_session)
    if player is not None:
        player.handle_frame(old_session)
    return FramePacket(session=old_session, player=player)
