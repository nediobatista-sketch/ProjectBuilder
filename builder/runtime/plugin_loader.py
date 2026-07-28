###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.5
# Arquivo....: builder/runtime/plugin_loader.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Descoberta e carregamento de Plugins.
#
###############################################################################

from __future__ import annotations

import importlib
import inspect
import pkgutil

from .plugin import RuntimePlugin


class PluginLoader:
    """
    Responsável por descobrir e carregar plugins.

    O Loader NÃO gerencia plugins.

    Sua única responsabilidade é localizar módulos Python,
    instanciar classes derivadas de RuntimePlugin e retorná-las
    para o PluginManager.
    """

    ###########################################################################

    def __init__(self) -> None:

        self._packages: list[str] = []

    ###########################################################################

    def add_package(
        self,
        package: str,
    ) -> None:
        """
        Adiciona um pacote para descoberta.
        """

        if package not in self._packages:

            self._packages.append(package)

    ###########################################################################

    @property
    def packages(self) -> tuple[str, ...]:

        return tuple(self._packages)

    ###########################################################################

    def discover(self) -> list[RuntimePlugin]:
        """
        Descobre todos os plugins registrados.
        """

        plugins: list[RuntimePlugin] = []

        for package_name in self._packages:

            try:

                package = importlib.import_module(package_name)

            except Exception:

                continue

            if not hasattr(package, "__path__"):

                continue

            for _, module_name, _ in pkgutil.iter_modules(package.__path__):

                module = importlib.import_module(
                    f"{package_name}.{module_name}"
                )

                plugins.extend(
                    self._discover_module(module)
                )

        return plugins

    ###########################################################################

    def _discover_module(
        self,
        module,
    ) -> list[RuntimePlugin]:

        plugins: list[RuntimePlugin] = []

        for _, obj in inspect.getmembers(
            module,
            inspect.isclass,
        ):

            if obj is RuntimePlugin:

                continue

            if not issubclass(obj, RuntimePlugin):

                continue

            plugins.append(obj())

        return plugins


###############################################################################
# END FILE
###############################################################################