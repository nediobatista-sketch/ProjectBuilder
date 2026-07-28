###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.4
# Arquivo....: builder/runtime/service_scope.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Escopo de resolução de serviços.
#
###############################################################################

from __future__ import annotations

from typing import Any

from .container import ServiceContainer


class ServiceScope:
    """
    Representa um escopo de resolução de serviços.

    Atualmente reutiliza o container principal.

    Em versões futuras suportará:

        • Scoped Services
        • Transações
        • Contexto de execução
        • Pipelines
        • Plugins
        • Workers
    """

    ###########################################################################

    def __init__(
        self,
        container: ServiceContainer,
    ) -> None:

        self._container = container

    ###########################################################################

    @property
    def services(self) -> ServiceContainer:

        return self._container

    ###########################################################################

    def resolve(
        self,
        service: type,
    ) -> Any:

        return self._container.resolve(service)

    ###########################################################################

    def contains(
        self,
        service: type,
    ) -> bool:

        return self._container.contains(service)

    ###########################################################################

    def dispose(self) -> None:
        """
        Finaliza o escopo.

        Nesta primeira implementação não há recursos
        específicos para liberar.
        """

        return


###############################################################################
# END FILE
###############################################################################