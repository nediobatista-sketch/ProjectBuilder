###############################################################################
# ProjectBuilder
#
# EPIC.......: 007
# Sprint.....: 7.3
# Arquivo....: builder/reports/json_report.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Gerador de relatórios em JSON.
#
###############################################################################
from __future__ import annotations
import json
from pathlib import Path
from .models import ReportData
class JsonReportGenerator:
    """Geração de relatórios em JSON."""
    def generate(
        self,
        data: ReportData,
        output: Path,
    ) -> None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(
                data.to_dict(),
                indent=4,
                ensure_ascii=False,
                default=str,
            ),
            encoding="utf-8",
        )
###############################################################################
# END FILE
###############################################################################
