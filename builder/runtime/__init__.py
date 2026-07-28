###############################################################################
# ProjectBuilder
#
# Arquivo....: builder/runtime/__init__.py
# Versão.....: 3.0
#
###############################################################################

"""
Pacote Runtime.

Os símbolos públicos são carregados sob demanda para evitar
dependências circulares durante a inicialização do pacote.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "Runtime",
    "RuntimeBuilder",
    "ServiceContainer",
    "ServiceCollection",
    "ServiceScope",
    "ServiceHost",
    "HostState",
]


def __getattr__(name: str) -> Any:

    if name == "Runtime":
        from .runtime import Runtime
        return Runtime

    if name == "RuntimeBuilder":
        from .builder import RuntimeBuilder
        return RuntimeBuilder

    if name == "ServiceContainer":
        from .container import ServiceContainer
        return ServiceContainer

    if name == "ServiceCollection":
        from .service_collection import ServiceCollection
        return ServiceCollection

    if name == "ServiceScope":
        from .service_scope import ServiceScope
        return ServiceScope

    if name == "ServiceHost":
        from .service_host import ServiceHost
        return ServiceHost

    if name == "HostState":
        from .service_host import HostState
        return HostState

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

###############################################################################
# END FILE
###############################################################################