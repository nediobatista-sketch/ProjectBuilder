###############################################################################
# ProjectBuilder
#
# EPIC.......: 003
# Sprint.....: 3.6
# Arquivo....: builder/core/stage.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Representa uma etapa (Stage) do Pipeline.
#
###############################################################################

from __future__ import annotations

from collections.abc import Iterator

from .task import Task


class Stage:
    """
    Representa uma etapa do Pipeline.

    Um Stage é composto por uma coleção de Tasks que
    possuem o mesmo objetivo.

    Exemplo:

        Discovery

        Backup

        Migration

        Validation

        Reports
    """

    ###########################################################################

    def __init__(
        self,
        name: str,
        description: str = "",
    ) -> None:

        self._name = name

        self._description = description

        self._tasks: list[Task] = []

    ###########################################################################
    # Informações
    ###########################################################################

    @property
    def name(self) -> str:

        return self._name

    ###########################################################################

    @property
    def description(self) -> str:

        return self._description

    ###########################################################################
    # Tasks
    ###########################################################################

    def add(
        self,
        task: Task,
    ) -> None:

        self._tasks.append(task)

    ###########################################################################

    def remove(
        self,
        task: Task,
    ) -> None:

        self._tasks.remove(task)

    ###########################################################################

    def clear(self) -> None:

        self._tasks.clear()

    ###########################################################################

    @property
    def tasks(self) -> tuple[Task, ...]:

        return tuple(self._tasks)

    ###########################################################################
    # Utilidades
    ###########################################################################

    def __len__(self) -> int:

        return len(self._tasks)

    ###########################################################################

    def __iter__(self) -> Iterator[Task]:

        return iter(self._tasks)

    ###########################################################################

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(name='{self._name}', "
            f"tasks={len(self._tasks)})"
        )


###############################################################################
# END FILE
###############################################################################