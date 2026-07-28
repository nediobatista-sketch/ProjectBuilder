###############################################################################
# ProjectBuilder - Testes de Integração
#
# EPIC.......: 009
# Sprint.....: 9.1
# Arquivo....: tests/test_integration.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Testes de integração para os módulos:
#   Runtime, Core, Discovery, Backup, Migration, Reports, Config, CLI.
#
###############################################################################
from __future__ import annotations
import json
import shutil
import tempfile
from pathlib import Path
# ─── Runtime ───────────────────────────────────────────────────────────
def test_runtime_builder():
    from builder.runtime.builder import RuntimeBuilder
    builder = RuntimeBuilder()
    assert builder is not None
    assert hasattr(builder, "build")
def test_runtime_builder_creates_runtime():
    from builder.runtime.builder import RuntimeBuilder
    builder = RuntimeBuilder()
    runtime = builder.build()
    assert runtime is not None
def test_runtime_bootstrap():
    from builder.runtime.bootstrap import Bootstrap
    bs = Bootstrap()
    assert bs is not None
# ─── Core ──────────────────────────────────────────────────────────────
def test_core_task():
    from builder.core.task import Task
    # Task é abstrata — testar que a classe existe e tem método execute
    assert hasattr(Task, 'execute')
    assert hasattr(Task, 'name')
def test_core_pipeline():
    from builder.core.pipeline import Pipeline
    p = Pipeline()
    assert p is not None
def test_core_result():
    from builder.core.result import Result
    r = Result(success=True)
    assert r.success is True
def test_core_manifest():
    from builder.core.manifest import Manifest
    m = Manifest(name="test", version="1.0")
    assert m.name == "test"
    assert m.version == "1.0"
def test_core_project():
    from builder.core.project import Project
    p = Project(name="test_project", root=Path("/tmp/test"))
    assert p.name == "test_project"
def test_core_project_builder():
    from builder.core.project_builder import ProjectBuilder
    pb = ProjectBuilder(name="test", root=Path("/tmp/test"))
    assert pb is not None
def test_core_stage():
    from builder.core.stage import Stage
    s = Stage(name="test_stage")
    assert s is not None
def test_core_artifact():
    from builder.core.artifact import Artifact
    a = Artifact(name="test", path=Path("/tmp/test"), artifact_type="file")
    assert a is not None
# ─── Discovery ─────────────────────────────────────────────────────────
def test_discovery_summary():
    from builder.discovery.summary import DiscoverySummary
    s = DiscoverySummary()
    assert s is not None
def test_discovery_engine():
    from builder.discovery.discovery_engine import DiscoveryEngine
    from builder.discovery.summary import DiscoverySummary
    from builder.discovery.environment_detector import EnvironmentDetector
    summary = DiscoverySummary()
    engine = DiscoveryEngine()
    engine.register(EnvironmentDetector(summary))
    result = engine.run()
    assert result is not None
    assert engine.detector_count >= 1
def test_discovery_environment_detector():
    from builder.discovery.environment_detector import EnvironmentDetector
    from builder.discovery.summary import DiscoverySummary
    summary = DiscoverySummary()
    detector = EnvironmentDetector(summary)
    assert detector is not None
def test_discovery_filesystem_detector():
    from builder.discovery.filesystem_detector import FilesystemDetector
    from builder.discovery.summary import DiscoverySummary
    summary = DiscoverySummary()
    detector = FilesystemDetector(summary)
    assert detector is not None
def test_discovery_package_detector():
    from builder.discovery.package_detector import PackageDetector
    from builder.discovery.summary import DiscoverySummary
    summary = DiscoverySummary()
    detector = PackageDetector(summary)
    assert detector is not None
def test_discovery_python_detector():
    from builder.discovery.python_detector import PythonDetector
    from builder.discovery.summary import DiscoverySummary
    summary = DiscoverySummary()
    detector = PythonDetector(summary)
    assert detector is not None
# ─── Backup ────────────────────────────────────────────────────────────
def test_backup_compressor():
    from builder.backup.compressor import BackupCompressor
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "source"
        src.mkdir()
        (src / "test.txt").write_text("hello")
        dst = Path(tmp) / "backup.zip"
        comp = BackupCompressor(default_format="zip")
        result = comp.compress_directory(src, dst)
        assert result.success is True
        assert result.archive.exists()
def test_backup_compressor_targz():
    from builder.backup.compressor import BackupCompressor
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "source"
        src.mkdir()
        (src / "test.txt").write_text("hello")
        dst = Path(tmp) / "backup.tar.gz"
        comp = BackupCompressor(default_format="tar.gz")
        result = comp.compress_directory(src, dst)
        assert result.success is True
