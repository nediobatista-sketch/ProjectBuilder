###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.3
# Arquivo....: builder/runtime/service.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Define a interface base para serviços do ProjectBuilder.
#
# DEPENDÊNCIAS
#   Nenhuma.
#
###############################################################################

from __future__ import annotations

from abc import ABC


class Service(ABC):
    """
    Classe base para todos os serviços do ProjectBuilder.

    Os serviços podem sobrescrever os métodos do ciclo de vida
    conforme necessário.

    Exemplo:

        class Logger(Service):

            def initialize(self):
                ...

            def shutdown(self):
                ...
    """

    ###########################################################################

    def initialize(self) -> None:
        """
        Executado quando o Runtime inicializa o serviço.

        A implementação padrão não realiza nenhuma ação.
        """
        return

    ###########################################################################

    def shutdown(self) -> None:
        """
        Executado quando o Runtime é encerrado.

        A implementação padrão não realiza nenhuma ação.
        """
        return

    ###########################################################################

    @property
    def name(self) -> str:
        """
        Nome amigável do serviço.
        """

        return self.__class__.__name__

    ###########################################################################

    @property
    def qualified_name(self) -> str:
        """
        Nome totalmente qualificado da classe.
        """

        return f"{self.__class__.__module__}.{self.__class__.__qualname__}"

    ###########################################################################

    def __repr__(self) -> str:

        return f"<{self.qualified_name}>"

###############################################################################
# END FILE
###############################################################################