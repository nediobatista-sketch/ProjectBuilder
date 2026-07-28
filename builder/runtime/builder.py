###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.4
# Arquivo....: builder/runtime/builder.py
# Versão.....: 3.0
#
###############################################################################

from __future__ import annotations

from .context import RuntimeContext
from .dependency_graph import DependencyGraph
from .runtime import Runtime
from .service_collection import ServiceCollection


class RuntimeBuilder:
    """
    Constrói uma instância configurada do Runtime.
    """

    ###########################################################################

    def __init__(self) -> None:

        self._services = ServiceCollection()

        self._graph = DependencyGraph()

    ###########################################################################

    @property
    def services(self) -> ServiceCollection:

        return self._services

    ###########################################################################

    @property
    def graph(self) -> DependencyGraph:

        return self._graph

    ###########################################################################

    def build(self) -> Runtime:
        """
        Constrói uma instância completamente inicializada do Runtime.
        """

        runtime = Runtime()

        runtime.context = RuntimeContext.create()

        runtime.container = self._services.container

        runtime.graph = self._graph

        return runtime


###############################################################################
# END FILE
###############################################################################