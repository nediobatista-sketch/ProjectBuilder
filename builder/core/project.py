###############################################################################
# ProjectBuilder
#
# EPIC.......: 003
# Sprint.....: 3.1
# Arquivo....: builder/core/project.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Representa um projeto do ProjectBuilder.
#
###############################################################################

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Project:
    """
    Representa um projeto.

    Esta classe contém apenas as informações principais.

    Componentes mais complexos (Workspace, Tasks,
    Pipeline etc.) serão adicionados posteriormente.
    """

    ###########################################################################

    name: str

    root: Path

    version: str = "0.1.0"

    description: str = ""

    ###########################################################################

    @property
    def exists(self) -> bool:

        return self.root.exists()

    ###########################################################################

    @property
    def builder_directory(self) -> Path:

        return self.root / "builder"

    ###########################################################################

    @property
    def tests_directory(self) -> Path:

        return self.root / "tests"

    ###########################################################################

    @property
    def docs_directory(self) -> Path:

        return self.root / "docs"

    ###########################################################################

    @property
    def scripts_directory(self) -> Path:

        return self.root / "scripts"

    ###########################################################################

    @property
    def pyproject(self) -> Path:

        return self.root / "pyproject.toml"

    ###########################################################################

    @property
    def readme(self) -> Path:

        return self.root / "README.md"


###############################################################################
# END FILE
###############################################################################