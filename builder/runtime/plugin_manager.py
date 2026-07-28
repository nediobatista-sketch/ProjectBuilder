###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.5
# Arquivo....: builder/runtime/plugin_manager.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Gerenciador de Plugins do Runtime.
#
###############################################################################

from __future__ import annotations

from typing import Iterator

from .plugin import RuntimePlugin


class PluginManager:
    """
    Gerencia todos os plugins carregados.

    Responsabilidades:

        • registrar plugins
        • remover plugins
        • localizar plugins
        • iniciar plugins
        • parar plugins
    """

    ###########################################################################

    def __init__(self) -> None:

        self._plugins: dict[str, RuntimePlugin] = {}

    ###########################################################################
    # Registro
    ###########################################################################

    def register(
        self,
        plugin: RuntimePlugin,
    ) -> None:

        self._plugins[plugin.name] = plugin

    ###########################################################################

    def unregister(
        self,
        name: str,
    ) -> None:

        self._plugins.pop(name, None)

    ###########################################################################

    def clear(self) -> None:

        self._plugins.clear()

    ###########################################################################
    # Consulta
    ###########################################################################

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._plugins

    ###########################################################################

    def get(
        self,
        name: str,
    ) -> RuntimePlugin | None:

        return self._plugins.get(name)

    ###########################################################################

    @property
    def plugins(self) -> tuple[RuntimePlugin, ...]:

        return tuple(self._plugins.values())

    ###########################################################################
    # Ciclo de vida
    ###########################################################################

    def configure(self) -> None:

        for plugin in self._plugins.values():

            plugin.configure()

    ###########################################################################

    def initialize(self) -> None:

        for plugin in self._plugins.values():

            plugin.initialize()

    ###########################################################################

    def start(self) -> None:

        for plugin in self._plugins.values():

            plugin.start()

    ###########################################################################

    def stop(self) -> None:

        #
        # Ordem inversa.
        #
        for plugin in reversed(tuple(self._plugins.values())):

            plugin.stop()

    ###########################################################################
    # Utilidades
    ###########################################################################

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return name in self._plugins

    ###########################################################################

    def __len__(self) -> int:

        return len(self._plugins)

    ###########################################################################

    def __iter__(self) -> Iterator[RuntimePlugin]:

        return iter(self._plugins.values())


###############################################################################
# END FILE
###############################################################################