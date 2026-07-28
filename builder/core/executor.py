###############################################################################
# ProjectBuilder
#
# EPIC.......: 003
# Sprint.....: 3.5
# Arquivo....: builder/core/executor.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Executor de tarefas do ProjectBuilder.
#
###############################################################################

from __future__ import annotations

import time

from .task import Task


class Executor:
    """
    Executor responsável por executar tarefas.

    Nesta primeira versão o Executor possui apenas
    a responsabilidade de controlar o ciclo de vida
    das tarefas.

    Futuramente suportará:

        • execução paralela
        • timeout
        • cancelamento
        • retry
        • prioridades
        • métricas
        • logging
        • profiling
    """

    ###########################################################################

    def __init__(self) -> None:

        self._executed = 0

        self._failed = 0

        self._elapsed = 0.0

    ###########################################################################
    # Execução
    ###########################################################################

    def execute(
        self,
        task: Task,
    ) -> None:
        """
        Executa uma tarefa.
        """

        if not task.enabled:

            return

        start = time.perf_counter()

        try:

            task.initialize()

            task.execute()

            task.finalize()

            self._executed += 1

        except Exception:

            self._failed += 1

            raise

        finally:

            self._elapsed += (
                time.perf_counter() - start
            )

    ###########################################################################
    # Estatísticas
    ###########################################################################

    @property
    def executed(self) -> int:

        return self._executed

    ###########################################################################

    @property
    def failed(self) -> int:

        return self._failed

    ###########################################################################

    @property
    def elapsed(self) -> float:

        return self._elapsed

    ###########################################################################

    def reset(self) -> None:

        self._executed = 0

        self._failed = 0

        self._elapsed = 0.0

    ###########################################################################

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(executed={self._executed}, "
            f"failed={self._failed}, "
            f"elapsed={self._elapsed:.6f}s)"
        )


###############################################################################
# END FILE
###############################################################################