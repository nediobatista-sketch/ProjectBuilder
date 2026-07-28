###############################################################################
# ProjectBuilder
#
# EPIC.......: 006
# Sprint.....: 6.5
# Arquivo....: builder/migration/snippets_migrator.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Migrador de Snippets do VS Code e VSCodium.
#
###############################################################################
from __future__ import annotations
import json
import shutil
from pathlib import Path
from typing import Any
from .migration_result import MigrationItem, MigrationAction, MigrationStatus
class SnippetsMigrator:
    """
    Migração de Snippets personalizados.
    """
    def __init__(
        self,
        merge_strategy: str = "replace",
    ) -> None:
        self._merge_strategy = merge_strategy
    @property
    def merge_strategy(self) -> str:
        return self._merge_strategy
    def migrate(
        self,
        source_user_dir: Path,
        target_user_dir: Path,
    ) -> list[MigrationItem]:
        """
        Migra todos os snippets.
        """
        items: list[MigrationItem] = []
        source_dir = source_user_dir / "User" / "snippets"
        target_dir = target_user_dir / "User" / "snippets"
        if not source_dir.exists():
            items.append(MigrationItem(
                name="snippets",
                category="Snippets",
                source=source_dir,
                destination=target_dir,
                status=MigrationStatus.SKIPPED,
                error="Pasta snippets não encontrada",
            ))
            return items
        target_dir.mkdir(parents=True, exist_ok=True)
        for snippet_file in sorted(source_dir.glob("*.json")):
            item = MigrationItem(
                name=snippet_file.name,
                category="Snippets",
                source=snippet_file,
                destination=target_dir / snippet_file.name,
                action=MigrationAction.COPY,
            )
            item.source_exists = True
            item.destination_exists = (
                target_dir / snippet_file.name
            ).exists()
            item.size = snippet_file.stat().st_size
            if self._merge_strategy == "replace" or not item.destination_exists:
                self._replace_copy(item)
            elif self._merge_strategy == "merge":
                self._merge_copy(item)
            else:
                item.status = MigrationStatus.SKIPPED
                item.error = "Snippet já existe no destino"
            items.append(item)
        return items
    def _replace_copy(self, item: MigrationItem) -> None:
        try:
            shutil.copy2(item.source, item.destination)
            item.migrated = True
            item.status = MigrationStatus.COMPLETED
            item.action = MigrationAction.REPLACE
        except Exception as e:
            item.error = str(e)
            item.status = MigrationStatus.FAILED
    def _merge_copy(self, item: MigrationItem) -> None:
        try:
            existing: dict[str, Any] = {}
            if item.destination.exists():
                existing = json.loads(
                    item.destination.read_text(encoding="utf-8")
                )
            new_snippets: dict[str, Any] = json.loads(
                item.source.read_text(encoding="utf-8")
            )
            merged = {**existing, **new_snippets}
            item.destination.write_text(
                json.dumps(merged, indent=4, ensure_ascii=False),
                encoding="utf-8",
            )
            item.migrated = True
            item.status = MigrationStatus.COMPLETED
            item.action = MigrationAction.MERGE
        except Exception as e:
            item.error = str(e)
            item.status = MigrationStatus.FAILED
###############################################################################
# END FILE
###############################################################################
