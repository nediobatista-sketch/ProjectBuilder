###############################################################################
# ProjectBuilder
#
# EPIC.......: 006
# Sprint.....: 6.3
# Arquivo....: builder/migration/extensions_migrator.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Migrador de extensões do VS Code e VSCodium.
#   Migra extensões instaladas, verificando compatibilidade.
#
###############################################################################
from __future__ import annotations
import json
import subprocess
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from .migration_result import MigrationItem, MigrationAction, MigrationStatus
@dataclass(slots=True)
class ExtensionInfo:
    """Informações de uma extensão."""
    publisher: str = ""
    name: str = ""
    version: str = ""
    display_name: str = ""
    description: str = ""
    source_path: Path | None = None
    full_id: str = ""
class ExtensionsMigrator:
    """
    Migração de extensões entre editores.
    Suporta:
        • Migração física de extensões
        • Geração de lista para reinstalação
        • Verificação de compatibilidade
    """
    def __init__(
        self,
        cli_tool: str = "",
    ) -> None:
        """
        Args:
            cli_tool: Caminho para o CLI do editor
                      (code ou codium).
        """
        self._cli_tool = cli_tool
    @property
    def cli_tool(self) -> str:
        return self._cli_tool
    def list_extensions(
        self,
        extensions_dir: Path,
    ) -> list[ExtensionInfo]:
        """
        Lista extensões instaladas no diretório.
        """
        extensions: list[ExtensionInfo] = []
        if not extensions_dir.exists():
            return extensions
        for ext_dir in sorted(extensions_dir.iterdir()):
            if not ext_dir.is_dir():
                continue
            info = self._read_extension_info(ext_dir)
            if info:
                extensions.append(info)
        return extensions
    def migrate_extensions(
        self,
        source_dir: Path,
        target_dir: Path,
        strategy: str = "list",
    ) -> list[MigrationItem]:
        """
        Migra extensões.
        Estratégias:
            • "list"     - gera lista de extensões para reinstalar
            • "copy"     - copia fisicamente as extensões
            • "reinstall"- usa o CLI para reinstalar
        """
        items: list[MigrationItem] = []
        extensions = self.list_extensions(source_dir)
        if not extensions:
            return items
        if strategy == "list":
            items = self._generate_install_list(extensions)
        elif strategy == "copy":
            items = self._copy_extensions(extensions, source_dir, target_dir)
        elif strategy == "reinstall":
            items = self._reinstall_extensions(extensions)
        return items
    def generate_install_script(
        self,
        extensions: list[ExtensionInfo],
        output: Path,
        cli_tool: str = "code",
    ) -> None:
        """
        Gera um script para reinstalar extensões.
        """
        lines = [
            "#!/bin/bash",
            f"# Script gerado pelo ProjectBuilder",
            f"# CLI Tool: {cli_tool}",
            "",
        ]
        for ext in extensions:
            full_id = ext.full_id or f"{ext.publisher}.{ext.name}"
            lines.append(f"{cli_tool} --install-extension {full_id}")
        output.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )
    def generate_install_commands(
        self,
        extensions: list[ExtensionInfo],
        cli_tool: str = "code",
    ) -> list[str]:
        """
        Gera comandos individuais para reinstalação.
        """
        commands = []
        for ext in extensions:
            full_id = ext.full_id or f"{ext.publisher}.{ext.name}"
            commands.append(
                f"{cli_tool} --install-extension {full_id}"
            )
        return commands
    def _read_extension_info(
        self,
        directory: Path,
    ) -> ExtensionInfo | None:
        package = directory / "package.json"
        if not package.exists():
            return None
        try:
            manifest = json.loads(
                package.read_text(encoding="utf-8")
            )
        except Exception:
            return None
        publisher = manifest.get("publisher", "")
        name = manifest.get("name", directory.name)
        return ExtensionInfo(
            publisher=publisher,
            name=name,
            version=manifest.get("version", ""),
            display_name=manifest.get("displayName", name),
            description=manifest.get("description", ""),
            source_path=directory,
            full_id=f"{publisher}.{name}",
        )
    def _generate_install_list(
        self,
        extensions: list[ExtensionInfo],
    ) -> list[MigrationItem]:
        items: list[MigrationItem] = []
        for ext in extensions:
            item = MigrationItem(
                name=ext.full_id or ext.name,
                category="Extensions",
                source=ext.source_path,
                action=MigrationAction.CREATE,
            )
            item.size = self._dir_size(ext.source_path) if ext.source_path else 0
            item.migrated = True
            item.status = MigrationStatus.COMPLETED
            item.error = f"Lista gerada: {ext.full_id}"
            items.append(item)
        return items
    def _copy_extensions(
        self,
        extensions: list[ExtensionInfo],
        source_dir: Path,
        target_dir: Path,
    ) -> list[MigrationItem]:
        items: list[MigrationItem] = []
        target_dir.mkdir(parents=True, exist_ok=True)
        for ext in extensions:
            item = MigrationItem(
                name=ext.full_id or ext.name,
                category="Extensions",
                source=ext.source_path,
                destination=target_dir / ext.name,
                action=MigrationAction.COPY,
            )
            if ext.source_path and ext.source_path.exists():
                item.source_exists = True
                try:
                    shutil.copytree(
                        ext.source_path,
                        target_dir / ext.name,
                        dirs_exist_ok=True,
                    )
                    item.migrated = True
                    item.status = MigrationStatus.COMPLETED
                except Exception as e:
                    item.error = str(e)
                    item.status = MigrationStatus.FAILED
            items.append(item)
        return items
    def _reinstall_extensions(
        self,
        extensions: list[ExtensionInfo],
    ) -> list[MigrationItem]:
        items: list[MigrationItem] = []
        cli = self._cli_tool or shutil.which("code") or shutil.which("codium")
        if not cli:
            for ext in extensions:
                items.append(MigrationItem(
                    name=ext.full_id or ext.name,
                    category="Extensions",
                    status=MigrationStatus.FAILED,
                    error="CLI do editor não encontrado",
                ))
            return items
        for ext in extensions:
            item = MigrationItem(
                name=ext.full_id or ext.name,
                category="Extensions",
                action=MigrationAction.CREATE,
            )
            try:
                full_id = ext.full_id or f"{ext.publisher}.{ext.name}"
                result = subprocess.run(
                    [cli, "--install-extension", full_id],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if result.returncode == 0:
                    item.migrated = True
                    item.status = MigrationStatus.COMPLETED
                else:
                    item.error = result.stderr.strip() or result.stdout.strip()
                    item.status = MigrationStatus.FAILED
            except subprocess.TimeoutExpired:
                item.error = "Timeout na instalação"
                item.status = MigrationStatus.FAILED
            except Exception as e:
                item.error = str(e)
                item.status = MigrationStatus.FAILED
            items.append(item)
        return items
    @staticmethod
    def _dir_size(path: Path | None) -> int:
        if not path or not path.exists():
            return 0
        total = 0
        for file in path.rglob("*"):
            if file.is_file():
                total += file.stat().st_size
        return total
###############################################################################
# END FILE
###############################################################################
