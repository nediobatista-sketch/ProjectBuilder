###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.1
# Arquivo....: builder/discovery/base_detector.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Classe base de todos os detectores.
#
###############################################################################

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseDetector(ABC):
    """
    Classe base para todos os detectores.
    """

    ###########################################################################

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Nome do detector.
        """

    ###########################################################################

    @abstractmethod
    def discover(self):
        """
        Executa a descoberta.
        """

    ###########################################################################

    def __repr__(self):

        return f"{self.__class__.__name__}()"


###############################################################################
# END FILE
###############################################################################