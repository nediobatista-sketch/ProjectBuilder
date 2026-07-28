###############################################################################
# ProjectBuilder
#
# EPIC.......: 007
# Sprint.....: 7.2
# Arquivo....: builder/reports/html_report.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Gerador de relatórios em HTML.
#
###############################################################################
from __future__ import annotations
from pathlib import Path
from .models import ReportData
class HtmlReportGenerator:
    """Geração de relatórios em HTML."""
    def generate(
        self,
        data: ReportData,
        output: Path,
    ) -> None:
        html = [
            "<!DOCTYPE html>",
            "<html lang='pt-BR'>",
            "<head>",
            "<meta charset='utf-8'>",
            "<meta name='viewport' content='width=device-width, initial-scale=1'>",
            f"<title>{self._escape(data.title)}</title>",
            "<style>",
            self._css(),
            "</style>",
            "</head>",
            "<body>",
            "<div class='container'>",
            f"<h1>{self._escape(data.title)}</h1>",
            f"<p class='meta'>Gerado em: {data.generated_at}</p>",
            f"<p class='meta'>Tipo: {self._escape(data.report_type)}</p>",
        ]
        for name, section_data in data.sections.items():
            html.append(f"<h2>{self._escape(name)}</h2>")
            html.append("<div class='section'>")
            if isinstance(section_data, dict):
                html.append(self._dict_to_table(section_data))
            elif isinstance(section_data, list):
                html.append(self._list_to_table(section_data))
            else:
                html.append(f"<pre>{self._escape(str(section_data))}</pre>")
            html.append("</div>")
        html.extend([
            "</div>",
            "</body>",
            "</html>",
        ])
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            "\n".join(html), encoding="utf-8",
        )
    def _css(self) -> str:
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f5f5f5; color: #333; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 2rem; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h1 { color: #1a73e8; margin-bottom: 1rem; }
        h2 { color: #333; margin: 2rem 0 1rem; border-bottom: 2px solid #1a73e8; padding-bottom: 0.5rem; }
        .meta { color: #666; font-size: 0.9rem; margin-bottom: 0.5rem; }
        table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
        th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #1a73e8; color: #fff; font-weight: 600; }
        tr:hover { background: #f0f7ff; }
        .section { margin: 1rem 0; }
        pre { background: #f8f9fa; padding: 1rem; border-radius: 4px; overflow-x: auto; }
        """
    def _dict_to_table(self, data: dict) -> str:
        if not data:
            return "<p>Sem dados</p>"
        keys = list(data.keys())
        html = ["<table>", "<tr>"]
        for k in keys:
            html.append(f"<th>{self._escape(str(k))}</th>")
        html.append("</tr><tr>")
        for k in keys:
            val = data[k]
            if isinstance(val, dict):
                html.append(f"<td><pre>{self._escape(str(val))}</pre></td>")
            else:
                html.append(f"<td>{self._escape(str(val))}</td>")
        html.append("</tr></table>")
        return "\n".join(html)
    def _list_to_table(self, data: list) -> str:
        if not data:
            return "<p>Sem dados</p>"
        if not data or not isinstance(data[0], dict):
            html = ["<table><tr><th>Item</th></tr>"]
            for item in data:
                html.append(f"<tr><td>{self._escape(str(item))}</td></tr>")
            html.append("</table>")
            return "\n".join(html)
        keys = list(data[0].keys())
        html = ["<table>", "<tr>"]
        for k in keys:
            html.append(f"<th>{self._escape(str(k))}</th>")
        html.append("</tr>")
        for row in data:
            html.append("<tr>")
            for k in keys:
                val = row.get(k, "")
                html.append(f"<td>{self._escape(str(val))}</td>")
            html.append("</tr>")
        html.append("</table>")
        return "\n".join(html)
    @staticmethod
    def _escape(text: str) -> str:
        return (
            text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )
###############################################################################
# END FILE
###############################################################################
