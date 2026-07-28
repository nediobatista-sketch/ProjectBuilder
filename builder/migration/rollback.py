###############################################################################
# ProjectBuilder
#
# EPIC.......: 006
# Sprint.....: 6.7
# Arquivo....: builder/migration/rollback.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Gerenciador de Rollback para operações de Migration.
#   Permite reverter migrações em caso de falha.
#
###############################################################################
from __future__ import annotations
import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from .migration_result import MigrationItem, MigrationStatus
@dataclass(slots=True)
class RollbackEntry:
    """Entrada individual de rollback."""
    item: MigrationItem
    backup_path: Path | None = None
    backup_exists: bool = False
@dataclass(slots=True)
class RollbackPlan:
    """Plano de rollback de uma migração."""
    source_editor: str = ""
    target_editor: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    rollback_dir: Path | None = None
    entries: list[RollbackEntry] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    def add_entry(
        self,
        entry: RollbackEntry,
    ) -> None:
        self.entries.append(entry)
    @property
    def entry_count(self) -> int:
        return len(self.entries)
    @property
    def backup_count(self) -> int:
        return sum(
            1 for e in self.entries if e.backup_exists
        )
    def to_dict(self) -> dict[str, Any]:
        return {
            "source_editor": self.source_editor,
            "target_editor": self.target_editor,
            "created_at": str(self.created_at),
            "rollback_dir": str(self.rollback_dir) if self.rollback_dir else None,
            "entry_count": self.entry_count,
            "backup_count": self.backup_count,
            "entries": [
                {
                    "name": e.item.name,
                    "category": e.item.category,
                    "backup_path": str(e.backup_path) if e.backup_path else None,
                    "backup_exists": e.backup_exists,
                }
                for e in self.entries
            ],
        }
class RollbackManager:
    """
    Gerenciador de Rollback.
    Cria backups antes da migração para permitir
    a reversão completa.
    """
    ROLLBACK_DIR = ".rollback"
    PLAN_FILENAME = "rollback_plan.json"
    def __init__(
        self,
        target_directory: Path,
    ) -> None:
        self._target_dir = target_directory
        self._rollback_dir = (
            target_directory / self.ROLLBACK_DIR
        )
    @property
    def rollback_directory(self) -> Path:
        return self._rollback_dir
    def create_plan(
        self,
        items: list[MigrationItem],
        source_editor: str = "",
        target_editor: str = "",
    ) -> RollbackPlan:
        """
        Cria um plano de rollback fazendo backup
        dos arquivos que serão sobrescritos.
        """
        plan = RollbackPlan(
            source_editor=source_editor,
            target_editor=target_editor,
        )
        self._rollback_dir.mkdir(parents=True, exist_ok=True)
        for item in items:
            entry = self._create_backup(item)
            plan.add_entry(entry)
        # Salva o plano
        plan_file = self._rollback_dir / self.PLAN_FILENAME
        plan.rollback_dir = self._rollback_dir
        plan_file.write_text(
            json.dumps(
                plan.to_dict(),
                indent=4,
                ensure_ascii=False,
                default=str,
            ),
            encoding="utf-8",
        )
        return plan
    def execute_rollback(
        self,
        plan_file: Path | None = None,
    ) -> dict[str, Any]:
        """
        Executa o rollback de uma migração.
        """
        if plan_file is None:
            plan_file = self._rollback_dir / self.PLAN_FILENAME
        if not plan_file.exists():
            return {
                "success": False,
                "error": "Plano de rollback não encontrado",
            }
        try:
            data = json.loads(
                plan_file.read_text(encoding="utf-8")
            )
            restored = 0
            failed = 0
            for entry_data in data.get("entries", []):
                backup_path = entry_data.get("backup_path")
                if not backup_path:
                    continue
                backup = Path(backup_path)
                if not backup.exists():
                    failed += 1
                    continue
                # Reconstrói o caminho original
                original_path = backup.parent.parent / backup.name
                if original_path.exists():
                    try:
                        shutil.copy2(backup, original_path)
                        restored += 1
                    except Exception:
                        failed += 1
                else:
                    original_path.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        shutil.copy2(backup, original_path)
                        restored += 1
                    except Exception:
                        failed += 1
            return {
                "success": True,
                "restored": restored,
                "failed": failed,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    def load_plan(self) -> RollbackPlan | None:
        """
        Carrega um plano de rollback existente.
        """
        plan_file = self._rollback_dir / self.PLAN_FILENAME
        if not plan_file.exists():
            return None
        try:
            data = json.loads(
                plan_file.read_text(encoding="utf-8")
            )
            plan = RollbackPlan(
                source_editor=data.get("source_editor", ""),
                target_editor=data.get("target_editor", ""),
                created_at=datetime.fromisoformat(
                    data.get("created_at", "")
                ),
                rollback_dir=self._rollback_dir,
            )
            return plan
        except Exception:
            return None
    def cleanup(self) -> int:
        """
        Remove o diretório de rollback.
        Retorna o número de arquivos removidos.
        """
        if not self._rollback_dir.exists():
            return 0
        count = sum(1 for _ in self._rollback_dir.rglob("*"))
        shutil.rmtree(self._rollback_dir, ignore_errors=True)
        return count
    def _create_backup(self, item: MigrationItem) -> RollbackEntry:
        entry = RollbackEntry(item=item)
        if item.destination and item.destination.exists():
            backup_path = (
                self._rollback_dir
                / f"{item.category}_{item.name.replace('/', '_')}.backup"
            )
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(item.destination, backup_path)
                entry.backup_path = backup_path
                entry.backup_exists = True
            except Exception:
                pass
        return entry
###############################################################################
# END FILE
###############################################################################
