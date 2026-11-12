from dataclasses import dataclass, field

from soma.event_fact import EventFact
from soma.handler import (
    handle_car_events,
    handle_event_facts,
    handle_frame,
    handle_session_events,
)
from soma.session import Session
from soma.snapshot import Snapshot
from soma.speaker import Speaker


@dataclass
class Packet:
    session: Session
    event_facts: list[EventFact] = field(default_factory=list)


def do_stuff(
    session: Session | None, frame: Snapshot, speaker: Speaker | None
) -> Packet:
    session = handle_frame(session, frame)
    event_facts: list[EventFact] = []
    event_facts = handle_session_events(event_facts, session)
    event_facts = handle_car_events(event_facts, session)
    if speaker:
        handle_event_facts(event_facts, speaker)
    return Packet(session=session, event_facts=event_facts)
