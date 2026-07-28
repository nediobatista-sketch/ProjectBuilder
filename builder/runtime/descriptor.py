###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.3
# Arquivo....: builder/runtime/descriptor.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Representa um serviço registrado no ServiceContainer.
#
# DEPENDÊNCIAS
#   builder/runtime/lifetime.py
#
###############################################################################

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .lifetime import ServiceLifetime


@dataclass(slots=True)
class ServiceDescriptor:
    """
    Descreve um serviço registrado no ServiceContainer.

    Attributes
    ----------
    service_type
        Tipo utilizado para resolução.

    implementation
        Classe concreta que será instanciada.

    lifetime
        Tempo de vida do serviço.

    instance
        Instância armazenada (Singleton).

    factory
        Factory opcional para criação do serviço.
    """

    service_type: type

    implementation: type

    lifetime: ServiceLifetime

    instance: Any | None = None

    factory: Callable[[], Any] | None = None

    @property
    def is_singleton(self) -> bool:
        return self.lifetime == ServiceLifetime.SINGLETON

    @property
    def is_transient(self) -> bool:
        return self.lifetime == ServiceLifetime.TRANSIENT

    @property
    def is_scoped(self) -> bool:
        return self.lifetime == ServiceLifetime.SCOPED

    @property
    def has_instance(self) -> bool:
        return self.instance is not None

    @property
    def has_factory(self) -> bool:
        return self.factory is not None


###############################################################################
# END FILE
###############################################################################