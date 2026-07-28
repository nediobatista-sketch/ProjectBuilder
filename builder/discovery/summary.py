###############################################################################
# ProjectBuilder
#
# EPIC.......: 004
# Sprint.....: 4.1
# Arquivo....: builder/discovery/summary.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Classe central que consolida todas as informações descobertas
#   pelos detectores do módulo Discovery.
#
###############################################################################
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from .statistics import DiscoveryStatistics
###############################################################################
@dataclass(slots=True)
class DiscoverySummary:
    """
    Consolidação de todas as informações descobertas
    durante o processo de Discovery.

    Cada detector recebe uma instância desta classe e
    popula os campos correspondentes ao seu domínio.
    """
    ###########################################################################
    # Meta-informação
    ###########################################################################
    started_at: datetime = field(
        default_factory=datetime.now,
    )
    finished_at: datetime | None = None
    duration: float = 0.0

    ###########################################################################
    # Ambiente
    ###########################################################################
    environment: dict[str, Any] = field(default_factory=dict)

    ###########################################################################
    # Sistema de arquivos
    ###########################################################################
    filesystem: dict[str, Path] = field(default_factory=dict)

    ###########################################################################
    # VS Code
    ###########################################################################
    vscode: dict[str, Any] = field(default_factory=dict)

    ###########################################################################
    # VSCodium
    ###########################################################################
    vscodium: dict[str, Any] = field(default_factory=dict)

    ###########################################################################
    # Pacotes e ferramentas
    ###########################################################################
    packages: dict[str, Any] = field(default_factory=dict)

    ###########################################################################
    # Python
    ###########################################################################
    python: dict[str, Any] = field(default_factory=dict)

    ###########################################################################
    # Extensões
    ###########################################################################
    extensions: list[dict[str, Any]] = field(default_factory=list)

    ###########################################################################
    # Perfis
    ###########################################################################
    profiles: list[dict[str, Any]] = field(default_factory=list)

    ###########################################################################
    # Configurações
    ###########################################################################
    settings: list[dict[str, Any]] = field(default_factory=list)

    ###########################################################################
    # Workspaces
    ###########################################################################
    workspaces: list[dict[str, Any]] = field(default_factory=list)

    ###########################################################################
    # Registro do Windows
    ###########################################################################
    registry: dict[str, Any] = field(default_factory=dict)

    ###########################################################################
    # Estatísticas
    ###########################################################################
    statistics: DiscoveryStatistics = field(
        default_factory=DiscoveryStatistics,
    )

    ###########################################################################
    # Finalização
    ###########################################################################
    def finish(self) -> None:
        """
        Finaliza o processo de Discovery e calcula
        métricas de tempo.
        """
        self.finished_at = datetime.now()
        if self.started_at:
            delta = self.finished_at - self.started_at
            self.duration = delta.total_seconds()

    ###########################################################################
    # Serialização
    ###########################################################################
    def to_dict(self) -> dict[str, Any]:
        """
        Converte o Summary para um dicionário
        serializável.
        """
        result: dict[str, Any] = {
            "started_at": str(self.started_at),
            "finished_at": str(self.finished_at),
            "duration": self.duration,
            "environment": self._serialize_dict(self.environment),
            "filesystem": {
                k: str(v) for k, v in self.filesystem.items()
            },
            "vscode": self._serialize_dict(self.vscode),
            "vscodium": self._serialize_dict(self.vscodium),
            "packages": self._serialize_dict(self.packages),
            "python": self._serialize_dict(self.python),
            "extensions": self._serialize_list(self.extensions),
            "profiles": self._serialize_list(self.profiles),
            "settings": self._serialize_list(self.settings),
            "workspaces": self._serialize_list(self.workspaces),
            "registry": self._serialize_dict(self.registry),
        }
        # Estatísticas
        stats = []
        for item in self.statistics.items:
            stats.append(
                {
                    "detector": item.detector,
                    "status": item.status,
                    "elapsed": item.elapsed,
                    "message": item.message,
                }
            )
        result["statistics"] = stats
        result["statistics_total"] = self.statistics.total
        result["statistics_success"] = self.statistics.success
        result["statistics_failed"] = self.statistics.failed
        return result

    ###########################################################################
    def _serialize_dict(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Converte valores Path para string.
        """
        result: dict[str, Any] = {}
        for key, value in data.items():
            if isinstance(value, Path):
                result[key] = str(value)
            elif isinstance(value, dict):
                result[key] = self._serialize_dict(value)
            elif isinstance(value, (list, tuple)):
                result[key] = self._serialize_list(list(value))
            else:
                result[key] = value
        return result

    ###########################################################################
    def _serialize_list(
        self,
        data: list[Any],
    ) -> list[Any]:
        """
        Converte itens da lista com Path para string.
        """
        result: list[Any] = []
        for item in data:
            if isinstance(item, dict):
                result.append(
                    {
                        k: str(v) if isinstance(v, Path) else v
                        for k, v in item.items()
                    }
                )
            elif isinstance(item, Path):
                result.append(str(item))
            else:
                result.append(item)
        return result

    ###########################################################################
    # Resumo textual
    ###########################################################################
    @property
    def summary_text(self) -> str:
        """
        Retorna um resumo textual do Discovery.
        """
        lines = [
            "=" * 60,
            "DISCOVERY REPORT",
            "=" * 60,
            "",
            f"Iniciado em : {self.started_at}",
            f"Finalizado em: {self.finished_at or 'N/A'}",
            f"Duração     : {self.duration:.4f}s",
            "",
            "── AMBIENTE ──────────────────────────────────────────",
            f"Plataforma  : {self.environment.get('platform', 'N/A')}",
            f"Release     : {self.environment.get('platform_release', 'N/A')}",
            f"Arquitetura : {self.environment.get('architecture', 'N/A')}",
            f"Usuário     : {self.environment.get('username', 'N/A')}",
            "",
            "── VS CODE ───────────────────────────────────────────",
            f"Instalação  : {self.vscode.get('installation', 'N/A')}",
            f"Usuário     : {self.vscode.get('user_data', 'N/A')}",
            f"Extensões   : {self.vscode.get('extensions', 'N/A')}",
            f"Perfis      : {self.vscode.get('profiles', 'N/A')}",
            "",
            "── VSCODIUM ──────────────────────────────────────────",
            f"Instalação  : {self.vscodium.get('installation', 'N/A')}",
            f"Usuário     : {self.vscodium.get('user_data', 'N/A')}",
            f"Extensões   : {self.vscodium.get('extensions', 'N/A')}",
            f"Perfis      : {self.vscodium.get('profiles', 'N/A')}",
            "",
            "── ESTATÍSTICAS ──────────────────────────────────────",
            f"Total       : {self.statistics.total}",
            f"Sucesso     : {self.statistics.success}",
            f"Falhas      : {self.statistics.failed}",
            "",
            "=" * 60,
        ]
        return "\n".join(lines)

    ###########################################################################
    def __repr__(self) -> str:
        return (
            f"DiscoverySummary("
            f"detectors={self.statistics.total}, "
            f"success={self.statistics.success}, "
            f"failed={self.statistics.failed})"
        )
###############################################################################
# END FILE
###############################################################################
