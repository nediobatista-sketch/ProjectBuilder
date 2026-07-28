from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict

from .event import Event
from .subscriber import EventSubscriber


class EventBus:
    """

    """

    def __init__(self) -> None:
        self._subscribers: DefaultDict[
            type[Event],
            list[EventSubscriber],
        ] = defaultdict(list)

    def subscribe(
        self,
        event_type: type[Event],
        subscriber: EventSubscriber,
    ) -> None:
        self._subscribers[event_type].append(subscriber)

    def subscribers_for(
        self,
        event_type: type[Event],
    ) -> tuple[EventSubscriber, ...]:
        return tuple(self._subscribers[event_type])



---
