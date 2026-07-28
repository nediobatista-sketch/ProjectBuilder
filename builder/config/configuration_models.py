###############################################################################
# ProjectBuilder
#
# EPIC.......: 003
# Sprint.....: 3.x
# Arquivo....: builder/config/configuration_models.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Modelos de dados para o sistema de Configuração.
#
###############################################################################
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any
class ConfigurationKey(Enum):
    """Chaves de configuração suportadas."""
    BACKUP_DIRECTORY = "backup_directory"
    BACKUP_FORMAT = "backup_format"
    BACKUP_KEEP_COUNT = "backup_keep_count"
    MIGRATION_STRATEGY = "migration_strategy"
    MIGRATION_ENABLE_ROLLBACK = "migration_enable_rollback"
    REPORT_DIRECTORY = "report_directory"
    REPORT_FORMAT = "report_format"
    LOG_LEVEL = "log_level"
    LOG_FILE = "log_file"
    EDITOR_SOURCE = "editor_source"
    EDITOR_TARGET = "editor_target"
    TEMP_DIRECTORY = "temp_directory"
    VERSION = "version"
class ConfigurationValue:
    """Valor de configuração tipado."""
    def __init__(self, value: Any, value_type: type = str) -> None:
        self._value = value
        self._type = value_type
    @property
    def value(self) -> Any:
        return self._value
    @value.setter
    def value(self, new_value: Any) -> None:
        self._value = new_value
    @property
    def value_type(self) -> type:
        return self._type
    def to_string(self) -> str:
        return str(self._value)
    def __repr__(self) -> str:
        return f"ConfigurationValue({self._value!r})"
@dataclass(slots=True)
class Configuration:
    """
    Representa uma configuração completa.
    """
    key: str = ""
    value: ConfigurationValue | None = None
    default: Any = None
    description: str = ""
    mutable: bool = True
###############################################################################
# END FILE
###############################################################################
