###############################################################################
# ProjectBuilder
#
# EPIC.......: 003
# Sprint.....: 3.8
# Arquivo....: builder/core/artifact.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Representa um artefato produzido pelo ProjectBuilder.
#
###############################################################################

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Artifact:
    """
    Representa um artefato gerado pelo Builder.

    Um Artifact pode representar:

        • Backup
        • Relatório
        • Arquivo exportado
        • Manifest
        • Log
        • Pacote
        • Template
        • Configuração

    Todo arquivo produzido pelo ProjectBuilder deverá ser
    representado por esta classe.
    """

    ###########################################################################
    # Informações
    ###########################################################################

    name: str

    path: Path

    artifact_type: str

    description: str = ""

    ###########################################################################
    # Utilidades
    ###########################################################################

    @property
    def exists(self) -> bool:

        return self.path.exists()

    ###########################################################################

    @property
    def filename(self) -> str:

        return self.path.name

    ###########################################################################

    @property
    def extension(self) -> str:

        return self.path.suffix

    ###########################################################################

    @property
    def directory(self) -> Path:

        return self.path.parent

    ###########################################################################

    @property
    def size(self) -> int:

        if not self.exists:

            return 0

        return self.path.stat().st_size

    ###########################################################################

    def delete(self) -> None:

        if self.exists:

            self.path.unlink()

    ###########################################################################

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"type='{self.artifact_type}', "
            f"path='{self.path}')"
        )


###############################################################################
# END FILE
###############################################################################