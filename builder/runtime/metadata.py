###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.3.1
# Arquivo....: builder/runtime/metadata.py
# Versão.....: 2.0
#
# DESCRIÇÃO
#   Metadados do Runtime.
#
###############################################################################

from __future__ import annotations

from dataclasses import dataclass
import platform


@dataclass(slots=True, frozen=True)
class RuntimeMetadata:
    """
    Metadados do Runtime.

    Todos os campos obrigatórios vêm antes dos opcionais,
    evitando erros de dataclass.
    """

    ###########################################################################
    # Campos obrigatórios
    ###########################################################################

    architecture: str

    ###########################################################################
    # Campos opcionais
    ###########################################################################

    application: str = "ProjectBuilder"

    version: str = "0.1.0-dev"

    python_version: str = platform.python_version()

    operating_system: str = platform.system()

    operating_system_version: str = platform.version()

    machine: str = platform.machine()

    processor: str = platform.processor()

    ###########################################################################

    @classmethod
    def current(cls) -> "RuntimeMetadata":
        """
        Cria os metadados do ambiente atual.
        """

        return cls(
            architecture=platform.architecture()[0],
        )

###############################################################################
# END FILE
###############################################################################