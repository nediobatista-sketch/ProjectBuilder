###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.3
# Arquivo....: builder/discovery/filesystem_detector.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Descoberta da estrutura de diretórios do sistema.
#
###############################################################################

from __future__ import annotations

import os
from pathlib import Path

from .base_detector import BaseDetector
from .summary import DiscoverySummary


class FilesystemDetector(BaseDetector):
    """
    Descobre os principais diretórios utilizados
    pelo ProjectBuilder.
    """

    ###########################################################################

    def __init__(
        self,
        summary: DiscoverySummary,
    ) -> None:

        self._summary = summary

    ###########################################################################

    @property
    def name(self) -> str:

        return "Filesystem"

    ###########################################################################

    def discover(self) -> None:

        fs = self._summary.filesystem

        home = Path.home()

        fs["home"] = home

        fs["desktop"] = home / "Desktop"

        fs["documents"] = home / "Documents"

        fs["downloads"] = home / "Downloads"

        fs["pictures"] = home / "Pictures"

        fs["music"] = home / "Music"

        fs["videos"] = home / "Videos"

        fs["appdata"] = Path(
            os.environ.get("APPDATA", "")
        )

        fs["localappdata"] = Path(
            os.environ.get("LOCALAPPDATA", "")
        )

        fs["programfiles"] = Path(
            os.environ.get("ProgramFiles", "")
        )

        fs["programfiles_x86"] = Path(
            os.environ.get("ProgramFiles(x86)", "")
        )

        fs["programdata"] = Path(
            os.environ.get("ProgramData", "")
        )

        fs["systemroot"] = Path(
            os.environ.get("SystemRoot", "")
        )

        fs["temp"] = Path(
            os.environ.get("TEMP", "")
        )

        fs["cwd"] = Path.cwd()


###############################################################################
# END FILE
###############################################################################