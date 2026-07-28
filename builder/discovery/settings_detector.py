# settings_detector.py

###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.10
# Arquivo....: builder/discovery/settings_detector.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Descobre e cataloga todas as configurações do VS Code e VSCodium.
#
###############################################################################

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base_detector import BaseDetector
from .summary import DiscoverySummary


class SettingsDetector(BaseDetector):
    """
    Detector das configurações dos editores.
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

        return "Settings"

    ###########################################################################

    def discover(self) -> None:

        settings: list[dict[str, Any]] = []

        settings.extend(
            self._discover_editor(
                "VSCode",
                self._summary.vscode.get("user_data"),
            )
        )

        settings.extend(
            self._discover_editor(
                "VSCodium",
                self._summary.vscodium.get("user_data"),
            )
        )

        self._summary.settings = settings

    ###########################################################################

    def _discover_editor(
        self,
        editor: str,
        user_data: Path | None,
    ) -> list[dict[str, Any]]:

        result: list[dict[str, Any]] = []

        if user_data is None:

            return result

        user = user_data / "User"

        if not user.exists():

            return result

        files = [

            "settings.json",

            "keybindings.json",

            "tasks.json",

            "launch.json",

            "argv.json",

            "locale.json",

            "syncLocalSettings.json",

        ]

        for filename in files:

            file = user / filename

            result.append(

                {

                    "editor": editor,

                    "file": filename,

                    "path": file,

                    "exists": file.exists(),

                    "size": file.stat().st_size if file.exists() else 0,

                    "json": self._load_json(file),

                }

            )

        return result

    ###########################################################################

    def _load_json(
        self,
        file: Path,
    ) -> dict[str, Any]:

        if not file.exists():

            return {}

        try:

            return json.loads(

                file.read_text(

                    encoding="utf-8",

                )

            )

        except Exception:

            return {}


###############################################################################
# END FILE
###############################################################################