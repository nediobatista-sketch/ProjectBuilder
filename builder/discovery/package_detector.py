# package_detector.py

###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.12
# Arquivo....: builder/discovery/package_detector.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Descobre ferramentas de desenvolvimento instaladas no sistema.
#
###############################################################################

from __future__ import annotations

import shutil
from pathlib import Path

from .base_detector import BaseDetector
from .summary import DiscoverySummary


class PackageDetector(BaseDetector):
    """
    Detector de ferramentas instaladas.
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

        return "Package"

    ###########################################################################

    def discover(self) -> None:

        packages = {}

        packages["git"] = self._find("git")

        packages["git-lfs"] = self._find("git-lfs")

        packages["node"] = self._find("node")

        packages["npm"] = self._find("npm")

        packages["pnpm"] = self._find("pnpm")

        packages["yarn"] = self._find("yarn")

        packages["bun"] = self._find("bun")

        packages["java"] = self._find("java")

        packages["javac"] = self._find("javac")

        packages["maven"] = self._find("mvn")

        packages["gradle"] = self._find("gradle")

        packages["go"] = self._find("go")

        packages["cargo"] = self._find("cargo")

        packages["rustc"] = self._find("rustc")

        packages["docker"] = self._find("docker")

        packages["docker-compose"] = self._find("docker-compose")

        packages["kubectl"] = self._find("kubectl")

        packages["helm"] = self._find("helm")

        packages["terraform"] = self._find("terraform")

        packages["winget"] = self._find("winget")

        packages["choco"] = self._find("choco")

        packages["scoop"] = self._find("scoop")

        packages["powershell"] = self._find("pwsh")

        packages["python"] = self._find("python")

        packages["python3"] = self._find("python3")

        packages["pip"] = self._find("pip")

        packages["pip3"] = self._find("pip3")

        packages["conda"] = self._find("conda")

        packages["poetry"] = self._find("poetry")

        packages["uv"] = self._find("uv")

        packages["virtualenv"] = self._find("virtualenv")

        self._summary.packages = packages

    ###########################################################################

    def _find(
        self,
        executable: str,
    ) -> dict:

        executable_path = shutil.which(executable)

        return {

            "installed": executable_path is not None,

            "path": Path(executable_path) if executable_path else None,

        }


###############################################################################
# END FILE
###############################################################################