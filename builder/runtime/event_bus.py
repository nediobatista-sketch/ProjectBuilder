###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.5
# Arquivo....: builder/runtime/event_bus.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Barramento de eventos do Runtime.
#
###############################################################################

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any


EventHandler = Callable[..., None]


class EventBus:
    """
    Barramento simples de eventos.

    Permite registrar ouvintes (listeners) para um evento
    e publicar eventos para todos os inscritos.

    Nas próximas versões suportará:

        • prioridades
        • eventos assíncronos
        • filtros
        • middleware
        • cancelamento
        • eventos distribuídos
    """

    ###########################################################################
    # Construtor
    ###########################################################################

    def __init__(self) -> None:

        self._listeners: dict[str, list[EventHandler]] = defaultdict(list)

    ###########################################################################
    # Registro
    ###########################################################################

    def subscribe(
        self,
        event: str,
        listener: EventHandler,
    ) -> None:

        if listener not in self._listeners[event]:

            self._listeners[event].append(listener)

    ###########################################################################
    # Remoção
    ###########################################################################

    def unsubscribe(
        self,
        event: str,
        listener: EventHandler,
    ) -> None:

        if event not in self._listeners:

            return

        if listener in self._listeners[event]:

            self._listeners[event].remove(listener)

            if not self._listeners[event]:

                del self._listeners[event]

    ###########################################################################
    # Publicação
    ###########################################################################

    def publish(
        self,
        event: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:

        listeners = tuple(self._listeners.get(event, ()))

        for listener in listeners:

            listener(*args, **kwargs)

    ###########################################################################
    # Consulta
    ###########################################################################

    def listeners(
        self,
        event: str,
    ) -> tuple[EventHandler, ...]:

        return tuple(self._listeners.get(event, ()))

    ###########################################################################
    # Limpeza
    ###########################################################################

    def clear(self) -> None:

        self._listeners.clear()

    ###########################################################################
    # Utilidades
    ###########################################################################

    def __contains__(
        self,
        event: str,
    ) -> bool:

        return event in self._listeners

    ###########################################################################

    def __len__(self) -> int:

        return len(self._listeners)


###############################################################################
# END FILE
###############################################################################