###############################################################################
# ProjectBuilder
#
# EPIC.......: 003
# Sprint.....: 3.4
# Arquivo....: builder/core/task.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Classe base para todas as tarefas do ProjectBuilder.
#
###############################################################################

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Task(ABC):
    """
    Classe base de todas as tarefas do ProjectBuilder.

    Exemplos:

        DiscoveryTask

        BackupTask

        MigrationTask

        ValidationTask

        ReportTask

    Todas deverão herdar desta classe.
    """

    ###########################################################################
    # Informações
    ###########################################################################

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Nome da tarefa.
        """

    ###########################################################################

    @property
    def description(self) -> str:

        return ""

    ###########################################################################

    @property
    def enabled(self) -> bool:

        return True

    ###########################################################################
    # Ciclo de vida
    ###########################################################################

    def initialize(self) -> None:
        """
        Inicialização da tarefa.
        """

    ###########################################################################

    @abstractmethod
    def execute(self) -> None:
        """
        Executa a tarefa.
        """

    ###########################################################################

    def finalize(self) -> None:
        """
        Finalização da tarefa.
        """

    ###########################################################################

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}')"
        )


###############################################################################
# END FILE
###############################################################################