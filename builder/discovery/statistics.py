# statistics.py

###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.4
# Arquivo....: builder/discovery/statistics.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Estatísticas da execução do Discovery.
#
###############################################################################

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DetectorStatistic:

    detector: str

    elapsed: float

    status: str

    message: str = ""


class DiscoveryStatistics:
    """
    Armazena estatísticas da execução do Discovery.
    """

    ###########################################################################

    def __init__(self):

        self._items: list[DetectorStatistic] = []

    ###########################################################################

    def add(

        self,

        detector: str,

        elapsed: float,

        status: str,

        message: str = "",

    ) -> None:

        self._items.append(

            DetectorStatistic(

                detector=detector,

                elapsed=elapsed,

                status=status,

                message=message,

            )

        )

    ###########################################################################

    def clear(self):

        self._items.clear()

    ###########################################################################

    @property
    def items(self):

        return tuple(self._items)

    ###########################################################################

    @property
    def total(self):

        return len(self._items)

    ###########################################################################

    @property
    def success(self):

        return sum(

            item.status == "OK"

            for item in self._items

        )

    ###########################################################################

    @property
    def failed(self):

        return sum(

            item.status != "OK"

            for item in self._items

        )


###############################################################################
# END FILE
###############################################################################