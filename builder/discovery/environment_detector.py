###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.2
# Arquivo....: builder/discovery/environment_detector.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Descoberta do ambiente operacional.
#
###############################################################################

from __future__ import annotations

import getpass
import os
import platform
from pathlib import Path

from .base_detector import BaseDetector
from .summary import DiscoverySummary


class EnvironmentDetector(BaseDetector):
    """
    Descobre informações básicas do sistema operacional.
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

        return "Environment"

    ###########################################################################

    def discover(self) -> None:

        env = self._summary.environment

        env["platform"] = platform.system()

        env["platform_release"] = platform.release()

        env["platform_version"] = platform.version()

        env["architecture"] = platform.architecture()[0]

        env["machine"] = platform.machine()

        env["processor"] = platform.processor()

        env["hostname"] = platform.node()

        env["username"] = getpass.getuser()

        env["python_version"] = platform.python_version()

        env["cwd"] = str(Path.cwd())

        env["home"] = str(Path.home())

        env["temp"] = os.environ.get("TEMP", "")

        env["path"] = os.environ.get("PATH", "")

        env["onedrive"] = os.environ.get("OneDrive", "")

        env["appdata"] = os.environ.get("APPDATA", "")

        env["localappdata"] = os.environ.get("LOCALAPPDATA", "")

        env["programfiles"] = os.environ.get("ProgramFiles", "")

        env["programfiles_x86"] = os.environ.get(
            "ProgramFiles(x86)",
            "",
        )

        env["programdata"] = os.environ.get(
            "ProgramData",
            "",
        )

        env["systemroot"] = os.environ.get(
            "SystemRoot",
            "",
        )


###############################################################################
# END FILE
###############################################################################