def test_backup_decompress():
    from builder.backup.compressor import BackupCompressor
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "source"
        src.mkdir()
        (src / "test.txt").write_text("hello world")
        dst = Path(tmp) / "backup.zip"
        comp = BackupCompressor(default_format="zip")
        comp.compress_directory(src, dst)
        extract_dir = Path(tmp) / "extracted"
        result = comp.decompress(dst, extract_dir)
        assert result.success is True
def test_backup_integrity():
    from builder.backup.integrity import IntegrityVerifier
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "test.txt").write_text("hello")
        verifier = IntegrityVerifier()
        manifest = verifier.create_manifest(d, editor="test")
        assert len(manifest.files) > 0
        verified = verifier.verify_manifest(d, manifest)
        assert all(f.valid for f in verified.files)
def test_backup_versioner():
    from builder.backup.versioner import BackupVersioner
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "backups"
        d.mkdir()
        (d / "test.zip").write_bytes(b"test data")
        versioner = BackupVersioner(d)
        v = versioner.version(
            archive_path=d / "test.zip",
            editor="VSCode",
        )
        assert v.number == 1
        assert v.editor == "VSCode"
        assert versioner.history.count == 1
def test_backup_versioner_list():
    from builder.backup.versioner import BackupVersioner
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "backups"
        d.mkdir()
        for i in range(3):
            f = d / f"backup_{i}.zip"
            f.write_bytes(b"test")
            versioner = BackupVersioner(d)
            versioner.version(archive_path=f, editor="VSCode")
        assert len(versioner.list_versions()) == 3
def test_backup_result():
    from builder.backup.backup_result import BackupResult, BackupStatus
    result = BackupResult(editor="VSCode")
    assert result.editor == "VSCode"
    assert result.status == BackupStatus.CREATED
    assert result.success is False
    result.status = BackupStatus.COMPLETED
    assert result.success is True
def test_backup_result_dict():
    from builder.backup.backup_result import BackupResult, BackupStatus
    result = BackupResult(editor="VSCode")
    result.status = BackupStatus.COMPLETED
    result.finish()
    d = result.to_dict()
    assert d["editor"] == "VSCode"
    assert d["status"] == "COMPLETED"
def test_backup_engine():
    from builder.backup.backup_engine import BackupEngine
    with tempfile.TemporaryDirectory() as tmp:
        engine = BackupEngine(backup_directory=Path(tmp))
        assert engine.backup_directory == Path(tmp)
def test_backup_restorer():
    from builder.backup.restorer import BackupRestorer
    from builder.backup.compressor import BackupCompressor
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "source"
        src.mkdir()
        (src / "test.txt").write_text("hello")
        dst = Path(tmp) / "backup.zip"
        comp = BackupCompressor(default_format="zip")
        comp.compress_directory(src, dst)
        restorer = BackupRestorer(comp)
        extract = Path(tmp) / "restored"
        result = restorer.restore_directory(dst, extract)
        assert result.status.value == 7  # RESTORED
# ─── Migration ─────────────────────────────────────────────────────────
def test_migration_result():
    from builder.migration.migration_result import (
        MigrationResult, MigrationStatus,
    )
    result = MigrationResult(
        source_editor="VSCode",
        target_editor="VSCodium",
    )
    assert result.source_editor == "VSCode"
    assert result.target_editor == "VSCodium"
    assert result.status == MigrationStatus.CREATED
    result.status = MigrationStatus.COMPLETED
    assert result.success is True
def test_migration_result_dict():
    from builder.migration.migration_result import MigrationResult, MigrationStatus
    result = MigrationResult(source_editor="A", target_editor="B")
    result.status = MigrationStatus.COMPLETED
    result.finish()
    d = result.to_dict()
    assert d["source_editor"] == "A"
    assert d["status"] == "COMPLETED"
def test_migration_engine():
    from builder.migration.migration_engine import MigrationEngine
    engine = MigrationEngine()
    assert engine is not None
    assert engine.merge_strategy == "replace"
    assert engine.enable_rollback is True
def test_config_migrator():
    from builder.migration.config_migrator import ConfigurationMigrator
    migrator = ConfigurationMigrator(merge_strategy="replace")
    assert migrator.merge_strategy == "replace"
    assert "settings.json" in migrator.CONFIG_FILES
def test_config_migrator_migrate():
    from builder.migration.config_migrator import ConfigurationMigrator
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "source"
        target = Path(tmp) / "target"
        source.mkdir()
        (source / "settings.json").write_text('{"test": true}')
        migrator = ConfigurationMigrator()
        items = migrator.migrate(source, target)
        assert len(items) > 0
def test_extensions_migrator():
    from builder.migration.extensions_migrator import ExtensionsMigrator
    migrator = ExtensionsMigrator()
    assert migrator is not None
