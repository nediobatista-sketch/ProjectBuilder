###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.5
# Arquivo....: builder/runtime/plugin.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Interface base dos Plugins do Runtime.
#
###############################################################################

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class RuntimePlugin(ABC):
    """
    Classe base para todos os plugins do ProjectBuilder.

    Todo plugin deverá herdar desta classe.
    """

    ###########################################################################
    # Informações
    ###########################################################################

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Nome do plugin.
        """

    ###########################################################################

    @property
    def version(self) -> str:

        return "1.0.0"

    ###########################################################################

    @property
    def author(self) -> str:

        return "Unknown"

    ###########################################################################

    @property
    def description(self) -> str:

        return ""

    ###########################################################################
    # Ciclo de vida
    ###########################################################################

    def configure(self) -> None:
        """
        Executado antes da inicialização.
        """

    ###########################################################################

    def initialize(self) -> None:
        """
        Inicialização do plugin.
        """

    ###########################################################################

    def start(self) -> None:
        """
        Plugin iniciado.
        """

    ###########################################################################

    def stop(self) -> None:
        """
        Plugin finalizado.
        """

###############################################################################
# END FILE
###############################################################################