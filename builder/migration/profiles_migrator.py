###############################################################################
# ProjectBuilder
#
# EPIC.......: 006
# Sprint.....: 6.4
# Arquivo....: builder/migration/profiles_migrator.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Migrador de Profiles do VS Code e VSCodium.
#
###############################################################################
from __future__ import annotations
import json
import shutil
from pathlib import Path
from typing import Any
from .migration_result import MigrationItem, MigrationAction, MigrationStatus
class ProfilesMigrator:
    """
    Migração de Profiles entre editores.
    """
    PROFILE_DIRS = [
        "settings.json",
        "keybindings.json",
        "tasks.json",
        "launch.json",
        "snippets",
        "extensions.json",
        "profile.json",
    ]
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
        source_profiles_dir: Path,
        target_profiles_dir: Path,
    ) -> list[MigrationItem]:
        """
        Migra todos os profiles.
        """
        items: list[MigrationItem] = []
        if not source_profiles_dir.exists():
            items.append(MigrationItem(
                name="profiles",
                category="Profiles",
                source=source_profiles_dir,
                destination=target_profiles_dir,
                status=MigrationStatus.SKIPPED,
                error="Diretório de profiles não encontrado",
            ))
            return items
        target_profiles_dir.mkdir(parents=True, exist_ok=True)
        for profile_dir in sorted(source_profiles_dir.iterdir()):
            if not profile_dir.is_dir():
                continue
            profile_items = self._migrate_profile(
                profile_dir,
                target_profiles_dir / profile_dir.name,
            )
            items.extend(profile_items)
        return items
    def _migrate_profile(
        self,
        source: Path,
        target: Path,
    ) -> list[MigrationItem]:
        items: list[MigrationItem] = []
        target.mkdir(parents=True, exist_ok=True)
        # profile.json
        profile_json = source / "profile.json"
        if profile_json.exists():
            item = MigrationItem(
                name=f"Profile/{profile_json.parent.name}/profile.json",
                category="Profiles",
                source=profile_json,
                destination=target / "profile.json",
                action=MigrationAction.COPY,
            )
            item.source_exists = True
            item.size = profile_json.stat().st_size
            try:
                shutil.copy2(profile_json, target / "profile.json")
                item.migrated = True
                item.status = MigrationStatus.COMPLETED
            except Exception as e:
                item.error = str(e)
                item.status = MigrationStatus.FAILED
            items.append(item)
        # Arquivos de configuração do profile
        for filename in ["settings.json", "keybindings.json", "tasks.json", "launch.json"]:
            file = source / filename
            if file.exists():
                item = MigrationItem(
                    name=f"Profile/{source.name}/{filename}",
                    category="Profiles",
                    source=file,
                    destination=target / filename,
                    action=MigrationAction.COPY,
                )
                item.source_exists = True
                item.size = file.stat().st_size
                try:
                    shutil.copy2(file, target / filename)
                    item.migrated = True
                    item.status = MigrationStatus.COMPLETED
                except Exception as e:
                    item.error = str(e)
                    item.status = MigrationStatus.FAILED
                items.append(item)
        # Snippets do profile
        snippets_dir = source / "snippets"
        if snippets_dir.exists() and snippets_dir.is_dir():
            target_snippets = target / "snippets"
            target_snippets.mkdir(parents=True, exist_ok=True)
            for snippet in snippets_dir.glob("*.json"):
                item = MigrationItem(
                    name=f"Profile/{source.name}/snippets/{snippet.name}",
                    category="Profiles",
                    source=snippet,
                    destination=target_snippets / snippet.name,
                    action=MigrationAction.COPY,
                )
                item.source_exists = True
                item.size = snippet.stat().st_size
                try:
                    shutil.copy2(snippet, target_snippets / snippet.name)
                    item.migrated = True
                    item.status = MigrationStatus.COMPLETED
                except Exception as e:
                    item.error = str(e)
                    item.status = MigrationStatus.FAILED
                items.append(item)
        return items
###############################################################################
# END FILE
###############################################################################
