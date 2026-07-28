###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.5
# Arquivo....: builder/runtime/plugin_context.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Contexto compartilhado entre o Runtime e os Plugins.
#
###############################################################################

from __future__ import annotations

from dataclasses import dataclass

from .configuration import RuntimeConfiguration
from .container import ServiceContainer
from .event_bus import EventBus
from .paths import RuntimePaths


@dataclass(slots=True)
class PluginContext:
    """
    Contexto disponibilizado para todos os plugins.

    O objetivo desta classe é impedir que um plugin dependa
    diretamente do Runtime.

    Toda comunicação entre Runtime e Plugins deverá ocorrer
    através deste contexto.
    """

    ###########################################################################
    # Serviços disponíveis
    ###########################################################################

    container: ServiceContainer

    configuration: RuntimeConfiguration

    event_bus: EventBus

    paths: RuntimePaths

    ###########################################################################

    def publish(
        self,
        event: str,
        *args,
        **kwargs,
    ) -> None:
        """
        Publica um evento no EventBus.
        """

        self.event_bus.publish(
            event,
            *args,
            **kwargs,
        )

    ###########################################################################

    def resolve(self, service: type):
        """
        Resolve um serviço registrado no Container.
        """

        return self.container.resolve(service)


###############################################################################
# END FILE
###############################################################################