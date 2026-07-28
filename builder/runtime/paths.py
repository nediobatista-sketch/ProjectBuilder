###############################################################################
# FILE: builder/runtime/paths.py
###############################################################################

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class RuntimePaths:
    """
    Diretórios principais do ProjectBuilder.
    """

    project_root: Path

    builder_root: Path

    tests: Path

    docs: Path

    templates: Path

    scripts: Path

    @classmethod
    def discover(cls) -> "RuntimePaths":

        root = Path(__file__).resolve().parents[2]

        return cls(
            project_root=root,
            builder_root=root / "builder",
            tests=root / "tests",
            docs=root / "docs",
            templates=root / "builder" / "templates",
            scripts=root / "scripts",
        )