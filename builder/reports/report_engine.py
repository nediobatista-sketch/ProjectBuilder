###############################################################################
# ProjectBuilder
#
# EPIC.......: 007
# Sprint.....: 7.1
# Arquivo....: builder/reports/report_engine.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Motor principal de geração de relatórios.
#   Coordena a geração em múltiplos formatos.
#
###############################################################################
from __future__ import annotations
from pathlib import Path
from typing import Any
from .models import ReportData, ReportFormat
from .html_report import HtmlReportGenerator
from .json_report import JsonReportGenerator
from .markdown_report import MarkdownReportGenerator
from .pdf_report import PdfReportGenerator
from .log_report import LogReportGenerator
class ReportEngine:
    """
    Motor de geração de relatórios.
    Suporta saída em múltiplos formatos simultaneamente.
    """
    GENERATORS = {
        "html": HtmlReportGenerator,
        "json": JsonReportGenerator,
        "markdown": MarkdownReportGenerator,
        "pdf": PdfReportGenerator,
        "log": LogReportGenerator,
    }
    def __init__(
        self,
        output_directory: Path | None = None,
    ) -> None:
        self._output_dir = output_directory or Path.cwd() / "reports"
    @property
    def output_directory(self) -> Path:
        return self._output_dir
    def generate(
        self,
        data: ReportData,
        formats: list[ReportFormat] | None = None,
        filename_prefix: str = "report",
    ) -> dict[str, Path]:
        self._output_dir.mkdir(parents=True, exist_ok=True)
        results: dict[str, Path] = {}
        if formats is None:
            formats = [ReportFormat.HTML, ReportFormat.JSON]
        for fmt in formats:
            if fmt == ReportFormat.ALL:
                for gen_format in self.GENERATORS:
                    path = self._generate_single(
                        data, gen_format, filename_prefix,
                    )
                    if path:
                        results[gen_format] = path
            else:
                gen_name = fmt.name.lower()
                path = self._generate_single(
                    data, gen_name, filename_prefix,
                )
                if path:
                    results[gen_name] = path
        return results
    def generate_from_backup(
        self,
        backup_result: Any,
        formats: list[ReportFormat] | None = None,
    ) -> dict[str, Path]:
        data = ReportData(
            title=f"Backup Report - {getattr(backup_result, 'editor', 'Unknown')}",
            report_type="backup",
            sections={
                "backup": backup_result.to_dict()
                if hasattr(backup_result, "to_dict") else str(backup_result),
            },
        )
        return self.generate(data, formats)
    def generate_from_migration(
        self,
        migration_result: Any,
        formats: list[ReportFormat] | None = None,
    ) -> dict[str, Path]:
        data = ReportData(
            title=(
                f"Migration Report - "
                f"{getattr(migration_result, 'source_editor', 'Unknown')} "
                f"→ "
                f"{getattr(migration_result, 'target_editor', 'Unknown')}"
            ),
            report_type="migration",
            sections={
                "migration": migration_result.to_dict()
                if hasattr(migration_result, "to_dict") else str(migration_result),
            },
        )
        return self.generate(data, formats)
    def _generate_single(
        self,
        data: ReportData,
        format_name: str,
        prefix: str,
    ) -> Path | None:
        ext_map = {
            "html": ".html",
            "json": ".json",
            "markdown": ".md",
            "pdf": ".pdf",
            "log": ".log",
        }
        ext = ext_map.get(format_name, f".{format_name}")
        filename = f"{prefix}_{format_name}{ext}"
        output = self._output_dir / filename
        generator_class = self.GENERATORS.get(format_name)
        if generator_class is None:
            return None
        generator = generator_class()
        try:
            generator.generate(data, output)
            return output
        except Exception:
            return None
###############################################################################
# END FILE
###############################################################################
