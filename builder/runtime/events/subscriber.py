from __future__ import annotations

from abc import ABC, abstractmethod

from .event import Event


class EventSubscriber(ABC):

    @abstractmethod
    def handle(self, event: Event) -> None:
        """
        """
        raise NotImplementedError


---
