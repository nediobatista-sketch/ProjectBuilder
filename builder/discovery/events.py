# events.py

###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.6
# Arquivo....: builder/discovery/events.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Sistema de eventos do Discovery.
#
###############################################################################

from __future__ import annotations

from collections import defaultdict
from typing import Callable


EventCallback = Callable[..., None]


class DiscoveryEvents:
    """
    Gerenciador de eventos do Discovery.
    """

    ###########################################################################

    def __init__(self):

        self._events = defaultdict(list)

    ###########################################################################

    def subscribe(

        self,

        event: str,

        callback: EventCallback,

    ) -> None:

        if callback not in self._events[event]:

            self._events[event].append(callback)

    ###########################################################################

    def unsubscribe(

        self,

        event: str,

        callback: EventCallback,

    ) -> None:

        if callback in self._events[event]:

            self._events[event].remove(callback)

    ###########################################################################

    def emit(

        self,

        event: str,

        *args,

        **kwargs,

    ) -> None:

        for callback in tuple(self._events[event]):

            callback(*args, **kwargs)

    ###########################################################################

    def clear(self):

        self._events.clear()

    ###########################################################################

    @property
    def events(self):

        return tuple(self._events.keys())


###############################################################################
# END FILE
###############################################################################