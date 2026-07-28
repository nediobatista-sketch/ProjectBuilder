###############################################################################
# ProjectBuilder
#
# EPIC.......: 007
# Sprint.....: 7.6
# Arquivo....: builder/reports/log_report.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Gerador de relatórios em formato de Log.
#
###############################################################################
from __future__ import annotations
import logging
from pathlib import Path
from .models import ReportData
class LogReportGenerator:
    """Geração de relatórios em formato de Log."""
    def __init__(
        self,
        log_level: int = logging.INFO,
    ) -> None:
        self._log_level = log_level
    def generate(
        self,
        data: ReportData,
        output: Path,
    ) -> None:
        output.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "=" * 70,
            f"  {data.title}",
            "=" * 70,
            f"  Tipo       : {data.report_type}",
            f"  Gerado em  : {data.generated_at}",
            "=" * 70,
            "",
        ]
        for name, section_data in data.sections.items():
            lines.append(f"[{name.upper()}]")
            if isinstance(section_data, dict):
                for key, value in section_data.items():
                    val_str = str(value)
                    if len(val_str) > 200:
                        val_str = val_str[:200] + "..."
                    lines.append(f"  {key:30s} : {val_str}")
            elif isinstance(section_data, list):
                for i, item in enumerate(section_data, 1):
                    if isinstance(item, dict):
                        for k, v in item.items():
                            lines.append(f"  [{i}] {k:25s} : {str(v)[:200]}")
                    else:
                        lines.append(f"  [{i}] {str(item)[:200]}")
            else:
                lines.append(f"  {str(section_data)[:500]}")
            lines.append("")
        lines.append("=" * 70)
        lines.append("  END OF REPORT")
        lines.append("=" * 70)
        output.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )
###############################################################################
# END FILE
###############################################################################
