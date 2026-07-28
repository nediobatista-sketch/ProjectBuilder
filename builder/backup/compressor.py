###############################################################################
# ProjectBuilder
#
# EPIC.......: 005
# Sprint.....: 5.3
# Arquivo....: builder/backup/compressor.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Compressão de backups do VS Code e VSCodium.
#   Suporta formatos ZIP e TAR.GZ.
#
###############################################################################
from __future__ import annotations
import gzip
import shutil
import tarfile
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
@dataclass(slots=True)
class CompressionResult:
    """Resultado da compressão."""
    source: Path
    archive: Path
    format: str
    original_size: int = 0
    compressed_size: int = 0
    elapsed: float = 0.0
    success: bool = False
    error: str = ""
    @property
    def ratio(self) -> float:
        if self.original_size == 0:
            return 0.0
        return self.compressed_size / self.original_size
class BackupCompressor:
    """
    Compressão de backups.
    Suporta os formatos:
        • ZIP
        • TAR.GZ
    """
    FORMAT_ZIP = "zip"
    FORMAT_TARGZ = "tar.gz"
    SUPPORTED_FORMATS = {
        FORMAT_ZIP,
        FORMAT_TARGZ,
    }
    def __init__(
        self,
        default_format: str = FORMAT_ZIP,
    ) -> None:
        if default_format not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Formato não suportado: {default_format}"
            )
        self._format = default_format
    @property
    def format(self) -> str:
        return self._format
    @format.setter
    def format(self, value: str) -> None:
        if value not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Formato não suportado: {value}"
            )
        self._format = value
    def compress_directory(
        self,
        source: Path,
        destination: Path,
    ) -> CompressionResult:
        """
        Comprime um diretório inteiro.
        """
        result = CompressionResult(
            source=source,
            archive=destination,
            format=self._format,
        )
        if not source.exists():
            result.error = f"Diretório não encontrado: {source}"
            return result
        if self._format == self.FORMAT_ZIP:
            return self._compress_zip(source, destination, result)
        elif self._format == self.FORMAT_TARGZ:
            return self._compress_targz(source, destination, result)
        return result
    def compress_file(
        self,
        source: Path,
        destination: Path,
    ) -> CompressionResult:
        """
        Comprime um arquivo individual.
        """
        result = CompressionResult(
            source=source,
            archive=destination,
            format=self._format,
        )
        if not source.exists():
            result.error = f"Arquivo não encontrado: {source}"
            return result
        if self._format == self.FORMAT_ZIP:
            return self._compress_single_zip(source, destination, result)
        elif self._format == self.FORMAT_TARGZ:
            return self._compress_single_targz(source, destination, result)
        return result
    def decompress(
        self,
        archive: Path,
        destination: Path,
    ) -> CompressionResult:
        """
        Descomprime um arquivo de backup.
        """
        result = CompressionResult(
            source=archive,
            archive=destination,
            format=self._format,
        )
        if not archive.exists():
            result.error = f"Arquivo não encontrado: {archive}"
            return result
        if self._format == self.FORMAT_ZIP:
            return self._decompress_zip(archive, destination, result)
        elif self._format == self.FORMAT_TARGZ:
            return self._decompress_targz(archive, destination, result)
        return result
    # ─── ZIP ───────────────────────────────────────────────────────────
    def _compress_zip(
        self,
        source: Path,
        destination: Path,
        result: CompressionResult,
    ) -> CompressionResult:
        from time import perf_counter
        start = perf_counter()
        try:
            archive = destination
            if not archive.suffix:
                archive = destination.with_suffix(".zip")
            if archive.suffix != ".zip":
                archive = destination.with_suffix(".zip")
            destination.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(
                archive,
                "w",
                zipfile.ZIP_DEFLATED,
            ) as zf:
                for file in source.rglob("*"):
                    if file.is_file():
                        arcname = file.relative_to(source.parent)
                        zf.write(file, arcname)
            result.archive = archive
            result.original_size = self._dir_size(source)
            result.compressed_size = archive.stat().st_size
            result.elapsed = perf_counter() - start
            result.success = True
        except Exception as e:
            result.error = str(e)
            result.elapsed = perf_counter() - start
        return result
    def _compress_single_zip(
        self,
        source: Path,
        destination: Path,
        result: CompressionResult,
    ) -> CompressionResult:
        from time import perf_counter
        start = perf_counter()
        try:
            archive = destination
            if not archive.suffix:
                archive = destination.with_suffix(".zip")
            destination.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(
                archive,
                "w",
                zipfile.ZIP_DEFLATED,
            ) as zf:
                zf.write(source, source.name)
            result.archive = archive
            result.original_size = source.stat().st_size
            result.compressed_size = archive.stat().st_size
            result.elapsed = perf_counter() - start
            result.success = True
        except Exception as e:
            result.error = str(e)
            result.elapsed = perf_counter() - start
        return result
    def _decompress_zip(
        self,
        archive: Path,
        destination: Path,
        result: CompressionResult,
    ) -> CompressionResult:
        from time import perf_counter
        start = perf_counter()
        try:
            destination.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(archive, "r") as zf:
                zf.extractall(destination)
            result.elapsed = perf_counter() - start
            result.success = True
        except Exception as e:
            result.error = str(e)
            result.elapsed = perf_counter() - start
        return result
    # ─── TAR.GZ ────────────────────────────────────────────────────────
    def _compress_targz(
        self,
        source: Path,
        destination: Path,
        result: CompressionResult,
    ) -> CompressionResult:
        from time import perf_counter
        start = perf_counter()
        try:
            archive = destination
            if not archive.suffixes or ".tar.gz" not in "".join(archive.suffixes):
                archive = destination.with_name(
                    destination.name + ".tar.gz"
                )
            destination.parent.mkdir(parents=True, exist_ok=True)
            with tarfile.open(archive, "w:gz") as tf:
                tf.add(source, arcname=source.name)
            result.archive = archive
            result.original_size = self._dir_size(source)
            result.compressed_size = archive.stat().st_size
            result.elapsed = perf_counter() - start
            result.success = True
        except Exception as e:
            result.error = str(e)
            result.elapsed = perf_counter() - start
        return result
    def _compress_single_targz(
        self,
        source: Path,
        destination: Path,
        result: CompressionResult,
    ) -> CompressionResult:
        from time import perf_counter
        start = perf_counter()
        try:
            archive = destination
            if not archive.suffixes or ".tar.gz" not in "".join(archive.suffixes):
                archive = destination.with_name(
                    destination.name + ".tar.gz"
                )
            destination.parent.mkdir(parents=True, exist_ok=True)
            with tarfile.open(archive, "w:gz") as tf:
                tf.add(source, arcname=source.name)
            result.archive = archive
            result.original_size = source.stat().st_size
            result.compressed_size = archive.stat().st_size
            result.elapsed = perf_counter() - start
            result.success = True
        except Exception as e:
            result.error = str(e)
            result.elapsed = perf_counter() - start
        return result
    def _decompress_targz(
        self,
        archive: Path,
        destination: Path,
        result: CompressionResult,
    ) -> CompressionResult:
        from time import perf_counter
        start = perf_counter()
        try:
            destination.mkdir(parents=True, exist_ok=True)
            with tarfile.open(archive, "r:gz") as tf:
                tf.extractall(destination)
            result.elapsed = perf_counter() - start
            result.success = True
        except Exception as e:
            result.error = str(e)
            result.elapsed = perf_counter() - start
        return result
    # ─── Utilidades ────────────────────────────────────────────────────
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
