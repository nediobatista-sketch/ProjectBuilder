###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.3.1
# Arquivo....: builder/runtime/provider.py
# Versão.....: 2.0
#
# DESCRIÇÃO
#   Responsável pela criação das instâncias dos serviços registrados
#   no ServiceContainer.
#
###############################################################################

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, get_type_hints

from .descriptor import ServiceDescriptor

if TYPE_CHECKING:
    from .container import ServiceContainer


class ServiceProvider:
    """
    Responsável pela criação das instâncias dos serviços.

    Resolve automaticamente as dependências declaradas no
    construtor utilizando type hints.
    """

    ###########################################################################

    def __init__(self, container: "ServiceContainer") -> None:

        self._container = container

    ###########################################################################

    def create(self, descriptor: ServiceDescriptor) -> Any:
        """
        Cria uma instância do serviço.
        """

        #
        # Factory registrada
        #
        if descriptor.factory is not None:
            return descriptor.factory()

        implementation = descriptor.implementation

        constructor = implementation.__init__

        signature = inspect.signature(constructor)

        #
        # Resolve corretamente Forward References
        #
        type_hints = get_type_hints(constructor)

        kwargs: dict[str, Any] = {}

        #
        # Ignora "self"
        #
        parameters = list(signature.parameters.values())[1:]

        for parameter in parameters:

            #
            # Ignora *args
            #
            if parameter.kind is inspect.Parameter.VAR_POSITIONAL:
                continue

            #
            # Ignora **kwargs
            #
            if parameter.kind is inspect.Parameter.VAR_KEYWORD:
                continue

            #
            # Obtém o type hint já resolvido.
            #
            annotation = type_hints.get(parameter.name)

            #
            # Parâmetro obrigatório sem type hint.
            #
            if annotation is None:

                #
                # Possui valor default?
                #
                if parameter.default is not inspect.Parameter.empty:
                    continue

                raise TypeError(
                    f"{implementation.__name__}.__init__(): "
                    f"o parâmetro '{parameter.name}' "
                    f"não possui type hint."
                )

            #
            # Resolve dependência.
            #
            dependency = self._container.resolve(annotation)

            kwargs[parameter.name] = dependency

        return implementation(**kwargs)

###############################################################################
# END FILE
###############################################################################