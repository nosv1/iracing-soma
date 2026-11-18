from dataclasses import dataclass, field

from soma.event_fact import EventFact
from soma.handler import (
    handle_car_events,
    handle_event_facts,
    handle_frame,
    handle_player_events,
    handle_session_events,
)
from soma.player import Player
from soma.session import Session
from soma.snapshot import Snapshot
from soma.speaker import Speaker


@dataclass
class StuffPacket:
    session: Session
    player: Player | None
    event_facts: list[EventFact] = field(default_factory=list)


def do_stuff(
    old_session: Session | None,
    frame: Snapshot,
    speaker: Speaker | None,
    player: Player | None,
) -> StuffPacket:
    frame_packet = handle_frame(old_session=old_session, player=player, frame=frame)
    new_session = frame_packet.session
    player = frame_packet.player

    event_facts: list[EventFact] = []
    event_facts.extend(handle_session_events(new_session))
    event_facts.extend(handle_car_events(new_session))
    if player is not None:
        event_facts.extend(handle_player_events(new_session, player))
    if speaker is not None:
        handle_event_facts(event_facts, speaker)
    return StuffPacket(session=new_session, player=player, event_facts=event_facts)
