###############################################################################
# ProjectBuilder
#
# EPIC.......: 005
# Sprint.....: 5.1
# Arquivo....: builder/backup/backup_result.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Estrutura de resultado das operações de Backup.
#
###############################################################################
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any
class BackupStatus(Enum):
    """Estados possíveis de um Backup."""
    CREATED = auto()
    COMPRESSING = auto()
    VERSIONED = auto()
    VERIFIED = auto()
    COMPLETED = auto()
    FAILED = auto()
    RESTORED = auto()
@dataclass(slots=True)
class BackupItem:
    """
    Representa um item individual do backup.
    """
    name: str
    source: Path
    exists: bool = False
    size: int = 0
    backup_path: Path | None = None
    backed_up: bool = False
    error: str = ""
@dataclass(slots=True)
class BackupResult:
    """
    Resultado completo de uma operação de Backup.
    """
    editor: str = ""
    status: BackupStatus = field(
        default=BackupStatus.CREATED,
    )
    started_at: datetime = field(
        default_factory=datetime.now,
    )
    finished_at: datetime | None = None
    duration: float = 0.0
    items: list[BackupItem] = field(default_factory=list)
    archive_path: Path | None = None
    version: str = ""
    checksum: str = ""
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    total_size: int = 0
    compressed_size: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    def add_item(
        self,
        item: BackupItem,
    ) -> None:
        self.items.append(item)
        if item.exists and not item.error:
            self.total_size += item.size
    @property
    def success(self) -> bool:
        return self.status == BackupStatus.COMPLETED
    @property
    def item_count(self) -> int:
        return len(self.items)
    @property
    def backed_up_count(self) -> int:
        return sum(1 for i in self.items if i.backed_up)
    @property
    def failed_count(self) -> int:
        return sum(1 for i in self.items if i.error)
    @property
    def compression_ratio(self) -> float:
        if self.total_size == 0:
            return 0.0
        return self.compressed_size / self.total_size
    def finish(self) -> None:
        self.finished_at = datetime.now()
        delta = self.finished_at - self.started_at
        self.duration = delta.total_seconds()
    def add_error(
        self,
        message: str,
    ) -> None:
        self.errors.append(message)
        self.status = BackupStatus.FAILED
    def add_warning(
        self,
        message: str,
    ) -> None:
        self.warnings.append(message)
    def to_dict(self) -> dict[str, Any]:
        return {
            "editor": self.editor,
            "status": self.status.name,
            "started_at": str(self.started_at),
            "finished_at": str(self.finished_at),
            "duration": self.duration,
            "items": [
                {
                    "name": item.name,
                    "source": str(item.source),
                    "exists": item.exists,
                    "size": item.size,
                    "backed_up": item.backed_up,
                    "error": item.error,
                }
                for item in self.items
            ],
            "archive_path": str(self.archive_path) if self.archive_path else None,
            "version": self.version,
            "checksum": self.checksum,
            "total_size": self.total_size,
            "compressed_size": self.compressed_size,
            "backed_up_count": self.backed_up_count,
            "failed_count": self.failed_count,
            "errors": self.errors,
            "warnings": self.warnings,
        }
###############################################################################
# END FILE
###############################################################################
