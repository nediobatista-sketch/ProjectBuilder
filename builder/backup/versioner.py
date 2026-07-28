###############################################################################
# ProjectBuilder
#
# EPIC.......: 005
# Sprint.....: 5.5
# Arquivo....: builder/backup/versioner.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Versionamento de backups.
#   Mantém um histórico de backups com numeração
#   sequencial e metadados.
#
###############################################################################
from __future__ import annotations
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
@dataclass(slots=True)
class BackupVersion:
    """
    Representa uma versão de backup.
    """
    number: int
    timestamp: datetime = field(default_factory=datetime.now)
    editor: str = ""
    size: int = 0
    archive_path: Path | None = None
    checksum: str = ""
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
@dataclass(slots=True)
class VersionHistory:
    """
    Histórico completo de backups versionados.
    """
    editor: str = ""
    versions: list[BackupVersion] = field(default_factory=list)
    def add(self, version: BackupVersion) -> None:
        self.versions.append(version)
    @property
    def latest(self) -> BackupVersion | None:
        if self.versions:
            return max(self.versions, key=lambda v: v.timestamp)
        return None
    @property
    def count(self) -> int:
        return len(self.versions)
    def to_dict(self) -> dict[str, Any]:
        return {
            "editor": self.editor,
            "count": self.count,
            "versions": [
                {
                    "number": v.number,
                    "timestamp": str(v.timestamp),
                    "editor": v.editor,
                    "size": v.size,
                    "archive_path": str(v.archive_path) if v.archive_path else None,
                    "checksum": v.checksum,
                    "description": v.description,
                    "metadata": v.metadata,
                }
                for v in self.versions
            ],
        }
class BackupVersioner:
    """
    Gerenciamento de versões de backups.
    """
    HISTORY_FILENAME = "versions.json"
    def __init__(
        self,
        backup_directory: Path,
    ) -> None:
        self._backup_dir = backup_directory
        self._history = VersionHistory()
        self._load_history()
    @property
    def backup_directory(self) -> Path:
        return self._backup_dir
    @property
    def history(self) -> VersionHistory:
        return self._history
    def version(
        self,
        archive_path: Path,
        editor: str = "",
        description: str = "",
        checksum: str = "",
    ) -> BackupVersion:
        """
        Cria uma nova versão de backup.
        """
        number = self._next_version_number()
        size = archive_path.stat().st_size if archive_path.exists() else 0
        version = BackupVersion(
            number=number,
            editor=editor,
            size=size,
            archive_path=archive_path,
            checksum=checksum,
            description=description,
        )
        self._history.editor = editor
        self._history.add(version)
        self._save_history()
        return version
    def list_versions(self) -> list[BackupVersion]:
        """
        Lista todas as versões disponíveis.
        """
        return sorted(
            self._history.versions,
            key=lambda v: v.timestamp,
            reverse=True,
        )
    def get_version(self, number: int) -> BackupVersion | None:
        """
        Obtém uma versão específica.
        """
        for v in self._history.versions:
            if v.number == number:
                return v
        return None
    def delete_version(self, number: int) -> bool:
        """
        Remove uma versão do histórico.
        """
        version = self.get_version(number)
        if version is None:
            return False
        if version.archive_path and version.archive_path.exists():
            version.archive_path.unlink()
        self._history.versions = [
            v for v in self._history.versions
            if v.number != number
        ]
        self._save_history()
        return True
    def purge_old(
        self,
        keep_count: int = 10,
    ) -> int:
        """
        Remove versões antigas, mantendo apenas
        as mais recentes.
        """
        versions = sorted(
            self._history.versions,
            key=lambda v: v.timestamp,
        )
        removed = 0
        while len(versions) > keep_count:
            oldest = versions.pop(0)
            if oldest.archive_path and oldest.archive_path.exists():
                oldest.archive_path.unlink()
            removed += 1
        self._history.versions = versions
        self._save_history()
        return removed
    # ─── Privados ──────────────────────────────────────────────────────
    def _next_version_number(self) -> int:
        if not self._history.versions:
            return 1
        return max(v.number for v in self._history.versions) + 1
    def _load_history(self) -> None:
        history_file = self._backup_dir / self.HISTORY_FILENAME
        if not history_file.exists():
            return
        try:
            data = json.loads(
                history_file.read_text(encoding="utf-8")
            )
            self._history.editor = data.get("editor", "")
            for v_data in data.get("versions", []):
                self._history.add(BackupVersion(
                    number=v_data.get("number", 0),
                    timestamp=datetime.fromisoformat(
                        v_data.get("timestamp", "")
                    ),
                    editor=v_data.get("editor", ""),
                    size=v_data.get("size", 0),
                    archive_path=Path(v_data["archive_path"]) if v_data.get("archive_path") else None,
                    checksum=v_data.get("checksum", ""),
                    description=v_data.get("description", ""),
                    metadata=v_data.get("metadata", {}),
                ))
        except Exception:
            pass
    def _save_history(self) -> None:
        self._backup_dir.mkdir(parents=True, exist_ok=True)
        history_file = self._backup_dir / self.HISTORY_FILENAME
        history_file.write_text(
            json.dumps(
                self._history.to_dict(),
                indent=4,
                ensure_ascii=False,
                default=str,
            ),
            encoding="utf-8",
        )
###############################################################################
# END FILE
###############################################################################
