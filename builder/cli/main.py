###############################################################################
# FILE: builder/cli/main.py
#
# EPIC.......: 008
# Sprint.....: 8.1
# Versão.....: 1.0
#
# DESCRIÇÃO
#   CLI completa do ProjectBuilder.
#   Comandos: version, discover, backup, migrate,
#   report, config, install, clean.
#   Suporta: --verbose, --silent, --format, --progress.
#
###############################################################################
from __future__ import annotations
import argparse
import sys
import time
from pathlib import Path
from typing import Any
from builder import __version__
# ─── Progress Bar ──────────────────────────────────────────────────────
class ProgressBar:
    """Barra de progresso simples para terminal."""
    def __init__(
        self,
        total: int = 100,
        width: int = 40,
    ) -> None:
        self._total = total
        self._width = width
        self._current = 0
    def update(self, current: int) -> None:
        self._current = min(current, self._total)
        pct = self._current / self._total
        filled = int(pct * self._width)
        bar = "=" * filled + "-" * (self._width - filled)
        sys.stdout.write(
            f"\r  [{bar}] {pct:.0%} ({self._current}/{self._total})"
        )
        sys.stdout.flush()
    def finish(self) -> None:
        self.update(self._total)
        sys.stdout.write("\n")
        sys.stdout.flush()
# ─── Logger CLI ────────────────────────────────────────────────────────
class CliLogger:
    """Logger da CLI com níveis de verbosidade."""
    SILENT = 0
    NORMAL = 1
    VERBOSE = 2
    def __init__(self, level: int = NORMAL) -> None:
        self._level = level
    def info(self, message: str) -> None:
        if self._level >= self.NORMAL:
            print(message)
    def verbose(self, message: str) -> None:
        if self._level >= self.VERBOSE:
            print(f"  [VERBOSE] {message}")
    def error(self, message: str) -> None:
        print(f"  [ERROR] {message}", file=sys.stderr)
    def success(self, message: str) -> None:
        if self._level >= self.NORMAL:
            print(f"  [OK] {message}")
# ─── Handlers ──────────────────────────────────────────────────────────
def handle_version(args: Any, logger: CliLogger) -> int:
    """Handler: --version"""
    logger.info(f"ProjectBuilder v{__version__}")
    logger.verbose(f"Python: {sys.version.split()[0]}")
    return 0
def handle_discover(args: Any, logger: CliLogger) -> int:
    """Handler: discover - detecta ambiente do usuário."""
    logger.info("Descobrindo ambiente...")
    try:
        from builder.discovery import DiscoveryEngine, DiscoverySummary
        from builder.discovery.environment_detector import EnvironmentDetector
        from builder.discovery.filesystem_detector import FilesystemDetector
        from builder.discovery.package_detector import PackageDetector
        from builder.discovery.python_detector import PythonDetector
        summary = DiscoverySummary()
        engine = DiscoveryEngine()
        engine.register(EnvironmentDetector(summary))
        engine.register(FilesystemDetector(summary))
        engine.register(PackageDetector(summary))
        engine.register(PythonDetector(summary))
        result = engine.run()
        if not args.silent:
            print(result.summary_text)
        logger.success("Discovery concluído.")
        return 0
    except Exception as e:
        logger.error(f"Falha no Discovery: {e}")
        return 1
def handle_backup(args: Any, logger: CliLogger) -> int:
    """Handler: backup - cria backup do editor."""
    editor = args.editor or "vscode"
    output = Path(args.output) if args.output else Path.cwd() / "backups"
    fmt = args.format or "zip"
    logger.info(f"Backup de {editor} → {output}")
    if not args.silent:
        pb = ProgressBar(total=6)
        for i in range(7):
            time.sleep(0.1)
            pb.update(i)
        pb.finish()
    try:
        from builder.backup import BackupEngine, BackupCompressor
        engine = BackupEngine(
            backup_directory=output,
            format=fmt,
        )
        if editor == "vscode":
            result = engine.backup_vscode()
        elif editor == "vscodium":
            result = engine.backup_vscodium()
        else:
            logger.error(f"Editor desconhecido: {editor}")
            return 1
        if result.success:
            logger.success(
                f"Backup concluído: {result.item_count} itens, "
                f"{result.backed_up_count} com sucesso"
            )
            if args.verbose:
                print(result.to_dict())
            return 0
        else:
            logger.error(f"Backup falhou: {result.errors}")
            return 1
    except Exception as e:
        logger.error(f"Falha no Backup: {e}")
        return 1
