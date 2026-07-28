###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.3
# Arquivo....: builder/runtime/registry.py
# Versão.....: 2.0
#
# DESCRIÇÃO
#   Registro central de serviços do Runtime.
#
# RESPONSABILIDADES
#   - Encapsular o ServiceContainer
#   - Expor uma API simples ao Runtime
#   - Centralizar registro e resolução de serviços
#
# DEPENDÊNCIAS
#   builder/runtime/container.py
#   builder/runtime/lifetime.py
#
###############################################################################

from __future__ import annotations

from typing import Any, Callable

from .container import ServiceContainer
from .lifetime import ServiceLifetime


class RuntimeRegistry:
    """
    Registro central de serviços do Runtime.

    Atua como uma camada de abstração sobre o ServiceContainer,
    permitindo que o Runtime não dependa diretamente da
    implementação interna do container.
    """

    ###########################################################################

    def __init__(self) -> None:

        self._container = ServiceContainer()

    ###########################################################################

    @property
    def container(self) -> ServiceContainer:
        """
        Retorna o ServiceContainer interno.
        """

        return self._container

    ###########################################################################

    def register(
        self,
        service: type,
        implementation: type | None = None,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
    ) -> None:
        """
        Registra um serviço.
        """

        self._container.register(
            service=service,
            implementation=implementation,
            lifetime=lifetime,
        )

    ###########################################################################

    def register_instance(
        self,
        service: type,
        instance: Any,
    ) -> None:
        """
        Registra uma instância existente.
        """

        self._container.register_instance(
            service=service,
            instance=instance,
        )

    ###########################################################################

    def register_factory(
        self,
        service: type,
        factory: Callable[[], Any],
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
    ) -> None:
        """
        Registra uma factory.
        """

        self._container.register_factory(
            service=service,
            factory=factory,
            lifetime=lifetime,
        )

    ###########################################################################

    def resolve(self, service: type) -> Any:
        """
        Resolve um serviço.
        """

        return self._container.resolve(service)

    ###########################################################################

    def contains(self, service: type) -> bool:
        """
        Verifica se um serviço está registrado.
        """

        return self._container.contains(service)

    ###########################################################################

    def remove(self, service: type) -> None:
        """
        Remove um serviço.
        """

        self._container.remove(service)

    ###########################################################################

    def clear(self) -> None:
        """
        Remove todos os serviços registrados.
        """

        self._container.clear()

    ###########################################################################

    def services(self) -> tuple[type, ...]:
        """
        Retorna todos os serviços registrados.
        """

        return self._container.services()

    ###########################################################################

    def descriptors(self):
        """
        Retorna todos os descritores registrados.
        """

        return self._container.descriptors()

    ###########################################################################

    def __contains__(self, service: type) -> bool:

        return self.contains(service)

    ###########################################################################

    def __len__(self) -> int:

        return len(self._container)


###############################################################################
# END FILE
###############################################################################