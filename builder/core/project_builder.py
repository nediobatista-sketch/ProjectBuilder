###############################################################################
# ProjectBuilder
#
# EPIC.......: 003
# Sprint.....: 3.10
# Arquivo....: builder/core/project_builder.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Classe principal do Core do ProjectBuilder.
#
###############################################################################

from __future__ import annotations

from pathlib import Path

from builder.runtime import Runtime

from .executor import Executor
from .manifest import Manifest
from .pipeline import Pipeline
from .project import Project
from .workspace import Workspace


class ProjectBuilder:
    """
    Classe principal do Core.

    Esta classe representa o Builder completo e reúne
    todos os componentes necessários para executar um projeto.
    """

    ###########################################################################
    # Inicialização
    ###########################################################################

    def __init__(
        self,
        name: str,
        root: Path,
        version: str = "0.1.0",
        description: str = "",
    ) -> None:

        #######################################################################
        # Projeto
        #######################################################################

        self._project = Project(
            name=name,
            root=root,
            version=version,
            description=description,
        )

        #######################################################################
        # Workspace
        #######################################################################

        self._workspace = Workspace(
            self._project,
        )

        #######################################################################
        # Pipeline
        #######################################################################

        self._pipeline = Pipeline()

        #######################################################################
        # Executor
        #######################################################################

        self._executor = Executor()

        #######################################################################
        # Runtime
        #######################################################################

        self._runtime = Runtime()

        #######################################################################
        # Manifest
        #######################################################################

        self._manifest = Manifest(
            name=name,
            version=version,
            description=description,
        )

    ###########################################################################
    # Propriedades
    ###########################################################################

    @property
    def project(self) -> Project:

        return self._project

    ###########################################################################

    @property
    def workspace(self) -> Workspace:

        return self._workspace

    ###########################################################################

    @property
    def pipeline(self) -> Pipeline:

        return self._pipeline

    ###########################################################################

    @property
    def executor(self) -> Executor:

        return self._executor

    ###########################################################################

    @property
    def runtime(self) -> Runtime:

        return self._runtime

    ###########################################################################

    @property
    def manifest(self) -> Manifest:

        return self._manifest

    ###########################################################################
    # Operações
    ###########################################################################

    def initialize(self) -> None:
        """
        Inicializa o Builder.
        """

        self._workspace.create()

    ###########################################################################

    def start(self) -> None:
        """
        Inicializa o Runtime.
        """

        self._runtime.start()

    ###########################################################################

    def stop(self) -> None:
        """
        Finaliza o Runtime.
        """

        self._runtime.stop()

    ###########################################################################

    def execute(self) -> None:
        """
        Executa todas as etapas registradas no Pipeline.
        """

        self._pipeline.execute()

    ###########################################################################

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"project='{self.project.name}', "
            f"version='{self.project.version}')"
        )


###############################################################################
# END FILE
###############################################################################