# vscodium_detector.py

###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.7
# Arquivo....: builder/discovery/vscodium_detector.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Descobre instalações e configurações do VSCodium.
#
###############################################################################

from __future__ import annotations

import os
from pathlib import Path

from .base_detector import BaseDetector
from .summary import DiscoverySummary


class VSCodiumDetector(BaseDetector):
    """
    Detector do VSCodium.
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

        return "VSCodium"

    ###########################################################################

    def discover(self) -> None:

        vscodium = self._summary.vscodium

        vscodium["installation"] = self._installation()

        vscodium["user_data"] = self._user_data()

        vscodium["extensions"] = self._extensions()

        vscodium["profiles"] = self._profiles()

        vscodium["settings"] = self._settings()

        vscodium["snippets"] = self._snippets()

        vscodium["workspace_storage"] = self._workspace_storage()

        vscodium["logs"] = self._logs()

    ###########################################################################

    def _installation(self):

        candidates = [

            Path(os.environ.get("ProgramFiles", ""))
            / "VSCodium",

            Path(os.environ.get("ProgramFiles(x86)", ""))
            / "VSCodium",

            Path(os.environ.get("LOCALAPPDATA", ""))
            / "Programs"
            / "VSCodium",

        ]

        for path in candidates:

            if path.exists():

                return path

        return None

    ###########################################################################

    def _user_data(self):

        path = (
            Path(os.environ.get("APPDATA", ""))
            / "VSCodium"
        )

        if path.exists():

            return path

        return None

    ###########################################################################

    def _extensions(self):

        path = (
            Path(os.environ.get("USERPROFILE", ""))
            / ".vscode-oss"
            / "extensions"
        )

        if path.exists():

            return path

        return None

    ###########################################################################

    def _profiles(self):

        path = (
            Path(os.environ.get("APPDATA", ""))
            / "VSCodium"
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
            / "VSCodium"
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
            / "VSCodium"
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
            / "VSCodium"
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
            / "VSCodium"
            / "logs"
        )

        if path.exists():

            return path

        return None


###############################################################################
# END FILE
###############################################################################