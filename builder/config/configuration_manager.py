###############################################################################
# ProjectBuilder
#
# EPIC.......: 003
# Sprint.....: 3.x
# Arquivo....: builder/config/configuration_manager.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Gerenciador de Configurações do ProjectBuilder.
#   Gerencia configurações globais e de usuário.
#
###############################################################################
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .configuration_models import (
    Configuration,
    ConfigurationKey,
    ConfigurationValue,
)
class ConfigurationManager:
    """
    Gerenciador central de configurações.
    """
    CONFIG_DIR_NAME = ".projectbuilder"
    CONFIG_FILENAME = "config.json"
    def __init__(
        self,
        config_dir: Path | None = None,
    ) -> None:
        self._config_dir = (
            config_dir
            or Path.home() / self.CONFIG_DIR_NAME
        )
        self._config_file = self._config_dir / self.CONFIG_FILENAME
        self._data: dict[str, Any] = {}
        self._load()
    @property
    def config_directory(self) -> Path:
        return self._config_dir
    @property
    def config_file(self) -> Path:
        return self._config_file
    def get(
        self,
        key: str | ConfigurationKey,
        default: Any = None,
    ) -> Any:
        key_str = key.value if isinstance(key, ConfigurationKey) else key
        return self._data.get(key_str, default)
    def set(
        self,
        key: str | ConfigurationKey,
        value: Any,
    ) -> None:
        key_str = key.value if isinstance(key, ConfigurationKey) else key
        self._data[key_str] = value
        self._save()
    def delete(self, key: str | ConfigurationKey) -> bool:
        key_str = key.value if isinstance(key, ConfigurationKey) else key
        if key_str in self._data:
            del self._data[key_str]
            self._save()
            return True
        return False
    def to_dict(self) -> dict[str, Any]:
        return dict(self._data)
    def reset(self) -> None:
        self._data = {}
        self._save()
    # ─── Propriedades de conveniência ─────────────────────────────────
    @property
    def backup_directory(self) -> str:
        return self.get("backup_directory", str(Path.cwd() / "backups"))
    @backup_directory.setter
    def backup_directory(self, value: str) -> None:
        self.set("backup_directory", value)
    @property
    def backup_format(self) -> str:
        return self.get("backup_format", "zip")
    @backup_format.setter
    def backup_format(self, value: str) -> None:
        self.set("backup_format", value)
    @property
    def backup_keep_count(self) -> int:
        return int(self.get("backup_keep_count", 10))
    @backup_keep_count.setter
    def backup_keep_count(self, value: int) -> None:
        self.set("backup_keep_count", value)
    @property
    def migration_strategy(self) -> str:
        return self.get("migration_strategy", "replace")
    @migration_strategy.setter
    def migration_strategy(self, value: str) -> None:
        self.set("migration_strategy", value)
    @property
    def migration_enable_rollback(self) -> bool:
        return bool(self.get("migration_enable_rollback", True))
    @migration_enable_rollback.setter
    def migration_enable_rollback(self, value: bool) -> None:
        self.set("migration_enable_rollback", value)
    @property
    def report_directory(self) -> str:
        return self.get("report_directory", str(Path.cwd() / "reports"))
    @report_directory.setter
    def report_directory(self, value: str) -> None:
        self.set("report_directory", value)
    @property
    def report_format(self) -> str:
        return self.get("report_format", "html")
    @report_format.setter
    def report_format(self, value: str) -> None:
        self.set("report_format", value)
    @property
    def log_level(self) -> str:
        return self.get("log_level", "INFO")
    @log_level.setter
    def log_level(self, value: str) -> None:
        self.set("log_level", value)
    @property
    def editor_source(self) -> str:
        return self.get("editor_source", "vscode")
    @editor_source.setter
    def editor_source(self, value: str) -> None:
        self.set("editor_source", value)
    @property
    def editor_target(self) -> str:
        return self.get("editor_target", "vscodium")
    @editor_target.setter
    def editor_target(self, value: str) -> None:
        self.set("editor_target", value)
    # ─── Privados ──────────────────────────────────────────────────────
    def _load(self) -> None:
        if self._config_file.exists():
            try:
                self._data = json.loads(
                    self._config_file.read_text(encoding="utf-8")
                )
            except Exception:
                self._data = {}
    def _save(self) -> None:
        self._config_dir.mkdir(parents=True, exist_ok=True)
        self._config_file.write_text(
            json.dumps(
                self._data,
                indent=4,
                ensure_ascii=False,
                default=str,
            ),
            encoding="utf-8",
        )
    @property
    def summary_text(self) -> str:
        lines = [
            "=" * 50,
            "  ProjectBuilder Configuration",
            "=" * 50,
        ]
        for key, value in sorted(self._data.items()):
            lines.append(f"  {key:30s} = {value}")
        lines.append("=" * 50)
        return "\n".join(lines)
###############################################################################
# END FILE
###############################################################################
