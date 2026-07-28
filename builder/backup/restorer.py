###############################################################################
# ProjectBuilder
#
# EPIC.......: 005
# Sprint.....: 5.6
# Arquivo....: builder/backup/restorer.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Restauração de backups do VS Code e VSCodium.
#
###############################################################################
from __future__ import annotations
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from .backup_result import BackupResult, BackupStatus, BackupItem
from .compressor import BackupCompressor, CompressionResult
@dataclass(slots=True)
class RestoreResult:
    """Resultado da restauração."""
    editor: str = ""
    status: BackupStatus = field(default=BackupStatus.CREATED)
    started_at: datetime = field(default_factory=datetime.now)
    finished_at: datetime | None = None
    duration: float = 0.0
    source_archive: Path | None = None
    destination: Path | None = None
    items_restored: int = 0
    errors: list[str] = field(default_factory=list)
    def finish(self) -> None:
        self.finished_at = datetime.now()
        delta = self.finished_at - self.started_at
        self.duration = delta.total_seconds()
class BackupRestorer:
    """
    Restauração de backups.
    Responsável por restaurar backups do VS Code
    e VSCodium para seus diretórios originais.
    """
    def __init__(
        self,
        compressor: BackupCompressor | None = None,
    ) -> None:
        self._compressor = compressor or BackupCompressor()
    @property
    def compressor(self) -> BackupCompressor:
        return self._compressor
    def restore_directory(
        self,
        archive: Path,
        destination: Path,
        editor: str = "",
    ) -> RestoreResult:
        """
        Restaura um backup compactado.
        """
        result = RestoreResult(
            editor=editor,
            source_archive=archive,
            destination=destination,
        )
        if not archive.exists():
            result.errors.append(f"Arquivo não encontrado: {archive}")
            result.status = BackupStatus.FAILED
            result.finish()
            return result
        result.status = BackupStatus.RESTORED
        try:
            comp_result = self._compressor.decompress(
                archive, destination,
            )
            if comp_result.success:
                result.items_restored = 1
                result.status = BackupStatus.RESTORED
            else:
                result.errors.append(comp_result.error)
                result.status = BackupStatus.FAILED
        except Exception as e:
            result.errors.append(str(e))
            result.status = BackupStatus.FAILED
        result.finish()
        return result
    def restore_files(
        self,
        archive: Path,
        destination: Path,
        editor: str = "",
        file_pattern: str = "",
    ) -> RestoreResult:
        """
        Restaura arquivos específicos de um backup.
        """
        result = RestoreResult(
            editor=editor,
            source_archive=archive,
            destination=destination,
        )
        if not archive.exists():
            result.errors.append(f"Arquivo não encontrado: {archive}")
            result.status = BackupStatus.FAILED
            result.finish()
            return result
        try:
            temp_dir = destination.parent / f".temp_restore_{archive.stem}"
            temp_dir.mkdir(parents=True, exist_ok=True)
            comp_result = self._compressor.decompress(
                archive, temp_dir,
            )
            if comp_result.success:
                if file_pattern:
                    for file in temp_dir.rglob(file_pattern):
                        if file.is_file():
                            target = destination / file.relative_to(temp_dir)
                            target.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(file, target)
                            result.items_restored += 1
                else:
                    for file in temp_dir.rglob("*"):
                        if file.is_file():
                            target = destination / file.relative_to(temp_dir)
                            target.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(file, target)
                            result.items_restored += 1
                result.status = BackupStatus.RESTORED
            else:
                result.errors.append(comp_result.error)
                result.status = BackupStatus.FAILED
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            result.errors.append(str(e))
            result.status = BackupStatus.FAILED
        result.finish()
        return result
    def restore_single_file(
        self,
        source: Path,
        destination: Path,
    ) -> RestoreResult:
        """
        Restaura um arquivo individual.
        """
        result = RestoreResult(
            source_archive=source,
            destination=destination,
        )
        if not source.exists():
            result.errors.append(f"Arquivo não encontrado: {source}")
            result.status = BackupStatus.FAILED
            result.finish()
            return result
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            result.items_restored = 1
            result.status = BackupStatus.RESTORED
        except Exception as e:
            result.errors.append(str(e))
            result.status = BackupStatus.FAILED
        result.finish()
        return result
###############################################################################
# END FILE
###############################################################################
