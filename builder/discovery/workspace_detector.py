# workspace_detector.py

###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.11
# Arquivo....: builder/discovery/workspace_detector.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Descobre Workspaces, arquivos .code-workspace e áreas de armazenamento
#   utilizadas pelo VS Code e VSCodium.
#
###############################################################################

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base_detector import BaseDetector
from .summary import DiscoverySummary


class WorkspaceDetector(BaseDetector):
    """
    Detector de Workspaces.
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

        return "Workspace"

    ###########################################################################

    def discover(self) -> None:

        workspaces = []

        workspaces.extend(

            self._discover_editor(

                "VSCode",

                self._summary.vscode.get("user_data"),

            )

        )

        workspaces.extend(

            self._discover_editor(

                "VSCodium",

                self._summary.vscodium.get("user_data"),

            )

        )

        self._summary.workspaces = workspaces

    ###########################################################################

    def _discover_editor(

        self,

        editor: str,

        user_data: Path | None,

    ) -> list[dict[str, Any]]:

        result = []

        if user_data is None:

            return result

        workspace_storage = user_data / "User" / "workspaceStorage"

        global_storage = user_data / "User" / "globalStorage"

        workspace_files = list(

            Path.cwd().rglob("*.code-workspace")

        )

        result.append(

            {

                "editor": editor,

                "workspace_storage": workspace_storage,

                "workspace_storage_exists": workspace_storage.exists(),

                "global_storage": global_storage,

                "global_storage_exists": global_storage.exists(),

                "workspace_count": len(workspace_files),

                "workspace_files": workspace_files,

            }

        )

        return result

    ###########################################################################

    def load_workspace(

        self,

        workspace: Path,

    ) -> dict[str, Any]:

        if not workspace.exists():

            return {}

        try:

            return json.loads(

                workspace.read_text(

                    encoding="utf-8",

                )

            )

        except Exception:

            return {}


###############################################################################
# END FILE
###############################################################################