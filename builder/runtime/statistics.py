###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.3
# Arquivo....: builder/runtime/statistics.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Estruturas de estatísticas do ServiceContainer.
#
###############################################################################

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ContainerStatistics:
    """
    Estatísticas do ServiceContainer.
    """

    services: int = 0

    singletons: int = 0

    transients: int = 0

    scoped: int = 0

    instances: int = 0

    factories: int = 0

###############################################################################
# END FILE
###############################################################################