# report.py

###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.8
# Arquivo....: builder/discovery/report.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Geração dos relatórios do processo Discovery.
#
###############################################################################

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .summary import DiscoverySummary


class DiscoveryReport:
    """
    Geração de relatórios do Discovery.
    """

    ###########################################################################

    def __init__(

        self,

        summary: DiscoverySummary,

    ):

        self._summary = summary

    ###########################################################################

    @property
    def summary(self):

        return self._summary

    ###########################################################################

    def save_json(

        self,

        filename: Path,

    ):

        filename.write_text(

            json.dumps(

                self._summary.to_dict(),

                indent=4,

                ensure_ascii=False,

                default=str,

            ),

            encoding="utf-8",

        )

    ###########################################################################

    def save_markdown(

        self,

        filename: Path,

    ):

        lines = [

            "# Discovery Report",

            "",

            f"Gerado em: {datetime.now()}",

            "",

            "## Detectores",

            "",

        ]

        if hasattr(self._summary, "statistics"):

            for item in self._summary.statistics:

                lines.append(

                    f"- **{item.detector}**"

                    f" - {item.status}"

                    f" ({item.elapsed:.4f}s)"

                )

        filename.write_text(

            "\n".join(lines),

            encoding="utf-8",

        )

    ###########################################################################

    def save_html(

        self,

        filename: Path,

    ):

        html = [

            "<html>",

            "<head>",

            "<meta charset='utf-8'>",

            "<title>Discovery Report</title>",

            "</head>",

            "<body>",

            "<h1>Discovery Report</h1>",

            "<table border='1'>",

            "<tr>",

            "<th>Detector</th>",

            "<th>Status</th>",

            "<th>Tempo</th>",

            "</tr>",

        ]

        if hasattr(self._summary, "statistics"):

            for item in self._summary.statistics:

                html.extend(

                    [

                        "<tr>",

                        f"<td>{item.detector}</td>",

                        f"<td>{item.status}</td>",

                        f"<td>{item.elapsed:.4f}</td>",

                        "</tr>",

                    ]

                )

        html.extend(

            [

                "</table>",

                "</body>",

                "</html>",

            ]

        )

        filename.write_text(

            "\n".join(html),

            encoding="utf-8",

        )


###############################################################################
# END FILE
###############################################################################