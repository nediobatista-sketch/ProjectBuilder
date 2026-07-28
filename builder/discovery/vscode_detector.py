# vscode_detector.py

###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.6
# Arquivo....: builder/discovery/vscode_detector.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Descobre instalações e configurações do Visual Studio Code.
#
###############################################################################

from __future__ import annotations

import os
from pathlib import Path

from .base_detector import BaseDetector
from .summary import DiscoverySummary


class VSCodeDetector(BaseDetector):
    """
    Detector do Visual Studio Code.
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

        return "VSCode"

    ###########################################################################

    def discover(self) -> None:

        vscode = self._summary.vscode

        vscode["installation"] = self._installation()

        vscode["user_data"] = self._user_data()

        vscode["extensions"] = self._extensions()

        vscode["profiles"] = self._profiles()

        vscode["settings"] = self._settings()

        vscode["snippets"] = self._snippets()

        vscode["workspace_storage"] = self._workspace_storage()

        vscode["logs"] = self._logs()

    ###########################################################################

    def _installation(self):

        candidates = [

            Path(os.environ.get("ProgramFiles", ""))
            / "Microsoft VS Code",

            Path(os.environ.get("ProgramFiles(x86)", ""))
            / "Microsoft VS Code",

            Path(os.environ.get("LOCALAPPDATA", ""))
            / "Programs"
            / "Microsoft VS Code",

        ]

        for path in candidates:

            if path.exists():

                return path

        return None

    ###########################################################################

    def _user_data(self):

        path = (
            Path(os.environ.get("APPDATA", ""))
            / "Code"
        )

        if path.exists():

            return path

        return None

    ###########################################################################

    def _extensions(self):

        path = (
            Path(os.environ.get("USERPROFILE", ""))
            / ".vscode"
            / "extensions"
        )

        if path.exists():

            return path

        return None

    ###########################################################################

    def _profiles(self):

        path = (
            Path(os.environ.get("APPDATA", ""))
            / "Code"
            / "User"
            / "profiles"
        )

        if path.exists():

            return path

        return None

    ###########################################################################

    def _settings(self):

        path = (
            Path(os.environ.get("APPDATA", ""))
            / "Code"
            / "User"
            / "settings.json"
        )

        if path.exists():

            return path

        return None

    ###########################################################################

    def _snippets(self):

        path = (
            Path(os.environ.get("APPDATA", ""))
            / "Code"
            / "User"
            / "snippets"
        )

        if path.exists():

            return path

        return None

    ###########################################################################

    def _workspace_storage(self):

        path = (
            Path(os.environ.get("APPDATA", ""))
            / "Code"
            / "User"
            / "workspaceStorage"
        )

        if path.exists():

            return path

        return None

    ###########################################################################

    def _logs(self):

        path = (
            Path(os.environ.get("APPDATA", ""))
            / "Code"
            / "logs"
        )

        if path.exists():

            return path

        return None


###############################################################################
# END FILE
###############################################################################