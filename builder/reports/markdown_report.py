###############################################################################
# ProjectBuilder
#
# EPIC.......: 007
# Sprint.....: 7.4
# Arquivo....: builder/reports/markdown_report.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Gerador de relatórios em Markdown.
#
###############################################################################
from __future__ import annotations
from pathlib import Path
from .models import ReportData
class MarkdownReportGenerator:
    """Geração de relatórios em Markdown."""
    def generate(
        self,
        data: ReportData,
        output: Path,
    ) -> None:
        lines = [
            f"# {data.title}",
            "",
            f"**Gerado em:** {data.generated_at}",
            f"**Tipo:** {data.report_type}",
            "",
            "---",
            "",
        ]
        for name, section_data in data.sections.items():
            lines.append(f"## {name}")
            lines.append("")
            if isinstance(section_data, dict):
                lines.extend(self._format_dict(section_data))
            elif isinstance(section_data, list):
                lines.extend(self._format_list(section_data))
            else:
                lines.append(f"```")
                lines.append(str(section_data))
                lines.append(f"```")
            lines.append("")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )
    def _format_dict(self, data: dict) -> list[str]:
        lines = []
        if not data:
            lines.append("*Sem dados*")
            return lines
        lines.append("| Propriedade | Valor |")
        lines.append("|---|---|")
        for key, value in data.items():
            val_str = str(value)
            if len(val_str) > 100:
                val_str = val_str[:100] + "..."
            lines.append(f"| {key} | {val_str} |")
        return lines
    def _format_list(self, data: list) -> list[str]:
        lines = []
        if not data:
            lines.append("*Sem dados*")
            return lines
        if data and isinstance(data[0], dict):
            keys = list(data[0].keys())
            lines.append("| " + " | ".join(keys) + " |")
            lines.append("| " + " | ".join(["---"] * len(keys)) + " |")
            for row in data:
                vals = [str(row.get(k, ""))[:50] for k in keys]
                lines.append("| " + " | ".join(vals) + " |")
        else:
            for item in data:
                lines.append(f"- {item}")
        return lines
###############################################################################
# END FILE
###############################################################################
