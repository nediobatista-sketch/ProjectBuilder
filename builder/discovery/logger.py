# logger.py

###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.7
# Arquivo....: builder/discovery/logger.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Logger do processo de Discovery.
#
###############################################################################

from __future__ import annotations

from datetime import datetime
from pathlib import Path


class DiscoveryLogger:
    """
    Logger do Discovery.
    """

    ###########################################################################

    def __init__(

        self,

        logfile: Path | None = None,

    ):

        self._logfile = logfile

        self._enabled = logfile is not None

    ###########################################################################

    @property
    def enabled(self):

        return self._enabled

    ###########################################################################

    def info(

        self,

        message: str,

    ):

        self._write(

            "INFO",

            message,

        )

    ###########################################################################

    def warning(

        self,

        message: str,

    ):

        self._write(

            "WARNING",

            message,

        )

    ###########################################################################

    def error(

        self,

        message: str,

    ):

        self._write(

            "ERROR",

            message,

        )

    ###########################################################################

    def detector_started(

        self,

        detector,

    ):

        self.info(

            f"Detector iniciado: {detector.name}"

        )

    ###########################################################################

    def detector_finished(

        self,

        detector,

    ):

        self.info(

            f"Detector finalizado: {detector.name}"

        )

    ###########################################################################

    def detector_failed(

        self,

        detector,

        exception,

    ):

        self.error(

            f"{detector.name}: {exception}"

        )

    ###########################################################################

    def _write(

        self,

        level: str,

        message: str,

    ):

        timestamp = datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        )

        line = (

            f"[{timestamp}] "

            f"[{level}] "

            f"{message}"

        )

        print(line)

        if self._enabled:

            with self._logfile.open(

                "a",

                encoding="utf-8",

            ) as fp:

                fp.write(

                    line + "\n"

                )


###############################################################################
# END FILE
###############################################################################