def test_rollback_manager():
    from builder.migration.rollback import RollbackManager
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        manager = RollbackManager(d)
        assert manager is not None
        assert manager.rollback_directory == d / ".rollback"
def test_profiles_migrator():
    from builder.migration.profiles_migrator import ProfilesMigrator
    migrator = ProfilesMigrator()
    assert migrator is not None
def test_snippets_migrator():
    from builder.migration.snippets_migrator import SnippetsMigrator
    migrator = SnippetsMigrator()
    assert migrator is not None
def test_workspaces_migrator():
    from builder.migration.workspaces_migrator import WorkspacesMigrator
    migrator = WorkspacesMigrator()
    assert migrator is not None
# ─── Reports ───────────────────────────────────────────────────────────
def test_report_engine():
    from builder.reports.report_engine import ReportEngine, ReportFormat
    from builder.reports.models import ReportData
    with tempfile.TemporaryDirectory() as tmp:
        engine = ReportEngine(output_directory=Path(tmp))
        data = ReportData(title="Test", report_type="test")
        data.add_section("info", {"version": "1.0"})
        results = engine.generate(data, [ReportFormat.JSON])
        assert "json" in results
        assert results["json"].exists()
def test_report_html():
    from builder.reports.html_report import HtmlReportGenerator
    from builder.reports.models import ReportData
    with tempfile.TemporaryDirectory() as tmp:
        gen = HtmlReportGenerator()
        data = ReportData(title="Test", report_type="test")
        data.add_section("info", {"status": "ok"})
        gen.generate(data, Path(tmp) / "test.html")
        assert (Path(tmp) / "test.html").exists()
        content = (Path(tmp) / "test.html").read_text()
        assert "Test" in content
def test_report_markdown():
    from builder.reports.markdown_report import MarkdownReportGenerator
    from builder.reports.models import ReportData
    with tempfile.TemporaryDirectory() as tmp:
        gen = MarkdownReportGenerator()
        data = ReportData(title="Test", report_type="test")
        data.add_section("info", {"status": "ok"})
        gen.generate(data, Path(tmp) / "test.md")
        assert (Path(tmp) / "test.md").exists()
        content = (Path(tmp) / "test.md").read_text()
        assert "Test" in content
def test_report_json():
    from builder.reports.json_report import JsonReportGenerator
    from builder.reports.models import ReportData
    with tempfile.TemporaryDirectory() as tmp:
        gen = JsonReportGenerator()
        data = ReportData(title="Test", report_type="test")
        data.add_section("info", {"status": "ok"})
        gen.generate(data, Path(tmp) / "test.json")
        assert (Path(tmp) / "test.json").exists()
        loaded = json.loads((Path(tmp) / "test.json").read_text())
        assert loaded["title"] == "Test"
def test_report_log():
    from builder.reports.log_report import LogReportGenerator
    from builder.reports.models import ReportData
    with tempfile.TemporaryDirectory() as tmp:
        gen = LogReportGenerator()
        data = ReportData(title="Test", report_type="test")
        data.add_section("info", {"status": "ok"})
        gen.generate(data, Path(tmp) / "test.log")
        assert (Path(tmp) / "test.log").exists()
def test_report_all_formats():
    from builder.reports.report_engine import ReportEngine, ReportFormat
    from builder.reports.models import ReportData
    with tempfile.TemporaryDirectory() as tmp:
        engine = ReportEngine(output_directory=Path(tmp))
        data = ReportData(title="Test", report_type="test")
        data.add_section("info", {"status": "ok"})
        results = engine.generate(data, [ReportFormat.ALL])
        assert len(results) >= 4
# ─── Config ────────────────────────────────────────────────────────────
def test_config_manager():
    from builder.config.configuration_manager import ConfigurationManager
    with tempfile.TemporaryDirectory() as tmp:
        manager = ConfigurationManager(config_dir=Path(tmp))
        manager.set("test_key", "test_value")
        assert manager.get("test_key") == "test_value"
        assert "test_key" in manager.to_dict()
        manager.delete("test_key")
        assert manager.get("test_key") is None
def test_config_properties():
    from builder.config.configuration_manager import ConfigurationManager
    with tempfile.TemporaryDirectory() as tmp:
        manager = ConfigurationManager(config_dir=Path(tmp))
        manager.backup_format = "tar.gz"
        assert manager.backup_format == "tar.gz"
        manager.migration_strategy = "merge"
        assert manager.migration_strategy == "merge"
def test_config_persistence():
    from builder.config.configuration_manager import ConfigurationManager
    with tempfile.TemporaryDirectory() as tmp:
        manager = ConfigurationManager(config_dir=Path(tmp))
        manager.set("persist_key", "persist_value")
        manager2 = ConfigurationManager(config_dir=Path(tmp))
        assert manager2.get("persist_key") == "persist_value"
