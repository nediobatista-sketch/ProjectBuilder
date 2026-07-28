###############################################################################
# ProjectBuilder
#
# EPIC.......: 007
# Sprint.....: 7.5
# Arquivo....: builder/reports/pdf_report.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Gerador de relatórios em PDF.
#   Utiliza a biblioteca fpdf2 para geração.
#
###############################################################################
from __future__ import annotations
from pathlib import Path
from .models import ReportData
class PdfReportGenerator:
    """Geração de relatórios em PDF."""
    def generate(
        self,
        data: ReportData,
        output: Path,
    ) -> None:
        try:
            from fpdf import FPDF
        except ImportError:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                f"ProjectBuilder Report\n"
                f"{'='*50}\n"
                f"Title: {data.title}\n"
                f"Type: {data.report_type}\n"
                f"Generated: {data.generated_at}\n"
                f"{'='*50}\n",
                encoding="utf-8",
            )
            return
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 20)
        pdf.cell(0, 10, data.title, ln=True, align="C")
        pdf.ln(5)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 5, f"Tipo: {data.report_type}", ln=True)
        pdf.cell(0, 5, f"Gerado em: {data.generated_at}", ln=True)
        pdf.ln(10)
        for name, section_data in data.sections.items():
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 8, name, ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.ln(2)
            if isinstance(section_data, dict):
                for key, value in section_data.items():
                    val_str = str(value)[:200]
                    pdf.cell(40, 5, f"{key}:", ln=False)
                    pdf.cell(0, 5, val_str, ln=True)
            elif isinstance(section_data, list):
                for item in section_data:
                    pdf.cell(0, 5, f"  - {item}", ln=True)
            else:
                pdf.multi_cell(0, 5, str(section_data)[:1000])
            pdf.ln(5)
        output.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(output))
###############################################################################
# END FILE
###############################################################################
