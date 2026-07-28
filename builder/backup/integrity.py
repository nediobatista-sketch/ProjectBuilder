###############################################################################
# ProjectBuilder
#
# EPIC.......: 005
# Sprint.....: 5.4
# Arquivo....: builder/backup/integrity.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Verificação de integridade dos backups.
#   Utiliza hashes SHA-256 para garantir a integridade
#   dos arquivos de backup.
#
###############################################################################
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
@dataclass(slots=True)
class IntegrityReport:
    """Relatório de integridade de um arquivo."""
    path: Path
    expected_hash: str = ""
    actual_hash: str = ""
    valid: bool = False
    size: int = 0
    checked_at: datetime = field(default_factory=datetime.now)
    error: str = ""
@dataclass(slots=True)
class IntegrityManifest:
    """
    Manifesto de integridade.
    Armazena os hashes de todos os arquivos do backup.
    """
    editor: str = ""
    version: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    files: list[IntegrityReport] = field(default_factory=list)
    def add_file(
        self,
        report: IntegrityReport,
    ) -> None:
        self.files.append(report)
    def to_dict(self) -> dict[str, Any]:
        return {
            "editor": self.editor,
            "version": self.version,
            "created_at": str(self.created_at),
            "files": [
                {
                    "path": str(r.path),
                    "expected_hash": r.expected_hash,
                    "actual_hash": r.actual_hash,
                    "valid": r.valid,
                    "size": r.size,
                    "checked_at": str(r.checked_at),
                    "error": r.error,
                }
                for r in self.files
            ],
        }
class IntegrityVerifier:
    """
    Verificação de integridade de backups.
    """
    ALGORITHM = "sha256"
    MANIFEST_FILENAME = "integrity.json"
    def __init__(
        self,
        algorithm: str = "sha256",
    ) -> None:
        self._algorithm = algorithm
    @property
    def algorithm(self) -> str:
        return self._algorithm
    def compute_hash(
        self,
        path: Path,
    ) -> str:
        """
        Calcula o hash SHA-256 de um arquivo.
        """
        h = hashlib.new(self._algorithm)
        with path.open("rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    def create_manifest(
        self,
        directory: Path,
        editor: str = "",
        version: str = "",
    ) -> IntegrityManifest:
        """
        Cria um manifesto de integridade para todos
        os arquivos de um diretório.
        """
        manifest = IntegrityManifest(
            editor=editor,
            version=version,
        )
        if not directory.exists():
            return manifest
        for file in sorted(directory.rglob("*")):
            if file.is_file():
                report = IntegrityReport(
                    path=file,
                    expected_hash=self.compute_hash(file),
                    actual_hash="",
                    valid=True,
                    size=file.stat().st_size,
                )
                manifest.add_file(report)
        return manifest
    def verify_manifest(
        self,
        directory: Path,
        manifest: IntegrityManifest,
    ) -> IntegrityManifest:
        """
        Verifica a integridade de todos os arquivos
        contra o manifesto.
        """
        verified = IntegrityManifest(
            editor=manifest.editor,
            version=manifest.version,
            created_at=datetime.now(),
        )
        for report in manifest.files:
            file = directory / report.path
            if not file.exists():
                verified.add_file(IntegrityReport(
                    path=report.path,
                    expected_hash=report.expected_hash,
                    valid=False,
                    error="Arquivo não encontrado",
                ))
                continue
            actual = self.compute_hash(file)
            verified.add_file(IntegrityReport(
                path=report.path,
                expected_hash=report.expected_hash,
                actual_hash=actual,
                valid=actual == report.expected_hash,
                size=file.stat().st_size,
            ))
        return verified
    def save_manifest(
        self,
        manifest: IntegrityManifest,
        destination: Path,
    ) -> None:
        """
        Salva o manifesto de integridade em JSON.
        """
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(
                manifest.to_dict(),
                indent=4,
                ensure_ascii=False,
                default=str,
            ),
            encoding="utf-8",
        )
    def load_manifest(
        self,
        path: Path,
    ) -> IntegrityManifest | None:
        """
        Carrega um manifesto de integridade do disco.
        """
        if not path.exists():
            return None
        try:
            data = json.loads(
                path.read_text(encoding="utf-8")
            )
            manifest = IntegrityManifest(
                editor=data.get("editor", ""),
                version=data.get("version", ""),
                created_at=datetime.fromisoformat(
                    data.get("created_at", "")
                ),
            )
            for file_data in data.get("files", []):
                manifest.add_file(IntegrityReport(
                    path=Path(file_data.get("path", "")),
                    expected_hash=file_data.get("expected_hash", ""),
                    actual_hash=file_data.get("actual_hash", ""),
                    valid=file_data.get("valid", False),
                    size=file_data.get("size", 0),
                    error=file_data.get("error", ""),
                ))
            return manifest
        except Exception:
            return None
    @property
    def summary(self) -> str:
        """Resumo do verificador."""
        return (
            f"IntegrityVerifier("
            f"algorithm={self._algorithm})"
        )
###############################################################################
# END FILE
###############################################################################
