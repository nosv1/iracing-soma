from dataclasses import dataclass

from soma.handler import handle_event_facts, handle_events, handle_frame
from soma.session import Session
from soma.snapshot import Snapshot
from soma.speaker import Speaker


@dataclass
class Packet:
    session: Session


def do_stuff(session: Session | None, frame: Snapshot, speaker: Speaker) -> Packet:
    session = handle_frame(session, frame)
    event_facts = handle_events(session)
    handle_event_facts(event_facts, speaker)
    return Packet(session)
