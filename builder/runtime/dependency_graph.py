###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.4
# Arquivo....: builder/runtime/dependency_graph.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Grafo de dependências dos serviços.
#
###############################################################################

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator


class DependencyGraph:
    """
    Grafo dirigido de dependências.

    Exemplo:

        Database
            └── Logger

        Repository
            ├── Database
            └── Cache
    """

    ###########################################################################

    def __init__(self) -> None:

        self._graph: dict[type, set[type]] = defaultdict(set)

    ###########################################################################

    def add_service(
        self,
        service: type,
    ) -> None:

        self._graph.setdefault(service, set())

    ###########################################################################

    def add_dependency(
        self,
        service: type,
        dependency: type,
    ) -> None:

        self._graph[service].add(dependency)

        self._graph.setdefault(dependency, set())

    ###########################################################################

    def dependencies_of(
        self,
        service: type,
    ) -> tuple[type, ...]:

        return tuple(self._graph.get(service, set()))

    ###########################################################################

    def contains(
        self,
        service: type,
    ) -> bool:

        return service in self._graph

    ###########################################################################

    def clear(self) -> None:

        self._graph.clear()

    ###########################################################################

    def __len__(self) -> int:

        return len(self._graph)

    ###########################################################################

    def __iter__(self) -> Iterator[type]:

        return iter(self._graph)

    ###########################################################################

    def items(self):

        return self._graph.items()

###############################################################################
# END FILE
###############################################################################