###############################################################################
# ProjectBuilder
#
# EPIC.......: 010
# Sprint.....: 10.1
# Arquivo....: builder/installer/installer.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Instalador do ProjectBuilder.
#   Gerencia instalação, atualização e desinstalação.
#
###############################################################################
from __future__ import annotations
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
@dataclass(slots=True)
class InstallResult:
    """Resultado da instalação."""
    success: bool = False
    installed_version: str = ""
    install_path: Path | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
class Installer:
    """
    Instalador do ProjectBuilder.
    Suporta instalação via pip, standalone e portable.
    """
    MODE_PIP = "pip"
    MODE_STANDALONE = "standalone"
    MODE_PORTABLE = "portable"
    def __init__(
        self,
        install_path: Path | None = None,
    ) -> None:
        self._install_path = (
            install_path
            or Path(sys.prefix) / "Lib" / "site-packages" / "projectbuilder"
        )
    @property
    def install_path(self) -> Path:
        return self._install_path
    def install(
        self,
        mode: str = MODE_PIP,
    ) -> InstallResult:
        """
        Instala o ProjectBuilder.
        """
        result = InstallResult()
        if mode == self.MODE_PIP:
            return self._install_pip(result)
        elif mode == self.MODE_STANDALONE:
            return self._install_standalone(result)
        elif mode == self.MODE_PORTABLE:
            return self._install_portable(result)
        else:
            result.errors.append(f"Modo desconhecido: {mode}")
            return result
    def update(self) -> InstallResult:
        """
        Atualiza o ProjectBuilder.
        """
        return self.install(mode=self.MODE_PIP)
    def uninstall(self) -> InstallResult:
        """
        Desinstala o ProjectBuilder.
        """
        result = InstallResult()
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "uninstall",
                 "-y", "projectbuilder"],
                capture_output=True, text=True, timeout=120,
            )
            result.success = True
            result.installed_version = "removed"
        except Exception as e:
            result.errors.append(str(e))
        return result
    def is_installed(self) -> bool:
        """
        Verifica se o ProjectBuilder está instalado.
        """
        try:
            from builder import __version__
            return True
        except ImportError:
            return False
    def get_version(self) -> str:
        """
        Retorna a versão instalada.
        """
        try:
            from builder import __version__
            return __version__
        except ImportError:
            return "not installed"
    # ─── Privados ──────────────────────────────────────────────────────
    def _install_pip(self, result: InstallResult) -> InstallResult:
        try:
            project_dir = self._find_project_dir()
            if project_dir:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install",
                     "-e", str(project_dir)],
                    capture_output=True, text=True, timeout=300,
                )
            result.success = True
            result.install_path = self._install_path
        except subprocess.TimeoutExpired:
            result.errors.append("Timeout na instalação pip")
        except Exception as e:
            result.errors.append(str(e))
        return result
    def _install_standalone(self, result: InstallResult) -> InstallResult:
        self._install_path.mkdir(parents=True, exist_ok=True)
        project_dir = self._find_project_dir()
        if project_dir:
            # Copia os arquivos do projeto
            for item in ["builder", "pyproject.toml"]:
                src = project_dir / item
                dst = self._install_path / item
                if src.exists():
                    if src.is_dir():
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, dst)
            result.success = True
            result.install_path = self._install_path
        else:
            result.errors.append("Diretório do projeto não encontrado")
        return result
    def _install_portable(self, result: InstallResult) -> InstallResult:
        portable_dir = self._install_path / "portable"
        portable_dir.mkdir(parents=True, exist_ok=True)
        result.success = True
        result.install_path = portable_dir
        return result
    def _find_project_dir(self) -> Path | None:
        """Encontra o diretório raiz do projeto."""
        candidates = [
            Path(__file__).parent.parent.parent,
            Path.cwd(),
            Path.cwd() / "..",
        ]
        for candidate in candidates:
            pyproject = candidate / "pyproject.toml"
            if pyproject.exists():
                return candidate
        return None
###############################################################################
# END FILE
###############################################################################
