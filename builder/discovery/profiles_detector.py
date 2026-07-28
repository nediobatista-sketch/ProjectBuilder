# profiles_detector.py

###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.9
# Arquivo....: builder/discovery/profiles_detector.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Descobre todos os Profiles do VS Code e VSCodium.
#
###############################################################################

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base_detector import BaseDetector
from .summary import DiscoverySummary


class ProfilesDetector(BaseDetector):
    """
    Detector de Profiles.
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

        return "Profiles"

    ###########################################################################

    def discover(self) -> None:

        profiles: list[dict[str, Any]] = []

        profiles.extend(
            self._discover_profiles(
                self._summary.vscode.get("profiles"),
                "VSCode",
            )
        )

        profiles.extend(
            self._discover_profiles(
                self._summary.vscodium.get("profiles"),
                "VSCodium",
            )
        )

        self._summary.profiles = profiles

    ###########################################################################

    def _discover_profiles(
        self,
        root: Path | None,
        editor: str,
    ) -> list[dict[str, Any]]:

        result: list[dict[str, Any]] = []

        if root is None:

            return result

        if not root.exists():

            return result

        for profile in sorted(root.iterdir()):

            if not profile.is_dir():

                continue

            result.append(
                self._read_profile(
                    profile,
                    editor,
                )
            )

        return result

    ###########################################################################

    def _read_profile(
        self,
        directory: Path,
        editor: str,
    ) -> dict[str, Any]:

        settings = directory / "settings.json"

        keybindings = directory / "keybindings.json"

        tasks = directory / "tasks.json"

        launch = directory / "launch.json"

        snippets = directory / "snippets"

        extensions = directory / "extensions.json"

        profile_json = directory / "profile.json"

        metadata = {}

        if profile_json.exists():

            try:

                metadata = json.loads(
                    profile_json.read_text(
                        encoding="utf-8",
                    )
                )

            except Exception:

                metadata = {}

        return {

            "editor": editor,

            "uuid": directory.name,

            "name": metadata.get(
                "name",
                directory.name,
            ),

            "directory": directory,

            "profile_json": profile_json,

            "settings": settings,

            "keybindings": keybindings,

            "tasks": tasks,

            "launch": launch,

            "snippets": snippets,

            "extensions": extensions,

            "exists_settings": settings.exists(),

            "exists_keybindings": keybindings.exists(),

            "exists_tasks": tasks.exists(),

            "exists_launch": launch.exists(),

            "exists_snippets": snippets.exists(),

            "exists_extensions": extensions.exists(),

        }


###############################################################################
# END FILE
###############################################################################