###############################################################################
# ProjectBuilder
#
# EPIC.......: 006
# Sprint.....: 6.1
# Arquivo....: builder/migration/migration_result.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Estruturas de resultado das operações de Migration.
#
###############################################################################
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any
class MigrationStatus(Enum):
    """Estados possíveis de uma Migration."""
    CREATED = auto()
    ANALYZING = auto()
    MIGRATING = auto()
    VALIDATING = auto()
    COMPLETED = auto()
    ROLLED_BACK = auto()
    FAILED = auto()
    SKIPPED = auto()
class MigrationAction(Enum):
    """Tipos de ação de migração."""
    COPY = auto()
    MERGE = auto()
    REPLACE = auto()
    CREATE = auto()
    DELETE = auto()
    SKIP = auto()
@dataclass(slots=True)
class MigrationItem:
    """
    Representa um item individual da migração.
    """
    name: str
    category: str = ""
    source: Path | None = None
    destination: Path | None = None
    action: MigrationAction = field(
        default=MigrationAction.COPY,
    )
    status: MigrationStatus = field(
        default=MigrationStatus.CREATED,
    )
    source_exists: bool = False
    destination_exists: bool = False
    migrated: bool = False
    error: str = ""
    size: int = 0
@dataclass(slots=True)
class MigrationResult:
    """
    Resultado completo de uma operação de Migration.
    """
    source_editor: str = ""
    target_editor: str = ""
    status: MigrationStatus = field(
        default=MigrationStatus.CREATED,
    )
    started_at: datetime = field(
        default_factory=datetime.now,
    )
    finished_at: datetime | None = None
    duration: float = 0.0
    items: list[MigrationItem] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    rollback_available: bool = False
    rollback_path: Path | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    def add_item(self, item: MigrationItem) -> None:
        self.items.append(item)
    @property
    def success(self) -> bool:
        return self.status == MigrationStatus.COMPLETED
    @property
    def item_count(self) -> int:
        return len(self.items)
    @property
    def migrated_count(self) -> int:
        return sum(1 for i in self.items if i.migrated)
    @property
    def failed_count(self) -> int:
        return sum(
            1 for i in self.items
            if i.error
        )
    @property
    def skipped_count(self) -> int:
        return sum(
            1 for i in self.items
            if i.status == MigrationStatus.SKIPPED
        )
    def finish(self) -> None:
        self.finished_at = datetime.now()
        delta = self.finished_at - self.started_at
        self.duration = delta.total_seconds()
    def add_error(self, message: str) -> None:
        self.errors.append(message)
        self.status = MigrationStatus.FAILED
    def add_warning(self, message: str) -> None:
        self.warnings.append(message)
    def to_dict(self) -> dict[str, Any]:
        return {
            "source_editor": self.source_editor,
            "target_editor": self.target_editor,
            "status": self.status.name,
            "started_at": str(self.started_at),
            "finished_at": str(self.finished_at),
            "duration": self.duration,
            "items": [
                {
                    "name": item.name,
                    "category": item.category,
                    "source": str(item.source) if item.source else None,
                    "destination": str(item.destination) if item.destination else None,
                    "action": item.action.name,
                    "status": item.status.name,
                    "migrated": item.migrated,
                    "error": item.error,
                }
                for item in self.items
            ],
            "errors": self.errors,
            "warnings": self.warnings,
            "rollback_available": self.rollback_available,
        }
    @property
    def summary_text(self) -> str:
        lines = [
            "=" * 60,
            "MIGRATION REPORT",
            "=" * 60,
            "",
            f"De           : {self.source_editor}",
            f"Para         : {self.target_editor}",
            f"Status       : {self.status.name}",
            f"Início       : {self.started_at}",
            f"Término      : {self.finished_at or 'N/A'}",
            f"Duração      : {self.duration:.4f}s",
            "",
            f"Total itens  : {self.item_count}",
            f"Migrados     : {self.migrated_count}",
            f"Falhas       : {self.failed_count}",
            f"Ignorados    : {self.skipped_count}",
            f"Rollback     : {'Sim' if self.rollback_available else 'Não'}",
            "",
        ]
        if self.errors:
            lines.append("── ERROS ────────────────────────────────────────────")
            for e in self.errors:
                lines.append(f"  ✗ {e}")
            lines.append("")
        if self.warnings:
            lines.append("── AVISOS ───────────────────────────────────────────")
            for w in self.warnings:
                lines.append(f"  ⚠ {w}")
            lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)
    def __repr__(self) -> str:
        return (
            f"MigrationResult("
            f"from='{self.source_editor}', "
            f"to='{self.target_editor}', "
            f"migrated={self.migrated_count}, "
            f"failed={self.failed_count})"
        )
###############################################################################
# END FILE
###############################################################################
