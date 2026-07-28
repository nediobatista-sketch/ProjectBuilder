###############################################################################
# ProjectBuilder
#
# EPIC.......: 003
# Sprint.....: 3.9
# Arquivo....: builder/core/manifest.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Manifesto do Projeto.
#
###############################################################################

from __future__ import annotations

from dataclasses import dataclass, field

from .artifact import Artifact


@dataclass(slots=True)
class Manifest:
    """
    Manifesto do ProjectBuilder.

    Centraliza todas as informações do projeto.

    No futuro este objeto poderá ser serializado para:

        projectbuilder.manifest.json

    funcionando como uma fotografia completa do projeto.
    """

    ###########################################################################
    # Informações do Projeto
    ###########################################################################

    name: str

    version: str

    description: str = ""

    ###########################################################################
    # Componentes registrados
    ###########################################################################

    plugins: list[str] = field(default_factory=list)

    tasks: list[str] = field(default_factory=list)

    stages: list[str] = field(default_factory=list)

    pipelines: list[str] = field(default_factory=list)

    ###########################################################################
    # Artefatos produzidos
    ###########################################################################

    artifacts: list[Artifact] = field(default_factory=list)

    ###########################################################################
    # Métodos de registro
    ###########################################################################

    def register_plugin(
        self,
        plugin: str,
    ) -> None:

        if plugin not in self.plugins:

            self.plugins.append(plugin)

    ###########################################################################

    def register_task(
        self,
        task: str,
    ) -> None:

        if task not in self.tasks:

            self.tasks.append(task)

    ###########################################################################

    def register_stage(
        self,
        stage: str,
    ) -> None:

        if stage not in self.stages:

            self.stages.append(stage)

    ###########################################################################

    def register_pipeline(
        self,
        pipeline: str,
    ) -> None:

        if pipeline not in self.pipelines:

            self.pipelines.append(pipeline)

    ###########################################################################

    def register_artifact(
        self,
        artifact: Artifact,
    ) -> None:

        self.artifacts.append(artifact)

    ###########################################################################
    # Consultas
    ###########################################################################

    @property
    def plugin_count(self) -> int:

        return len(self.plugins)

    ###########################################################################

    @property
    def task_count(self) -> int:

        return len(self.tasks)

    ###########################################################################

    @property
    def stage_count(self) -> int:

        return len(self.stages)

    ###########################################################################

    @property
    def pipeline_count(self) -> int:

        return len(self.pipelines)

    ###########################################################################

    @property
    def artifact_count(self) -> int:

        return len(self.artifacts)

    ###########################################################################

    def clear(self) -> None:

        self.plugins.clear()

        self.tasks.clear()

        self.stages.clear()

        self.pipelines.clear()

        self.artifacts.clear()

    ###########################################################################

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"version='{self.version}', "
            f"plugins={self.plugin_count}, "
            f"tasks={self.task_count}, "
            f"stages={self.stage_count}, "
            f"artifacts={self.artifact_count})"
        )


###############################################################################
# END FILE
###############################################################################