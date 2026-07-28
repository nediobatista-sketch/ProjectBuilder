###############################################################################
# ProjectBuilder
#
# Arquivo....: builder/runtime/lifecycle.py
# Versão.....: 2.0
#
###############################################################################

from __future__ import annotations

from enum import Enum, auto


class RuntimeState(Enum):
    """
    Estados do Runtime.
    """

    CREATED = auto()

    INITIALIZED = auto()

    STARTING = auto()

    RUNNING = auto()

    STOPPING = auto()

    STOPPED = auto()


class LifecycleManager:
    """
    Gerencia o ciclo de vida do Runtime.
    """

    ###########################################################################

    def __init__(self) -> None:

        self._state = RuntimeState.CREATED

    ###########################################################################

    @property
    def state(self) -> RuntimeState:

        return self._state

    ###########################################################################

    def initialize(self) -> None:

        self._state = RuntimeState.INITIALIZED

    ###########################################################################

    def start(self) -> None:

        self._state = RuntimeState.RUNNING

    ###########################################################################

    def stop(self) -> None:

        self._state = RuntimeState.STOPPED

###############################################################################
# END FILE
###############################################################################