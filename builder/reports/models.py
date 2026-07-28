###############################################################################
# ProjectBuilder
#
# EPIC.......: 007
# Sprint.....: 7.1
# Arquivo....: builder/reports/models.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Modelos de dados para o sistema de relatórios.
#
###############################################################################
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any
class ReportFormat(Enum):
    """Formatos suportados de relatório."""
    HTML = auto()
    JSON = auto()
    MARKDOWN = auto()
    PDF = auto()
    LOG = auto()
    ALL = auto()
@dataclass(slots=True)
class ReportData:
    """Dados de um relatório."""
    title: str = "ProjectBuilder Report"
    report_type: str = ""
    generated_at: datetime = field(default_factory=datetime.now)
    sections: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    def add_section(self, name: str, data: Any) -> None:
        self.sections[name] = data
    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "report_type": self.report_type,
            "generated_at": str(self.generated_at),
            "sections": self.sections,
            "metadata": self.metadata,
        }
###############################################################################
# END FILE
###############################################################################
