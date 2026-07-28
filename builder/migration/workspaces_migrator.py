###############################################################################
# ProjectBuilder
#
# EPIC.......: 006
# Sprint.....: 6.6
# Arquivo....: builder/migration/workspaces_migrator.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Migrador de Workspaces do VS Code e VSCodium.
#
###############################################################################
from __future__ import annotations
import json
import shutil
from pathlib import Path
from typing import Any
from .migration_result import MigrationItem, MigrationAction, MigrationStatus
class WorkspacesMigrator:
    """
    Migração de Workspaces.
    """
    def __init__(
        self,
        remap_paths: bool = True,
    ) -> None:
        """
        Args:
            remap_paths: Se True, tenta remapear caminhos
                         de projetos entre sistemas.
        """
        self._remap_paths = remap_paths
    @property
    def remap_paths(self) -> bool:
        return self._remap_paths
    def migrate(
        self,
        source_user_dir: Path,
        target_user_dir: Path,
    ) -> list[MigrationItem]:
        """
        Migra workspaces armazenados.
        """
        items: list[MigrationItem] = []
        source_ws = source_user_dir / "User" / "workspaceStorage"
        target_ws = target_user_dir / "User" / "workspaceStorage"
        if not source_ws.exists():
            items.append(MigrationItem(
                name="workspaceStorage",
                category="Workspaces",
                source=source_ws,
                destination=target_ws,
                status=MigrationStatus.SKIPPED,
                error="workspaceStorage não encontrado na origem",
            ))
            return items
        target_ws.mkdir(parents=True, exist_ok=True)
        # Workspace storage (state)
        for ws_dir in sorted(source_ws.iterdir()):
            if not ws_dir.is_dir():
                continue
            target_dir = target_ws / ws_dir.name
            item = MigrationItem(
                name=f"workspace/{ws_dir.name}",
                category="Workspaces",
                source=ws_dir,
                destination=target_dir,
                action=MigrationAction.COPY,
            )
            item.source_exists = True
            item.size = self._dir_size(ws_dir)
            try:
                shutil.copytree(ws_dir, target_dir, dirs_exist_ok=True)
                item.migrated = True
                item.status = MigrationStatus.COMPLETED
            except Exception as e:
                item.error = str(e)
                item.status = MigrationStatus.FAILED
            items.append(item)
        # Global storage
        source_global = source_user_dir / "User" / "globalStorage"
        target_global = target_user_dir / "User" / "globalStorage"
        if source_global.exists():
            target_global.mkdir(parents=True, exist_ok=True)
            for ws_dir in sorted(source_global.iterdir()):
                if not ws_dir.is_dir():
                    continue
                target_dir = target_global / ws_dir.name
                item = MigrationItem(
                    name=f"globalStorage/{ws_dir.name}",
                    category="Workspaces",
                    source=ws_dir,
                    destination=target_dir,
                    action=MigrationAction.COPY,
                )
                item.source_exists = True
                item.size = self._dir_size(ws_dir)
                try:
                    shutil.copytree(ws_dir, target_dir, dirs_exist_ok=True)
                    item.migrated = True
                    item.status = MigrationStatus.COMPLETED
                except Exception as e:
                    item.error = str(e)
                    item.status = MigrationStatus.FAILED
                items.append(item)
        # Arquivos .code-workspace na origem
        source_code_workspaces = list(source_user_dir.glob("*.code-workspace"))
        for ws_file in source_code_workspaces:
            target_file = target_user_dir / ws_file.name
            item = MigrationItem(
                name=ws_file.name,
                category="Workspaces",
                source=ws_file,
                destination=target_file,
                action=MigrationAction.COPY,
            )
            item.source_exists = True
            item.size = ws_file.stat().st_size
            try:
                shutil.copy2(ws_file, target_file)
                if self._remap_paths:
                    self._remap_workspace_paths(target_file)
                item.migrated = True
                item.status = MigrationStatus.COMPLETED
            except Exception as e:
                item.error = str(e)
                item.status = MigrationStatus.FAILED
            items.append(item)
        return items
    def _remap_workspace_paths(self, workspace_file: Path) -> None:
        """
        Tenta remapear caminhos absolutos em um
        arquivo .code-workspace.
        """
        if not workspace_file.exists():
            return
        try:
            content = workspace_file.read_text(encoding="utf-8")
            data = json.loads(content)
            folders = data.get("folders", [])
            for folder in folders:
                uri = folder.get("path", "")
                # Verifica se é um caminho absoluto
                p = Path(uri)
                if p.is_absolute() and not p.exists():
                    # Tenta encontrar o diretório no novo sistema
                    if p.name and Path.cwd().parent.parent.exists():
                        pass  # Mantém o path original por enquanto
            workspace_file.write_text(
                json.dumps(data, indent=4, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception:
            pass
    @staticmethod
    def _dir_size(path: Path) -> int:
        total = 0
        for file in path.rglob("*"):
            if file.is_file():
                total += file.stat().st_size
        return total
###############################################################################
# END FILE
###############################################################################
