###############################################################################
# ProjectBuilder
#
# EPIC.......: 003
# Sprint.....: 3.2
# Arquivo....: builder/core/workspace.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Representa o Workspace do projeto.
#
###############################################################################

from __future__ import annotations

from pathlib import Path

from .project import Project


class Workspace:
    """
    Workspace do projeto.

    Centraliza todos os diretórios utilizados pelo
    ProjectBuilder.
    """

    ###########################################################################

    def __init__(
        self,
        project: Project,
    ) -> None:

        self._project = project

    ###########################################################################
    # Projeto
    ###########################################################################

    @property
    def project(self) -> Project:

        return self._project

    ###########################################################################
    # Diretórios principais
    ###########################################################################

    @property
    def root(self) -> Path:

        return self._project.root

    ###########################################################################

    @property
    def builder(self) -> Path:

        return self.root / "builder"

    ###########################################################################

    @property
    def runtime(self) -> Path:

        return self.builder / "runtime"

    ###########################################################################

    @property
    def core(self) -> Path:

        return self.builder / "core"

    ###########################################################################

    @property
    def plugins(self) -> Path:

        return self.builder / "plugins"

    ###########################################################################

    @property
    def templates(self) -> Path:

        return self.builder / "templates"

    ###########################################################################

    @property
    def tests(self) -> Path:

        return self.root / "tests"

    ###########################################################################

    @property
    def docs(self) -> Path:

        return self.root / "docs"

    ###########################################################################

    @property
    def scripts(self) -> Path:

        return self.root / "scripts"

    ###########################################################################

    @property
    def dist(self) -> Path:

        return self.root / "dist"

    ###########################################################################

    @property
    def build(self) -> Path:

        return self.root / "build"

    ###########################################################################

    @property
    def cache(self) -> Path:

        return self.root / ".projectbuilder"

    ###########################################################################
    # Utilidades
    ###########################################################################

    def create(self) -> None:
        """
        Cria toda a estrutura do Workspace.
        """

        directories = (
            self.builder,
            self.runtime,
            self.core,
            self.plugins,
            self.templates,
            self.tests,
            self.docs,
            self.scripts,
            self.dist,
            self.build,
            self.cache,
        )

        for directory in directories:

            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

    ###########################################################################

    def exists(self) -> bool:

        return self.root.exists()

    ###########################################################################

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(root='{self.root}')"
        )


###############################################################################
# END FILE
###############################################################################