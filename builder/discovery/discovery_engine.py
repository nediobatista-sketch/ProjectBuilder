###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.2
# Arquivo....: builder/discovery/discovery_engine.py
# Versão.....: 1.1
#
# DESCRIÇÃO
#   Engine principal do Discovery.
#
###############################################################################

from __future__ import annotations

from .summary import DiscoverySummary


class DiscoveryEngine:
    """
    Coordenador do processo de Discovery.
    """

    ###########################################################################

    def __init__(self):

        self._summary = DiscoverySummary()

        self._detectors = []

    ###########################################################################

    @property
    def summary(self):

        return self._summary

    ###########################################################################

    def register(self, detector):

        self._detectors.append(detector)

    ###########################################################################

    def run(self):

        for detector in self._detectors:

            detector.discover()

        return self._summary

    ###########################################################################

    def clear(self):

        self._detectors.clear()

    ###########################################################################

    @property
    def detector_count(self):

        return len(self._detectors)

    ###########################################################################

    @property
    def detectors(self):

        return tuple(self._detectors)


###############################################################################
# END FILE
###############################################################################