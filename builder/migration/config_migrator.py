###############################################################################
# ProjectBuilder
#
# EPIC.......: 006
# Sprint.....: 6.2
# Arquivo....: builder/migration/config_migrator.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Migrador de configurações do VS Code e VSCodium.
#   Migra settings.json, keybindings.json, tasks.json,
#   launch.json e outros arquivos de configuração.
#
###############################################################################
from __future__ import annotations
import json
import shutil
from pathlib import Path
from typing import Any
from .migration_result import MigrationItem, MigrationAction, MigrationStatus
class ConfigurationMigrator:
    """
    Migração de configurações entre editores.
    Suporta:
        • settings.json
        • keybindings.json
        • tasks.json
        • launch.json
        • argv.json
        • locale.json
    """
    CONFIG_FILES = [
        "settings.json",
        "keybindings.json",
        "tasks.json",
        "launch.json",
        "argv.json",
        "locale.json",
    ]
    def __init__(
        self,
        merge_strategy: str = "replace",
    ) -> None:
        """
        Args:
            merge_strategy: Estrategia de merge.
                • "replace" - substitui completamente
                • "merge"   - mescla configurações
                • "skip"    - ignora se destino existe
        """
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
        Migra todas as configurações.
        """
        items: list[MigrationItem] = []
        source_dir = source_user_dir / "User" if source_user_dir.exists() else source_user_dir
        target_dir = target_user_dir / "User"
        if not source_dir.exists():
            for filename in self.CONFIG_FILES:
                items.append(MigrationItem(
                    name=filename,
                    category="Settings",
                    source=source_dir / filename,
                    destination=target_dir / filename,
                    status=MigrationStatus.FAILED,
                    error="Diretório de origem não encontrado",
                ))
            return items
        target_dir.mkdir(parents=True, exist_ok=True)
        for filename in self.CONFIG_FILES:
            item = self._migrate_file(
                filename, source_dir, target_dir,
            )
            items.append(item)
        return items
    def migrate_snippets(
        self,
        source_user_dir: Path,
        target_user_dir: Path,
    ) -> list[MigrationItem]:
        """
        Migra snippets personalizados.
        """
        items: list[MigrationItem] = []
        source_dir = source_user_dir / "User" / "snippets"
        target_dir = target_user_dir / "User" / "snippets"
        if not source_dir.exists():
            items.append(MigrationItem(
                name="snippets",
                category="Snippets",
                source=source_dir,
                status=MigrationStatus.SKIPPED,
                error="Pasta snippets não encontrada na origem",
            ))
            return items
        target_dir.mkdir(parents=True, exist_ok=True)
        for snippet_file in source_dir.glob("*.json"):
            item = MigrationItem(
                name=snippet_file.name,
                category="Snippets",
                source=snippet_file,
                destination=target_dir / snippet_file.name,
            )
            try:
                item.source_exists = snippet_file.exists()
                item.size = snippet_file.stat().st_size
                shutil.copy2(snippet_file, target_dir / snippet_file.name)
                item.migrated = True
                item.status = MigrationStatus.COMPLETED
            except Exception as e:
                item.error = str(e)
                item.status = MigrationStatus.FAILED
            items.append(item)
        return items
    def _migrate_file(
        self,
        filename: str,
        source_dir: Path,
        target_dir: Path,
    ) -> MigrationItem:
        item = MigrationItem(
            name=filename,
            category="Settings",
            source=source_dir / filename,
            destination=target_dir / filename,
        )
        item.source_exists = item.source.exists()
        item.destination_exists = item.destination.exists()
        if not item.source_exists:
            item.status = MigrationStatus.SKIPPED
            item.error = "Arquivo não encontrado na origem"
            return item
        item.size = item.source.stat().st_size
        # Estratégia de merge
        if self._merge_strategy == "replace" or not item.destination_exists:
            return self._replace_copy(item)
        elif self._merge_strategy == "merge":
            return self._merge_copy(item)
        else:  # skip
            item.status = MigrationStatus.SKIPPED
            item.error = "Arquivo já existe no destino"
            return item
    def _replace_copy(self, item: MigrationItem) -> MigrationItem:
        try:
            item.destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item.source, item.destination)
            item.migrated = True
            item.status = MigrationStatus.COMPLETED
            item.action = MigrationAction.REPLACE
        except Exception as e:
            item.error = str(e)
            item.status = MigrationStatus.FAILED
        return item
    def _merge_copy(self, item: MigrationItem) -> MigrationItem:
        try:
            # Carrega configurações existentes
            existing: dict[str, Any] = {}
            if item.destination.exists():
                existing = json.loads(
                    item.destination.read_text(encoding="utf-8")
                )
            # Carrega novas configurações
            new_config: dict[str, Any] = json.loads(
                item.source.read_text(encoding="utf-8")
            )
            # Merge: novas sobrescrevem existentes
            merged = {**existing, **new_config}
            item.destination.parent.mkdir(parents=True, exist_ok=True)
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
        return item
###############################################################################
# END FILE
###############################################################################
