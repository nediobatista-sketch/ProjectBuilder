###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.3
# Arquivo....: builder/runtime/lifetime.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Define o tempo de vida (Lifetime) dos serviços registrados no
#   ServiceContainer.
#
# DEPENDÊNCIAS
#   Nenhuma.
#
###############################################################################

from __future__ import annotations

from enum import Enum


class ServiceLifetime(str, Enum):
    """
    Define o ciclo de vida de um serviço registrado no ServiceContainer.

    SINGLETON
        Uma única instância durante toda a vida do Runtime.

    TRANSIENT
        Uma nova instância é criada a cada resolução.

    SCOPED
        Reservado para futuras implementações (escopos de execução).
    """

    SINGLETON = "singleton"

    TRANSIENT = "transient"

    SCOPED = "scoped"


###############################################################################
# END FILE
###############################################################################