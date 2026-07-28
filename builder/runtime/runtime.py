###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.4
# Arquivo....: builder/runtime/runtime.py
# Versão.....: 3.0
#
###############################################################################

from __future__ import annotations

from .container import ServiceContainer
from .context import RuntimeContext
from .dependency_graph import DependencyGraph
from .exceptions import (
    RuntimeAlreadyRunning,
    RuntimeNotRunning,
)
from .lifecycle import RuntimeState
from .service_host import (
    HostState,
    ServiceHost,
)


class Runtime:
    """
    Runtime principal do ProjectBuilder.
    """

    ###########################################################################

    def __init__(self) -> None:

        self.container = ServiceContainer()

        self.graph = DependencyGraph()

        self.host = ServiceHost(self.container)

        self.context = RuntimeContext.create()

    ###########################################################################

    def start(self) -> None:

        if self.host.state is HostState.RUNNING:
            raise RuntimeAlreadyRunning()

        self.host.start()

    ###########################################################################

    def stop(self) -> None:

        if self.host.state in (
            HostState.CREATED,
            HostState.STOPPED,
        ):
            raise RuntimeNotRunning()

        self.host.stop()

    ###########################################################################

    def restart(self) -> None:

        self.stop()

        self.start()

    ###########################################################################

    def status(self) -> RuntimeState:

        mapping = {

            HostState.CREATED: RuntimeState.CREATED,

            HostState.STARTING: RuntimeState.STARTING,

            HostState.RUNNING: RuntimeState.RUNNING,

            HostState.STOPPING: RuntimeState.STOPPING,

            HostState.STOPPED: RuntimeState.STOPPED,

        }

        return mapping[self.host.state]

    ###########################################################################

    @property
    def is_running(self) -> bool:

        return self.host.is_running

###############################################################################
# END FILE
###############################################################################