###############################################################################
# ProjectBuilder
#
# EPIC.......: 005
# Sprint.....: 5.1
# Arquivo....: builder/backup/__init__.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Sistema de Backup do ProjectBuilder.
#   Responsável por criar backups completos do VS Code e VSCodium.
#
###############################################################################
from .backup_engine import BackupEngine
from .backup_result import BackupResult
from .compressor import BackupCompressor
from .integrity import IntegrityVerifier
from .restorer import BackupRestorer
from .versioner import BackupVersioner

__all__ = [
    "BackupEngine",
    "BackupResult",
    "BackupCompressor",
    "IntegrityVerifier",
    "BackupRestorer",
    "BackupVersioner",
]
###############################################################################
# END FILE
###############################################################################
