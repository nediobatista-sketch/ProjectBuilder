###############################################################################
# FILE: builder/runtime/context.py
###############################################################################

from __future__ import annotations

from dataclasses import dataclass

from .metadata import RuntimeMetadata
from .paths import RuntimePaths
from .registry import RuntimeRegistry


@dataclass(slots=True)
class RuntimeContext:
    """
    Contexto do Runtime.
    """

    metadata: RuntimeMetadata

    paths: RuntimePaths

    registry: RuntimeRegistry

    @classmethod
    def create(cls) -> "RuntimeContext":

        return cls(
            metadata=RuntimeMetadata.current(),
            paths=RuntimePaths.discover(),
            registry=RuntimeRegistry(),
        )