###############################################################################
# ProjectBuilder
#
# EPIC.......: 010
# Sprint.....: 10.2
# Arquivo....: builder/installer/packager.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Empacotador do ProjectBuilder.
#   Cria pacotes distribuíveis (wheel, sdist, exe).
#
###############################################################################
from __future__ import annotations
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
@dataclass(slots=True)
class PackageResult:
    """Resultado do empacotamento."""
    success: bool = False
    package_path: Path | None = None
    package_type: str = ""
    size: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    errors: list[str] = field(default_factory=list)
class Packager:
    """
    Empacotador do ProjectBuilder.
    Cria pacotes distribuíveis.
    """
    TYPE_WHEEL = "wheel"
    TYPE_SDIST = "sdist"
    TYPE_EXE = "exe"
    def __init__(
        self,
        project_dir: Path | None = None,
        output_dir: Path | None = None,
    ) -> None:
        self._project_dir = project_dir or Path.cwd()
        self._output_dir = output_dir or self._project_dir / "dist"
    @property
    def project_dir(self) -> Path:
        return self._project_dir
    @property
    def output_dir(self) -> Path:
        return self._output_dir
    def build_wheel(self) -> PackageResult:
        """Constrói um pacote wheel."""
        return self._build(self.TYPE_WHEEL)
    def build_sdist(self) -> PackageResult:
        """Constrói um pacote sdist."""
        return self._build(self.TYPE_SDIST)
    def build_all(self) -> list[PackageResult]:
        """Constrói todos os pacotes."""
        results = []
        for pkg_type in [self.TYPE_WHEEL, self.TYPE_SDIST]:
            results.append(self._build(pkg_type))
        return results
    def build_exe(self) -> PackageResult:
        """
        Converte em executável (requer PyInstaller).
        """
        result = PackageResult(package_type=self.TYPE_EXE)
        try:
            subprocess.run(
                [sys.executable, "-m", "PyInstaller",
                 "--onefile", "--name", "projectbuilder",
                 str(self._project_dir / "builder" / "cli" / "main.py")],
                capture_output=True, text=True, timeout=600,
                cwd=str(self._project_dir),
            )
            exe_path = self._project_dir / "dist" / "projectbuilder.exe"
            if not exe_path.exists():
                exe_path = self._project_dir / "dist" / "projectbuilder"
            if exe_path.exists():
                result.success = True
                result.package_path = exe_path
                result.size = exe_path.stat().st_size
            else:
                result.errors.append("PyInstaller não produziu executável")
        except FileNotFoundError:
            result.errors.append("PyInstaller não instalado")
        except subprocess.TimeoutExpired:
            result.errors.append("Timeout no empacotamento")
        except Exception as e:
            result.errors.append(str(e))
        return result
    def _build(self, package_type: str) -> PackageResult:
        result = PackageResult(package_type=package_type)
        self._output_dir.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(
                [sys.executable, "-m", "build",
                 "--outdir", str(self._output_dir),
                 "--" + package_type],
                capture_output=True, text=True, timeout=300,
                cwd=str(self._project_dir),
            )
            # Procura o pacote gerado
            for f in sorted(self._output_dir.iterdir(), reverse=True):
                if package_type == self.TYPE_WHEEL and f.suffix == ".whl":
                    result.package_path = f
                    result.size = f.stat().st_size
                    break
                elif package_type == self.TYPE_SDIST and ".tar.gz" in f.name:
                    result.package_path = f
                    result.size = f.stat().st_size
                    break
            if result.package_path:
                result.success = True
            else:
                result.errors.append(
                    f"Nenhum pacote {package_type} encontrado"
                )
        except subprocess.TimeoutExpired:
            result.errors.append("Timeout na construção")
        except Exception as e:
            result.errors.append(str(e))
        return result
###############################################################################
# END FILE
###############################################################################
