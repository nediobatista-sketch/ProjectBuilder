###############################################################################
# ProjectBuilder
#
# EPIC.......: 006
# Sprint.....: 6.1
# Arquivo....: builder/migration/migration_engine.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Motor principal de Migration do ProjectBuilder.
#   Coordenador que orquestra todos os migradores.
#
###############################################################################
from __future__ import annotations
import os
from pathlib import Path
from typing import Any
from .migration_result import MigrationResult, MigrationStatus, MigrationAction
from .config_migrator import ConfigurationMigrator
from .extensions_migrator import ExtensionsMigrator
from .profiles_migrator import ProfilesMigrator
from .snippets_migrator import SnippetsMigrator
from .workspaces_migrator import WorkspacesMigrator
from .rollback import RollbackManager
###############################################################################
# Diretórios padrão
###############################################################################
VS_CODE_USER_DIR = Path(os.environ.get("APPDATA", "")) / "Code" / "User"
VS_CODE_EXTENSIONS_DIR = Path(
    os.environ.get("USERPROFILE", "")
) / ".vscode" / "extensions"
VSCODIUM_USER_DIR = Path(os.environ.get("APPDATA", "")) / "VSCodium" / "User"
VSCODIUM_EXTENSIONS_DIR = Path(
    os.environ.get("USERPROFILE", "")
) / ".vscode-oss" / "extensions"
###############################################################################
class MigrationEngine:
    """
    Motor principal de Migration.
    Coordena a migração completa entre editores.
    """
    # Direções de migração
    VSCODE_TO_VSCODIUM = "vscode_to_vscodium"
    VSCODIUM_TO_VSCODE = "vscodium_to_vscode"
    def __init__(
        self,
        merge_strategy: str = "replace",
        enable_rollback: bool = True,
        extension_strategy: str = "list",
    ) -> None:
        """
        Args:
            merge_strategy: Estratégia de merge de configurações.
            enable_rollback: Se True, cria backups antes da migração.
            extension_strategy: Estratégia para extensões
                                ("list", "copy", "reinstall").
        """
        self._merge_strategy = merge_strategy
        self._enable_rollback = enable_rollback
        self._extension_strategy = extension_strategy
        self._config_migrator = ConfigurationMigrator(merge_strategy)
        self._profiles_migrator = ProfilesMigrator(merge_strategy)
        self._snippets_migrator = SnippetsMigrator(merge_strategy)
        self._workspaces_migrator = WorkspacesMigrator()
        self._extensions_migrator = ExtensionsMigrator()
    @property
    def merge_strategy(self) -> str:
        return self._merge_strategy
    @property
    def enable_rollback(self) -> bool:
        return self._enable_rollback
    @property
    def extension_strategy(self) -> str:
        return self._extension_strategy
    def migrate(
        self,
        direction: str,
    ) -> MigrationResult:
        """
        Executa a migração completa na direção especificada.
        """
        if direction == self.VSCODE_TO_VSCODIUM:
            return self._execute_migration(
                source_editor="VSCode",
                target_editor="VSCodium",
                source_user_dir=VS_CODE_USER_DIR,
                target_user_dir=VSCODIUM_USER_DIR,
                source_extensions_dir=VS_CODE_EXTENSIONS_DIR,
                target_extensions_dir=VSCODIUM_EXTENSIONS_DIR,
            )
        elif direction == self.VSCODIUM_TO_VSCODE:
            return self._execute_migration(
                source_editor="VSCodium",
                target_editor="VSCode",
                source_user_dir=VSCODIUM_USER_DIR,
                target_user_dir=VS_CODE_USER_DIR,
                source_extensions_dir=VSCODIUM_EXTENSIONS_DIR,
                target_extensions_dir=VS_CODE_EXTENSIONS_DIR,
            )
        else:
            result = MigrationResult()
            result.add_error(f"Direção desconhecida: {direction}")
            return result
    def migrate_custom(
        self,
        source_editor: str,
        target_editor: str,
        source_user_dir: Path,
        target_user_dir: Path,
        source_extensions_dir: Path | None = None,
        target_extensions_dir: Path | None = None,
    ) -> MigrationResult:
        """
        Executa migração customizada.
        """
        return self._execute_migration(
            source_editor=source_editor,
            target_editor=target_editor,
            source_user_dir=source_user_dir,
            target_user_dir=target_user_dir,
            source_extensions_dir=source_extensions_dir,
            target_extensions_dir=target_extensions_dir,
        )
    # ─── Privados ──────────────────────────────────────────────────────
    def _execute_migration(
        self,
        source_editor: str,
        target_editor: str,
        source_user_dir: Path,
        target_user_dir: Path,
        source_extensions_dir: Path | None = None,
        target_extensions_dir: Path | None = None,
    ) -> MigrationResult:
        result = MigrationResult(
            source_editor=source_editor,
            target_editor=target_editor,
        )
        result.status = MigrationStatus.ANALYZING
        # Rollback
        rollback_manager = None
        if self._enable_rollback and target_user_dir.exists():
            rollback_manager = RollbackManager(target_user_dir)
        # 1. Configurações
        config_items = self._config_migrator.migrate(
            source_user_dir, target_user_dir,
        )
        for item in config_items:
            result.add_item(item)
        # 2. Snippets
        snippet_items = self._snippets_migrator.migrate(
            source_user_dir, target_user_dir,
        )
        for item in snippet_items:
            result.add_item(item)
        # 3. Profiles
        profile_items = self._profiles_migrator.migrate(
            source_user_dir / "User" / "profiles" if source_user_dir.exists() else Path("/nonexistent"),
            target_user_dir / "User" / "profiles" if target_user_dir.exists() else Path("/nonexistent"),
        )
        for item in profile_items:
            result.add_item(item)
        # 4. Workspaces
        ws_items = self._workspaces_migrator.migrate(
            source_user_dir, target_user_dir,
        )
        for item in ws_items:
            result.add_item(item)
        # 5. Extensões
        if source_extensions_dir and target_extensions_dir:
            ext_items = self._extensions_migrator.migrate_extensions(
                source_extensions_dir,
                target_extensions_dir,
                strategy=self._extension_strategy,
            )
            for item in ext_items:
                result.add_item(item)
        # Rollback plan
        if rollback_manager:
            plan = rollback_manager.create_plan(
                result.items,
                source_editor=source_editor,
                target_editor=target_editor,
            )
            result.rollback_available = True
            result.rollback_path = rollback_manager.rollback_directory
        # Finalização
        result.status = MigrationStatus.COMPLETED
        if result.failed_count > 0 and result.migrated_count == 0:
            result.status = MigrationStatus.FAILED
        result.finish()
        return result
###############################################################################
# END FILE
###############################################################################
