###############################################################################
# ProjectBuilder
#
# EPIC.......: 005
# Sprint.....: 5.1
# Arquivo....: builder/backup/backup_engine.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Motor principal de Backup do ProjectBuilder.
#   Coordena todas as operações de backup, compressão,
#   versionamento e verificação de integridade.
#
###############################################################################
from __future__ import annotations
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any
from .backup_result import BackupResult, BackupStatus, BackupItem
from .compressor import BackupCompressor
from .integrity import IntegrityVerifier, IntegrityManifest
from .versioner import BackupVersioner
###############################################################################
# Diretórios padrão do VS Code e VSCodium
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
class BackupEngine:
    """
    Motor principal de Backup.
    Gerencia o ciclo completo de backup do VS Code
    e VSCodium.
    """
    def __init__(
        self,
        backup_directory: Path | None = None,
        format: str = BackupCompressor.FORMAT_ZIP,
    ) -> None:
        self._backup_dir = (
            backup_directory
            or Path.cwd() / "backups"
        )
        self._compressor = BackupCompressor(
            default_format=format,
        )
        self._verifier = IntegrityVerifier()
        self._versioner = BackupVersioner(self._backup_dir)
    @property
    def backup_directory(self) -> Path:
        return self._backup_dir
    @property
    def compressor(self) -> BackupCompressor:
        return self._compressor
    @property
    def verifier(self) -> IntegrityVerifier:
        return self._verifier
    @property
    def versioner(self) -> BackupVersioner:
        return self._versioner
    # ─── Backup do VS Code ─────────────────────────────────────────────
    def backup_vscode(self) -> BackupResult:
        """
        Executa backup completo do VS Code.
        """
        return self._backup_editor(
            editor="VSCode",
            user_dir=VS_CODE_USER_DIR,
            extensions_dir=VS_CODE_EXTENSIONS_DIR,
        )
    # ─── Backup do VSCodium ────────────────────────────────────────────
    def backup_vscodium(self) -> BackupResult:
        """
        Executa backup completo do VSCodium.
        """
        return self._backup_editor(
            editor="VSCodium",
            user_dir=VSCODIUM_USER_DIR,
            extensions_dir=VSCODIUM_EXTENSIONS_DIR,
        )
    # ─── Backup genérico ───────────────────────────────────────────────
    def backup_editor(
        self,
        editor: str,
        user_dir: Path,
        extensions_dir: Path,
    ) -> BackupResult:
        """
        Executa backup de um editor específico.
        """
        return self._backup_editor(
            editor=editor,
            user_dir=user_dir,
            extensions_dir=extensions_dir,
        )
    # ─── Backup customizado ────────────────────────────────────────────
    def backup_custom(
        self,
        name: str,
        directories: list[Path],
    ) -> BackupResult:
        """
        Executa backup de diretórios customizados.
        """
        result = BackupResult(editor=name)
        result.status = BackupStatus.CREATED
        self._backup_dir.mkdir(parents=True, exist_ok=True)
        for dir_path in directories:
            item = self._backup_item(
                name=dir_path.name,
                source=dir_path,
                result=result,
            )
            result.add_item(item)
        self._finalize_backup(result)
        return result
    # ─── Restauração ───────────────────────────────────────────────────
    def restore(
        self,
        editor: str,
        destination: Path | None = None,
    ) -> Any:
        """
        Restaura o backup mais recente de um editor.
        """
        from .restorer import BackupRestorer
        restorer = BackupRestorer(self._compressor)
        versions = self._versioner.list_versions()
        editor_versions = [
            v for v in versions
            if v.editor == editor
        ]
        if not editor_versions:
            raise FileNotFoundError(
                f"Nenhum backup encontrado para {editor}"
            )
        latest = editor_versions[0]
        if latest.archive_path is None:
            raise FileNotFoundError(
                "Arquivo de backup não encontrado"
            )
        target = destination or self._get_editor_dir(editor)
        return restorer.restore_directory(
            latest.archive_path,
            target,
            editor=editor,
        )
    # ─── Lista de backups ──────────────────────────────────────────────
    def list_backups(self, editor: str = "") -> list[dict[str, Any]]:
        """
        Lista todos os backups disponíveis.
        """
        versions = self._versioner.list_versions()
        if editor:
            versions = [
                v for v in versions if v.editor == editor
            ]
        return [
            {
                "number": v.number,
                "editor": v.editor,
                "timestamp": str(v.timestamp),
                "size": v.size,
                "checksum": v.checksum,
                "archive": str(v.archive_path) if v.archive_path else None,
            }
            for v in versions
        ]
    # ─── Privados ──────────────────────────────────────────────────────
    def _backup_editor(
        self,
        editor: str,
        user_dir: Path,
        extensions_dir: Path,
    ) -> BackupResult:
        result = BackupResult(editor=editor)
        result.status = BackupStatus.CREATED
        self._backup_dir.mkdir(parents=True, exist_ok=True)
        # Itens do backup
        backup_items = [
            ("User Settings", user_dir),
            ("Extensions", extensions_dir),
        ]
        for name, dir_path in backup_items:
            item = self._backup_item(
                name=name,
                source=dir_path,
                result=result,
            )
            result.add_item(item)
        self._finalize_backup(result)
        return result
    def _backup_item(
        self,
        name: str,
        source: Path,
        result: BackupResult,
    ) -> BackupItem:
        item = BackupItem(
            name=name,
            source=source,
        )
        if source.exists():
            item.exists = True
            item.size = self._dir_size(source)
            # Copia para diretório de backup
            temp_backup = (
                self._backup_dir
                / result.editor
                / f"temp_{name.lower().replace(' ', '_')}"
            )
            temp_backup.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(
                    source, temp_backup,
                    dirs_exist_ok=True,
                )
            else:
                shutil.copy2(source, temp_backup)
            item.backup_path = temp_backup
            item.backed_up = True
        else:
            item.error = f"Diretório não encontrado: {source}"
        return item
    def _finalize_backup(self, result: BackupResult) -> None:
        """
        Finaliza o backup: compressão, versionamento
        e verificação de integridade.
        """
        result.status = BackupStatus.COMPRESSING
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{result.editor}_backup_{timestamp}"
        archive_path = self._backup_dir / archive_name
        # Compressão
        temp_editor_dir = self._backup_dir / result.editor
        if temp_editor_dir.exists():
            comp_result = self._compressor.compress_directory(
                temp_editor_dir, archive_path,
            )
            if comp_result.success:
                result.archive_path = comp_result.archive
                result.total_size = comp_result.original_size
                result.compressed_size = comp_result.compressed_size
            else:
                result.add_error(comp_result.error)
        # Limpar temporários
        if temp_editor_dir.exists():
            shutil.rmtree(temp_editor_dir, ignore_errors=True)
        result.status = BackupStatus.VERSIONED
        # Versionamento
        checksum = ""
        if result.archive_path and result.archive_path.exists():
            checksum = self._verifier.compute_hash(
                result.archive_path,
            )
            result.checksum = checksum
            self._versioner.version(
                archive_path=result.archive_path,
                editor=result.editor,
                checksum=checksum,
                description=f"Backup {result.editor} - {timestamp}",
            )
        result.status = BackupStatus.VERIFIED
        result.finish()
    def _get_editor_dir(self, editor: str) -> Path:
        if editor.lower() == "vscode":
            return VS_CODE_USER_DIR
        elif editor.lower() == "vscodium":
            return VSCODIUM_USER_DIR
        raise ValueError(f"Editor desconhecido: {editor}")
    @staticmethod
    def _dir_size(path: Path) -> int:
        total = 0
        if path.is_dir():
            for file in path.rglob("*"):
                if file.is_file():
                    total += file.stat().st_size
        elif path.is_file():
            total = path.stat().st_size
        return total
###############################################################################
# END FILE
###############################################################################