def handle_migrate(args: Any, logger: CliLogger) -> int:
    """Handler: migrate - migra entre editores."""
    direction = args.direction or "vscode_to_vscodium"
    strategy = args.strategy or "replace"
    logger.info(f"Migração: {direction}")
    logger.verbose(f"Merge strategy: {strategy}")
    try:
        from builder.migration import MigrationEngine
        engine = MigrationEngine(
            merge_strategy=strategy,
            enable_rollback=not args.no_rollback,
            extension_strategy=args.ext_strategy or "list",
        )
        result = engine.migrate(direction)
        if not args.silent:
            print(result.summary_text)
        if result.success:
            logger.success("Migração concluída.")
            return 0
        else:
            logger.error(f"Migração falhou: {result.errors}")
            return 1
    except Exception as e:
        logger.error(f"Falha na Migration: {e}")
        return 1
def handle_report(args: Any, logger: CliLogger) -> int:
    """Handler: report - gera relatórios."""
    output = Path(args.output) if args.output else Path.cwd() / "reports"
    fmt = args.format or "html"
    logger.info(f"Gerando relatório {fmt} → {output}")
    try:
        from builder.reports import ReportEngine, ReportData, ReportFormat
        data = ReportData(
            title="ProjectBuilder Report",
            report_type="general",
        )
        data.add_section("info", {
            "version": __version__,
            "python": sys.version.split()[0],
        })
        engine = ReportEngine(output_directory=output)
        fmt_map = {
            "html": ReportFormat.HTML,
            "json": ReportFormat.JSON,
            "markdown": ReportFormat.MARKDOWN,
            "md": ReportFormat.MARKDOWN,
            "pdf": ReportFormat.PDF,
            "log": ReportFormat.LOG,
            "all": ReportFormat.ALL,
        }
        report_fmt = fmt_map.get(fmt.lower(), ReportFormat.HTML)
        results = engine.generate(data, [report_fmt])
        for f, path in results.items():
            logger.success(f"  {f}: {path}")
        return 0
    except Exception as e:
        logger.error(f"Falha no Report: {e}")
        return 1
def handle_config(args: Any, logger: CliLogger) -> int:
    """Handler: config - gerencia configurações."""
    action = args.action or "show"
    logger.info(f"Config: {action}")
    if action == "show":
        from builder.config.configuration_manager import ConfigurationManager
        manager = ConfigurationManager()
        print(manager.summary_text)
        return 0
    elif action == "set":
        if not args.key or not args.value:
            logger.error("Uso: config set <key> <value>")
            return 1
        from builder.config.configuration_manager import ConfigurationManager
        manager = ConfigurationManager()
        manager.set(args.key, args.value)
        logger.success(f"{args.key} = {args.value}")
        return 0
    elif action == "list":
        from builder.config.configuration_manager import ConfigurationManager
        manager = ConfigurationManager()
        for key, value in manager.to_dict().items():
            print(f"  {key:30s} = {value}")
        return 0
    else:
        logger.error(f"Ação desconhecida: {action}")
        return 1
def handle_install(args: Any, logger: CliLogger) -> int:
    """Handler: install - instala/atualiza ProjectBuilder."""
    logger.info("Verificando instalação...")
    try:
        from builder.installer import Installer
        installer = Installer()
        result = installer.install()
        if result:
            logger.success("Instalação concluída.")
        else:
            logger.error("Falha na instalação.")
            return 1
        return 0
    except Exception as e:
        logger.error(f"Falha na instalação: {e}")
        return 1
def handle_clean(args: Any, logger: CliLogger) -> int:
    """Handler: clean - limpa cache e temporários."""
    logger.info("Limpando cache...")
    import shutil
    cache_dirs = [
        Path.cwd() / ".projectbuilder" / "cache",
        Path.cwd() / "reports",
        Path.cwd() / "backups" / ".tmp",
    ]
    cleaned = 0
    for d in cache_dirs:
        if d.exists():
            try:
                count = sum(1 for _ in d.rglob("*"))
                shutil.rmtree(d)
                cleaned += count
                logger.verbose(f"  Removido: {d} ({count} arquivos)")
            except Exception as e:
                logger.error(f"  Erro em {d}: {e}")
    logger.success(f"Limpeza concluída. {cleaned} arquivos removidos.")
    return 0
