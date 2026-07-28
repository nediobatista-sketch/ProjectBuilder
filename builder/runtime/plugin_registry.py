###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.5
# Arquivo....: builder/runtime/plugin_registry.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Registro de Plugins do Runtime.
#
###############################################################################

from __future__ import annotations

from .plugin import RuntimePlugin


class PluginRegistry:
    """
    Registro central de plugins.

    O Registry apenas mantém o catálogo dos plugins
    conhecidos pelo Runtime.

    Não executa plugins.
    Não descobre plugins.
    Não controla ciclo de vida.
    """

    ###########################################################################

    def __init__(self) -> None:

        self._plugins: dict[str, RuntimePlugin] = {}

    ###########################################################################

    def register(
        self,
        plugin: RuntimePlugin,
    ) -> None:
        """
        Registra um plugin.
        """

        self._plugins[plugin.name] = plugin

    ###########################################################################

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove um plugin.
        """

        self._plugins.pop(name, None)

    ###########################################################################

    def clear(self) -> None:
        """
        Remove todos os plugins.
        """

        self._plugins.clear()

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

    @property
    def names(self) -> tuple[str, ...]:

        return tuple(sorted(self._plugins.keys()))

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

    def __iter__(self):

        return iter(self._plugins.values())


###############################################################################
# END FILE
###############################################################################