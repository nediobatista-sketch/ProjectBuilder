###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.4
# Arquivo....: builder/discovery/registry_detector.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Descobre informações armazenadas no Registro do Windows.
#
###############################################################################

from __future__ import annotations

import winreg
from typing import Any

from .base_detector import BaseDetector
from .summary import DiscoverySummary


class RegistryDetector(BaseDetector):
    """
    Detector do Registro do Windows.
    """

    ###########################################################################

    def __init__(self, summary: DiscoverySummary):

        self._summary = summary

    ###########################################################################

    @property
    def name(self) -> str:

        return "Registry"

    ###########################################################################

    def discover(self) -> None:

        registry = self._summary.registry

        registry["vscode"] = self._find_vscode()

        registry["vscodium"] = self._find_vscodium()

        registry["python"] = self._find_python()

        registry["git"] = self._find_git()

    ###########################################################################

    def _find_vscode(self) -> dict[str, Any]:

        return self._read_uninstall_key("Microsoft VS Code")

    ###########################################################################

    def _find_vscodium(self) -> dict[str, Any]:

        return self._read_uninstall_key("VSCodium")

    ###########################################################################

    def _find_python(self) -> dict[str, Any]:

        return self._read_uninstall_key("Python")

    ###########################################################################

    def _find_git(self) -> dict[str, Any]:

        return self._read_uninstall_key("Git")

    ###########################################################################

    def _read_uninstall_key(
        self,
        product: str,
    ) -> dict[str, Any]:

        roots = [

            (
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            ),

            (
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            ),

            (
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
            ),

        ]

        for hive, path in roots:

            try:

                key = winreg.OpenKey(hive, path)

            except OSError:

                continue

            try:

                total = winreg.QueryInfoKey(key)[0]

                for index in range(total):

                    sub = winreg.EnumKey(key, index)

                    try:

                        app = winreg.OpenKey(key, sub)

                        name = winreg.QueryValueEx(
                            app,
                            "DisplayName",
                        )[0]

                        if product.lower() not in name.lower():

                            continue

                        result = {

                            "display_name": name,

                        }

                        for field in (

                            "DisplayVersion",

                            "InstallLocation",

                            "Publisher",

                            "InstallDate",

                            "DisplayIcon",

                        ):

                            try:

                                result[field.lower()] = winreg.QueryValueEx(
                                    app,
                                    field,
                                )[0]

                            except OSError:

                                pass

                        return result

                    except OSError:

                        continue

            finally:

                winreg.CloseKey(key)

        return {}

###############################################################################
# END FILE
###############################################################################