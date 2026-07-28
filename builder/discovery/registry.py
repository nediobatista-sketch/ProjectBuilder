# registry.py

###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.5
# Arquivo....: builder/discovery/registry.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Registro dos Detectores do Discovery.
#
###############################################################################

from __future__ import annotations

from typing import Iterator

from .base_detector import BaseDetector


class DiscoveryRegistry:
    """
    Registro dos Detectores.
    """

    ###########################################################################

    def __init__(self):

        self._detectors: list[BaseDetector] = []

    ###########################################################################

    def register(

        self,

        detector: BaseDetector,

    ) -> None:

        self._detectors.append(detector)

    ###########################################################################

    def unregister(

        self,

        detector: BaseDetector,

    ) -> None:

        if detector in self._detectors:

            self._detectors.remove(detector)

    ###########################################################################

    def clear(self):

        self._detectors.clear()

    ###########################################################################

    @property
    def detectors(self):

        return tuple(self._detectors)

    ###########################################################################

    @property
    def count(self):

        return len(self._detectors)

    ###########################################################################

    def __len__(self):

        return len(self._detectors)

    ###########################################################################

    def __iter__(self) -> Iterator[BaseDetector]:

        return iter(self._detectors)

    ###########################################################################

    def __contains__(

        self,

        detector: BaseDetector,

    ) -> bool:

        return detector in self._detectors


###############################################################################
# END FILE
###############################################################################