###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.4
# Arquivo....: builder/runtime/bootstrap.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Bootstrap do Runtime.
#
###############################################################################

from __future__ import annotations

from typing import Callable

from .container import ServiceContainer


class Bootstrap:
    """
    Responsável pela inicialização do Runtime.

    Todas as rotinas de preparação são executadas
    antes do Runtime entrar em execução.
    """

    ###########################################################################

    def __init__(self) -> None:

        self._steps: list[Callable[[ServiceContainer], None]] = []

    ###########################################################################

    def register(
        self,
        action: Callable[[ServiceContainer], None],
    ) -> None:
        """
        Registra uma etapa de bootstrap.
        """

        self._steps.append(action)

    ###########################################################################

    def execute(
        self,
        services: ServiceContainer,
    ) -> None:
        """
        Executa todas as etapas registradas.
        """

        for action in self._steps:
            action(services)

    ###########################################################################

    @property
    def count(self) -> int:

        return len(self._steps)


###############################################################################
# END FILE
###############################################################################