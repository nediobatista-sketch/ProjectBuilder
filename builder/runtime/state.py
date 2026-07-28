###############################################################################
# FILE: builder/runtime/state.py
###############################################################################

"""
Runtime state definitions.

Este módulo define todos os estados possíveis do Runtime do
ProjectBuilder.
"""

from __future__ import annotations

from enum import Enum, auto


class RuntimeState(Enum):
    """
    Estados possíveis do Runtime.
    """

    CREATED = auto()

    INITIALIZING = auto()

    RUNNING = auto()

    STOPPING = auto()

    STOPPED = auto()

    FAILED = auto()

    def __str__(self) -> str:
        return self.name


###############################################################################
# END FILE
###############################################################################