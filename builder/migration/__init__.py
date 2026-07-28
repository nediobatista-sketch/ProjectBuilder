###############################################################################
# ProjectBuilder
#
# EPIC.......: 006
# Sprint.....: 6.1
# Arquivo....: builder/migration/__init__.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Sistema de Migration do ProjectBuilder.
#   Coração do projeto: migração de configurações,
#   extensões, perfis, snippets e workspaces.
#
###############################################################################
from .migration_engine import MigrationEngine
from .migration_result import MigrationResult, MigrationStatus, MigrationItem
from .config_migrator import ConfigurationMigrator
from .extensions_migrator import ExtensionsMigrator
from .profiles_migrator import ProfilesMigrator
from .snippets_migrator import SnippetsMigrator
from .workspaces_migrator import WorkspacesMigrator
from .rollback import RollbackManager

__all__ = [
    "MigrationEngine",
    "MigrationResult",
    "MigrationStatus",
    "MigrationItem",
    "ConfigurationMigrator",
    "ExtensionsMigrator",
    "ProfilesMigrator",
    "SnippetsMigrator",
    "WorkspacesMigrator",
    "RollbackManager",
]
###############################################################################
# END FILE
###############################################################################
