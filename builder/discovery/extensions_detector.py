# extensions_detector.py

###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.8
# Arquivo....: builder/discovery/extensions_detector.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Descobre extensões instaladas no VS Code e VSCodium.
#
###############################################################################

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base_detector import BaseDetector
from .summary import DiscoverySummary


class ExtensionsDetector(BaseDetector):
    """
    Detector de extensões.
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

        return "Extensions"

    ###########################################################################

    def discover(self) -> None:

        extensions = []

        extensions.extend(
            self._scan_directory(
                self._summary.vscode.get("extensions")
            )
        )

        extensions.extend(
            self._scan_directory(
                self._summary.vscodium.get("extensions")
            )
        )

        self._summary.extensions = extensions

    ###########################################################################

    def _scan_directory(
        self,
        directory: Path | None,
    ) -> list[dict[str, Any]]:

        result: list[dict[str, Any]] = []

        if directory is None:

            return result

        if not directory.exists():

            return result

        for extension in sorted(directory.iterdir()):

            if not extension.is_dir():

                continue

            info = self._read_extension(extension)

            if info:

                result.append(info)

        return result

    ###########################################################################

    def _read_extension(
        self,
        directory: Path,
    ) -> dict[str, Any]:

        package = directory / "package.json"

        manifest = {}

        if package.exists():

            try:

                manifest = json.loads(
                    package.read_text(
                        encoding="utf-8",
                    )
                )

            except Exception:

                manifest = {}

        return {

            "name": manifest.get("name"),

            "display_name": manifest.get("displayName"),

            "publisher": manifest.get("publisher"),

            "version": manifest.get("version"),

            "description": manifest.get("description"),

            "engines": manifest.get("engines"),

            "categories": manifest.get("categories", []),

            "keywords": manifest.get("keywords", []),

            "activation_events": manifest.get(
                "activationEvents",
                [],
            ),

            "extension_dependencies": manifest.get(
                "extensionDependencies",
                [],
            ),

            "extension_pack": manifest.get(
                "extensionPack",
                [],
            ),

            "repository": manifest.get(
                "repository",
            ),

            "bugs": manifest.get(
                "bugs",
            ),

            "homepage": manifest.get(
                "homepage",
            ),

            "license": manifest.get(
                "license",
            ),

            "preview": manifest.get(
                "preview",
                False,
            ),

            "path": directory,

            "package_json": package,

        }


###############################################################################
# END FILE
###############################################################################