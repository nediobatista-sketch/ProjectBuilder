###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.3
# Arquivo....: builder/runtime/container.py
# Versão.....: 1.1
#
# DESCRIÇÃO
#   Container de Injeção de Dependências (Dependency Injection Container).
#
###############################################################################

from __future__ import annotations

from typing import Any, Callable

from .descriptor import ServiceDescriptor
from .lifetime import ServiceLifetime
from .provider import ServiceProvider
from .statistics import ContainerStatistics


class ServiceContainer:
    """
    Container de Injeção de Dependências.

    Responsável pelo registro, resolução e gerenciamento
    do ciclo de vida dos serviços.
    """

    ###########################################################################

    def __init__(self) -> None:

        self._services: dict[type, ServiceDescriptor] = {}

        self._provider = ServiceProvider(self)

    ###########################################################################

    def register(
        self,
        service: type,
        implementation: type | None = None,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
    ) -> None:

        implementation = implementation or service

        descriptor = ServiceDescriptor(
            service_type=service,
            implementation=implementation,
            lifetime=lifetime,
        )

        self._services[service] = descriptor

    ###########################################################################

    def register_instance(
        self,
        service: type,
        instance: Any,
    ) -> None:

        descriptor = ServiceDescriptor(
            service_type=service,
            implementation=type(instance),
            lifetime=ServiceLifetime.SINGLETON,
            instance=instance,
        )

        self._services[service] = descriptor

    ###########################################################################

    def register_factory(
        self,
        service: type,
        factory: Callable[[], Any],
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
    ) -> None:

        descriptor = ServiceDescriptor(
            service_type=service,
            implementation=service,
            lifetime=lifetime,
            factory=factory,
        )

        self._services[service] = descriptor

    ###########################################################################

    def resolve(self, service: type) -> Any:

        if service not in self._services:
            raise KeyError(
                f"Service '{service.__name__}' não está registrado."
            )

        descriptor = self._services[service]

        #
        # Singleton
        #
        if descriptor.is_singleton:

            if descriptor.instance is None:
                descriptor.instance = self._provider.create(descriptor)

            return descriptor.instance

        #
        # Transient
        #
        return self._provider.create(descriptor)

    ###########################################################################

    def contains(self, service: type) -> bool:

        return service in self._services

    ###########################################################################

    def remove(self, service: type) -> None:

        self._services.pop(service, None)

    ###########################################################################

    def clear(self) -> None:

        self._services.clear()

    ###########################################################################

    def services(self) -> tuple[type, ...]:

        return tuple(self._services.keys())

    ###########################################################################

    def descriptors(self) -> tuple[ServiceDescriptor, ...]:

        return tuple(self._services.values())

    ###########################################################################

    def statistics(self) -> ContainerStatistics:
        """
        Retorna estatísticas do container.
        """

        stats = ContainerStatistics()

        stats.services = len(self._services)

        for descriptor in self._services.values():

            if descriptor.is_singleton:
                stats.singletons += 1

            elif descriptor.is_transient:
                stats.transients += 1

            elif descriptor.is_scoped:
                stats.scoped += 1

            if descriptor.instance is not None:
                stats.instances += 1

            if descriptor.factory is not None:
                stats.factories += 1

        return stats

    ###########################################################################

    def __contains__(self, service: type) -> bool:

        return self.contains(service)

    ###########################################################################

    def __len__(self) -> int:

        return len(self._services)

    ###########################################################################

    def __iter__(self):

        return iter(self._services.values())


###############################################################################
# END FILE
###############################################################################