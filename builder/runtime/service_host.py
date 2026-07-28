###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.4
# Arquivo....: builder/runtime/service_host.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Host responsável pelo ciclo de vida dos serviços.
#
###############################################################################

from __future__ import annotations

from enum import Enum, auto

from .container import ServiceContainer


class HostState(Enum):
    """
    Estados do Host.
    """

    CREATED = auto()

    STARTING = auto()

    RUNNING = auto()

    STOPPING = auto()

    STOPPED = auto()


class ServiceHost:
    """
    Host principal do Runtime.

    Responsável por controlar o ciclo de vida dos serviços.
    """

    ###########################################################################

    def __init__(self, container: ServiceContainer) -> None:

        self._container = container

        self._state = HostState.CREATED

    ###########################################################################

    @property
    def state(self) -> HostState:

        return self._state

    ###########################################################################

    @property
    def is_running(self) -> bool:

        return self._state is HostState.RUNNING

    ###########################################################################

    def start(self) -> None:
        """
        Inicializa o Host.
        """

        if self._state is HostState.RUNNING:
            return

        self._state = HostState.STARTING

        #
        # Futuramente:
        #
        # Bootstrap
        # Plugins
        # Workers
        # Scheduler
        # Hosted Services
        #

        self._state = HostState.RUNNING

    ###########################################################################

    def stop(self) -> None:
        """
        Finaliza o Host.
        """

        if self._state is HostState.STOPPED:
            return

        self._state = HostState.STOPPING

        #
        # Futuramente:
        #
        # Dispose
        # Shutdown Hooks
        #

        self._state = HostState.STOPPED

###############################################################################
# END FILE
###############################################################################