def handle_status(args: Any, logger: CliLogger) -> int:
    """Handler: status - mostra status do projeto."""
    logger.info("Status do ProjectBuilder")
    print("=" * 50)
    print(f"  Versão     : {__version__}")
    print(f"  Python     : {sys.version.split()[0]}")
    print(f"  Platform   : {sys.platform}")
    print("=" * 50)
    # Módulos disponíveis
    modules = [
        ("Runtime", "builder.runtime"),
        ("Core", "builder.core"),
        ("Discovery", "builder.discovery"),
        ("Backup", "builder.backup"),
        ("Migration", "builder.migration"),
        ("Reports", "builder.reports"),
        ("Config", "builder.config"),
    ]
    print("\n  Módulos:")
    for name, module in modules:
        try:
            __import__(module)
            print(f"    ✓ {name}")
        except Exception as e:
            print(f"    ✗ {name} ({e})")
    print()
    return 0
# ─── Parser ────────────────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="projectbuilder",
        description="ProjectBuilder - Ferramenta de migração e backup "
                    "para VS Code e VSCodium.",
    )
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Mostra a versão do ProjectBuilder.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Modo verbose (detalhes adicionais).",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Modo silencioso (apenas erros).",
    )
    sub = parser.add_subparsers(dest="command")
    # version
    sub.add_parser("version", help="Mostra a versão.")
    # discover
    disc = sub.add_parser("discover", help="Descobre o ambiente.")
    disc.add_argument("--silent", action="store_true")
    # backup
    bk = sub.add_parser("backup", help="Cria backup do editor.")
    bk.add_argument("--editor", "-e", default="vscode",
                     choices=["vscode", "vscodium"])
    bk.add_argument("--output", "-o", default=None)
    bk.add_argument("--format", "-f", default="zip",
                     choices=["zip", "tar.gz"])
    bk.add_argument("--silent", action="store_true")
    bk.add_argument("--verbose", action="store_true")
    # migrate
    mg = sub.add_parser("migrate", help="Migra entre editores.")
    mg.add_argument("--direction", "-d",
                     default="vscode_to_vscodium",
                     choices=["vscode_to_vscodium", "vscodium_to_vscode"])
    mg.add_argument("--strategy", "-s", default="replace",
                     choices=["replace", "merge", "skip"])
    mg.add_argument("--ext-strategy", default="list",
                     choices=["list", "copy", "reinstall"])
    mg.add_argument("--no-rollback", action="store_true")
    mg.add_argument("--silent", action="store_true")
    mg.add_argument("--verbose", action="store_true")
    # report
    rp = sub.add_parser("report", help="Gera relatórios.")
    rp.add_argument("--format", "-f", default="html",
                     choices=["html", "json", "markdown", "md", "pdf", "log", "all"])
    rp.add_argument("--output", "-o", default=None)
    rp.add_argument("--silent", action="store_true")
    # config
    cf = sub.add_parser("config", help="Gerencia configurações.")
    cf.add_argument("action", nargs="?", default="show",
                     choices=["show", "set", "list"])
    cf.add_argument("--key", "-k", default=None)
    cf.add_argument("--value", default=None)
    cf.add_argument("--silent", action="store_true")
    # install
    sub.add_parser("install", help="Instala/atualiza o ProjectBuilder.")
    # clean
    sub.add_parser("clean", help="Limpa cache e temporários.")
    # status
    sub.add_parser("status", help="Mostra status do projeto.")
    return parser
# ─── Main ──────────────────────────────────────────────────────────────
def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    level = CliLogger.NORMAL
    if getattr(args, "silent", False):
        level = CliLogger.SILENT
    elif getattr(args, "verbose", False):
        level = CliLogger.VERBOSE
    logger = CliLogger(level=level)
    if args.version:
        return handle_version(args, logger)
    command = args.command
    if command is None:
        parser.print_help()
        return 0
    handlers = {
        "version": handle_version,
        "discover": handle_discover,
        "backup": handle_backup,
        "migrate": handle_migrate,
        "report": handle_report,
        "config": handle_config,
        "install": handle_install,
        "clean": handle_clean,
        "status": handle_status,
    }
    handler = handlers.get(command)
    if handler:
        return handler(args, logger)
    else:
        logger.error(f"Comando desconhecido: {command}")
        parser.print_help()
        return 1
###############################################################################
# END FILE
###############################################################################
