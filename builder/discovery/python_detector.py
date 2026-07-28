###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.5
# Arquivo....: builder/discovery/python_detector.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Descobre instalações e ambientes Python.
#
###############################################################################

from __future__ import annotations

import shutil
from pathlib import Path

from .base_detector import BaseDetector
from .summary import DiscoverySummary


class PythonDetector(BaseDetector):
    """
    Detector do ambiente Python.
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

        return "Python"

    ###########################################################################

    def discover(self) -> None:

        python = self._summary.python

        python["python"] = shutil.which("python")

        python["python3"] = shutil.which("python3")

        python["py"] = shutil.which("py")

        python["pip"] = shutil.which("pip")

        python["pip3"] = shutil.which("pip3")

        python["conda"] = shutil.which("conda")

        python["poetry"] = shutil.which("poetry")

        python["uv"] = shutil.which("uv")

        python["virtualenv"] = shutil.which("virtualenv")

        python["venvs"] = self._find_virtual_environments()

        python["projects"] = self._find_python_projects()

    ###########################################################################

    def _find_virtual_environments(self):

        result = []

        root = Path.cwd()

        names = {

            ".venv",

            "venv",

            "env",

        }

        for directory in root.rglob("*"):

            if not directory.is_dir():

                continue

            if directory.name not in names:

                continue

            activate = directory / "Scripts" / "activate.bat"

            if activate.exists():

                result.append(directory)

        return sorted(result)

    ###########################################################################

    def _find_python_projects(self):

        result = []

        root = Path.cwd()

        files = (

            "pyproject.toml",

            "requirements.txt",

            "requirements-dev.txt",

            "poetry.lock",

            "uv.lock",

            "setup.py",

            "setup.cfg",

        )

        for filename in files:

            for file in root.rglob(filename):

                result.append(file.parent)

        unique = []

        visited = set()

        for path in result:

            if path in visited:

                continue

            visited.add(path)

            unique.append(path)

        return sorted(unique)


###############################################################################
# END FILE
###############################################################################