###############################################################################
# ProjectBuilder
#
# EPIC.......: 003
# Sprint.....: 3.7
# Arquivo....: builder/core/result.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Resultado padronizado das operações do ProjectBuilder.
#
###############################################################################

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any


@dataclass(slots=True)
class Result:
    """
    Resultado de uma operação.

    Todas as Tasks, Stages e Pipelines poderão retornar
    um objeto Result.
    """

    ###########################################################################
    # Estado
    ###########################################################################

    success: bool = True

    ###########################################################################

    message: str = ""

    ###########################################################################

    data: Any = None

    ###########################################################################

    errors: list[str] = field(default_factory=list)

    ###########################################################################

    warnings: list[str] = field(default_factory=list)

    ###########################################################################

    artifacts: list[Any] = field(default_factory=list)

    ###########################################################################

    elapsed: float = 0.0

    ###########################################################################
    # Controle interno
    ###########################################################################

    _start: float = field(
        default_factory=perf_counter,
        init=False,
        repr=False,
    )

    ###########################################################################
    # Operações
    ###########################################################################

    def finish(self) -> None:
        """
        Finaliza a medição de tempo.
        """

        self.elapsed = perf_counter() - self._start

    ###########################################################################

    def add_error(
        self,
        message: str,
    ) -> None:

        self.success = False

        self.errors.append(message)

    ###########################################################################

    def add_warning(
        self,
        message: str,
    ) -> None:

        self.warnings.append(message)

    ###########################################################################

    def add_artifact(
        self,
        artifact: Any,
    ) -> None:

        self.artifacts.append(artifact)

    ###########################################################################

    @property
    def has_errors(self) -> bool:

        return bool(self.errors)

    ###########################################################################

    @property
    def has_warnings(self) -> bool:

        return bool(self.warnings)

    ###########################################################################

    @property
    def artifact_count(self) -> int:

        return len(self.artifacts)

    ###########################################################################

    def __bool__(self) -> bool:

        return self.success


###############################################################################
# END FILE
###############################################################################