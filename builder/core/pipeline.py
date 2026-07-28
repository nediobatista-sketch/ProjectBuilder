###############################################################################
# ProjectBuilder
#
# EPIC.......: 003
# Sprint.....: 3.3
# Arquivo....: builder/core/pipeline.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Pipeline de execução do ProjectBuilder.
#
###############################################################################

from __future__ import annotations

from collections.abc import Callable


class Pipeline:
    """
    Pipeline de execução.

    Responsável por organizar a execução das etapas
    do ProjectBuilder.

    Exemplo:

        Discover
            ↓
        Analyze
            ↓
        Backup
            ↓
        Migration
            ↓
        Validation
            ↓
        Reports
    """

    ###########################################################################

    def __init__(self) -> None:

        self._stages: list[tuple[str, Callable]] = []

    ###########################################################################
    # Registro
    ###########################################################################

    def add(
        self,
        name: str,
        action: Callable,
    ) -> None:
        """
        Adiciona uma etapa ao pipeline.
        """

        self._stages.append(
            (
                name,
                action,
            )
        )

    ###########################################################################

    def clear(self) -> None:

        self._stages.clear()

    ###########################################################################

    @property
    def stages(self) -> tuple[tuple[str, Callable], ...]:

        return tuple(self._stages)

    ###########################################################################

    def execute(self) -> None:
        """
        Executa todas as etapas registradas.
        """

        for _, action in self._stages:

            action()

    ###########################################################################

    def __len__(self) -> int:

        return len(self._stages)

    ###########################################################################

    def __iter__(self):

        return iter(self._stages)

    ###########################################################################

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(stages={len(self._stages)})"
        )


###############################################################################
# END FILE
###############################################################################