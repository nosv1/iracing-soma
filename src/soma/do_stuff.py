from dataclasses import dataclass, field

from soma.event_fact import EventFact
from soma.handler import (
    handle_car_events,
    handle_event_facts,
    handle_frame,
    handle_player_events,
    handle_session_events,
)
from soma.player_constants import PlayerConstants
from soma.session import Session
from soma.snapshot import Snapshot
from soma.speaker import Speaker


@dataclass
class Packet:
    session: Session
    event_facts: list[EventFact] = field(default_factory=list)


def do_stuff(
    old_session: Session | None,
    frame: Snapshot,
    speaker: Speaker | None,
    player_constants: PlayerConstants | None,
) -> Packet:
    new_session = handle_frame(old_session, frame)
    event_facts: list[EventFact] = []
    event_facts.extend(handle_session_events(new_session))
    event_facts.extend(handle_car_events(new_session))
    if player_constants is not None:
        event_facts.extend(handle_player_events(new_session, player_constants))
    if speaker is not None:
        handle_event_facts(event_facts, speaker)
    return Packet(session=new_session, event_facts=event_facts)