# ─── CLI ───────────────────────────────────────────────────────────────
def test_cli_parser():
    from builder.cli.main import build_parser
    parser = build_parser()
    assert parser is not None
def test_cli_version():
    from builder.cli.main import main
    import sys
    old = sys.argv
    sys.argv = ["pb", "--version"]
    rc = main()
    sys.argv = old
    assert rc == 0
def test_cli_status():
    from builder.cli.main import main
    import sys
    old = sys.argv
    sys.argv = ["pb", "status"]
    rc = main()
    sys.argv = old
    assert rc == 0
def test_cli_discover():
    from builder.cli.main import main
    import sys
    old = sys.argv
    sys.argv = ["pb", "discover"]
    rc = main()
    sys.argv = old
    assert rc == 0
def test_cli_report():
    from builder.cli.main import main
    import sys
    with tempfile.TemporaryDirectory() as tmp:
        old = sys.argv
        sys.argv = ["pb", "report", "--format", "json", "--output", tmp]
        rc = main()
        sys.argv = old
        assert rc == 0
        assert (Path(tmp) / "report_json.json").exists()
# ─── Installer ─────────────────────────────────────────────────────────
def test_installer():
    from builder.installer.installer import Installer
    installer = Installer()
    assert installer is not None
def test_installer_check():
    from builder.installer.installer import Installer
    installer = Installer()
    assert installer.is_installed() is True
def test_packager():
    from builder.installer.packager import Packager
    packager = Packager()
    assert packager is not None
# ─── Cross-module integration ─────────────────────────────────────────
def test_discovery_to_backup():
    """Testa o fluxo Discovery → Backup."""
    from builder.discovery.discovery_engine import DiscoveryEngine
    from builder.discovery.summary import DiscoverySummary
    from builder.discovery.environment_detector import EnvironmentDetector
    from builder.backup.backup_engine import BackupEngine
    summary = DiscoverySummary()
    engine = DiscoveryEngine()
    engine.register(EnvironmentDetector(summary))
    result = engine.run()
    assert result is not None
    backup_engine = BackupEngine()
    assert backup_engine.backup_directory is not None
def test_backup_to_report():
    """Testa o fluxo Backup → Report."""
    from builder.backup.backup_result import BackupResult, BackupStatus
    from builder.reports.report_engine import ReportEngine, ReportFormat
    result = BackupResult(editor="VSCode")
    result.status = BackupStatus.COMPLETED
    result.finish()
    with tempfile.TemporaryDirectory() as tmp:
        engine = ReportEngine(output_directory=Path(tmp))
        reports = engine.generate_from_backup(result, [ReportFormat.JSON])
        assert "json" in reports
        assert reports["json"].exists()
def test_migration_to_report():
    """Testa o fluxo Migration → Report."""
    from builder.migration.migration_result import MigrationResult, MigrationStatus
    from builder.reports.report_engine import ReportEngine, ReportFormat
    result = MigrationResult(
        source_editor="VSCode",
        target_editor="VSCodium",
        status=MigrationStatus.COMPLETED,
    )
    result.finish()
    with tempfile.TemporaryDirectory() as tmp:
        engine = ReportEngine(output_directory=Path(tmp))
        reports = engine.generate_from_migration(result, [ReportFormat.JSON])
        assert "json" in reports
        assert reports["json"].exists()
def test_full_pipeline():
    """Testa o pipeline completo: Discovery → Backup → Report."""
    from builder.discovery.discovery_engine import DiscoveryEngine
    from builder.discovery.summary import DiscoverySummary
    from builder.discovery.environment_detector import EnvironmentDetector
    from builder.backup.backup_result import BackupResult, BackupStatus
    from builder.reports.report_engine import ReportEngine, ReportFormat
    summary = DiscoverySummary()
    engine = DiscoveryEngine()
    engine.register(EnvironmentDetector(summary))
    discovery_result = engine.run()
    assert discovery_result is not None
    backup_result = BackupResult(editor="VSCode")
    backup_result.status = BackupStatus.COMPLETED
    backup_result.finish()
    with tempfile.TemporaryDirectory() as tmp:
        report_engine = ReportEngine(output_directory=Path(tmp))
        reports = report_engine.generate(
            __import__(
                "builder.reports.models",
                fromlist=["ReportData"],
            ).ReportData(
                title="Full Pipeline Test",
                report_type="integration",
            ),
            [ReportFormat.JSON, ReportFormat.MARKDOWN],
        )
        assert len(reports) >= 2
###############################################################################
# END FILE
###############################################################################
