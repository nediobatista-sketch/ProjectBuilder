###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.5
# Arquivo....: builder/runtime/configuration.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Gerenciamento das configurações do Runtime.
#
###############################################################################

from __future__ import annotations

from pathlib import Path
from typing import Any


class RuntimeConfiguration:
    """
    Armazena todas as configurações do Runtime.

    Nesta primeira versão funciona como um pequeno repositório
    chave/valor.

    Nas próximas Sprints passará a carregar:

        • JSON
        • TOML
        • YAML
        • Variáveis de ambiente
        • Configurações do usuário
        • Configurações do projeto
    """

    ###########################################################################

    def __init__(self) -> None:

        self._values: dict[str, Any] = {}

    ###########################################################################

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self._values[key] = value

    ###########################################################################

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self._values.get(key, default)

    ###########################################################################

    def remove(
        self,
        key: str,
    ) -> None:

        self._values.pop(key, None)

    ###########################################################################

    def clear(self) -> None:

        self._values.clear()

    ###########################################################################

    def load(self, filename: Path) -> None:
        """
        Placeholder.

        Implementaremos o carregamento de arquivos
        em uma Sprint posterior.
        """

        raise NotImplementedError(
            "Carregamento de configuração ainda não implementado."
        )

    ###########################################################################

    def save(self, filename: Path) -> None:
        """
        Placeholder.

        Implementaremos a gravação posteriormente.
        """

        raise NotImplementedError(
            "Gravação de configuração ainda não implementada."
        )

    ###########################################################################

    @property
    def values(self) -> dict[str, Any]:

        return dict(self._values)

    ###########################################################################

    def __contains__(
        self,
        key: str,
    ) -> bool:

        return key in self._values

    ###########################################################################

    def __len__(self) -> int:

        return len(self._values)

    ###########################################################################

    def __iter__(self):

        return iter(self._values.items())


###############################################################################
# END FILE
###############################################################################