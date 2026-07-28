###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.4
# Arquivo....: builder/runtime/service_collection.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   API pública para registro de serviços.
#
###############################################################################

from __future__ import annotations

from typing import Any

from .container import ServiceContainer
from .lifetime import ServiceLifetime


class ServiceCollection:
    """
    Coleção de serviços do Runtime.

    Encapsula o ServiceContainer e fornece uma API estável
    para registro de serviços.
    """

    ###########################################################################

    def __init__(self) -> None:

        self._container = ServiceContainer()

    ###########################################################################

    @property
    def container(self) -> ServiceContainer:
        """
        Retorna o container interno.
        """

        return self._container

    ###########################################################################

    def add_singleton(
        self,
        service: type,
        implementation: type | None = None,
    ) -> "ServiceCollection":

        self._container.register(
            service=service,
            implementation=implementation,
            lifetime=ServiceLifetime.SINGLETON,
        )

        return self

    ###########################################################################

    def add_transient(
        self,
        service: type,
        implementation: type | None = None,
    ) -> "ServiceCollection":

        self._container.register(
            service=service,
            implementation=implementation,
            lifetime=ServiceLifetime.TRANSIENT,
        )

        return self

    ###########################################################################

    def add_instance(
        self,
        service: type,
        instance: Any,
    ) -> "ServiceCollection":

        self._container.register_instance(
            service,
            instance,
        )

        return self

    ###########################################################################

    def contains(
        self,
        service: type,
    ) -> bool:

        return self._container.contains(service)

    ###########################################################################

    def clear(self) -> None:

        self._container.clear()

    ###########################################################################

    def __len__(self) -> int:

        return len(self._container)

###############################################################################
# END FILE
###############################################################################