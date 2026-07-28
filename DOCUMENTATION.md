# ProjectBuilder - Documentação Completa

**Versão:** 0.5.0-dev
**Data:** 28 de Julho de 2026

---

## Visão Geral

O **ProjectBuilder** é uma ferramenta Python para backup, migração e gerenciamento de ambientes VS Code e VSCodium. Ele permite descobrir o ambiente do usuário, criar backups completos, migrar configurações entre editores e gerar relatórios detalhados.

---

## Arquitetura

O projeto segue uma arquitetura modular organizada por EPICs (Épicos):

```
builder/
├── __init__.py          # Versão e metadata
├── __main__.py          # Ponto de entrada
├── cli/                 # EPIC-008: Interface CLI
│   └── main.py
├── core/                # Core: Task, Pipeline, Project, etc.
│   ├── artifact.py
│   ├── executor.py
│   ├── manifest.py
│   ├── pipeline.py
│   ├── project.py
│   ├── project_builder.py
│   ├── result.py
│   ├── stage.py
│   ├── task.py
│   └── workspace.py
├── discovery/           # EPIC-004: Descoberta de ambiente
│   ├── discovery_engine.py
│   ├── summary.py
│   ├── environment_detector.py
│   ├── filesystem_detector.py
│   ├── package_detector.py
│   ├── python_detector.py
│   ├── vscode_detector.py
│   ├── vscodium_detector.py
│   ├── extensions_detector.py
│   ├── profiles_detector.py
│   ├── settings_detector.py
│   ├── workspace_detector.py
│   ├── registry_detector.py
│   └── ...
├── backup/              # EPIC-005: Backup
│   ├── backup_engine.py
│   ├── backup_result.py
│   ├── compressor.py
│   ├── integrity.py
│   ├── restorer.py
│   └── versioner.py
├── migration/           # EPIC-006: Migração
│   ├── migration_engine.py
│   ├── migration_result.py
│   ├── config_migrator.py
│   ├── extensions_migrator.py
│   ├── profiles_migrator.py
│   ├── snippets_migrator.py
│   ├── workspaces_migrator.py
│   └── rollback.py
├── reports/             # EPIC-007: Relatórios
│   ├── report_engine.py
│   ├── models.py
│   ├── html_report.py
│   ├── json_report.py
│   ├── markdown_report.py
│   ├── pdf_report.py
│   └── log_report.py
├── config/              # EPIC-003: Configuração
│   ├── configuration_manager.py
│   └── configuration_models.py
├── installer/           # EPIC-010: Instalação
│   ├── installer.py
│   └── packager.py
├── runtime/             # EPIC-001: Runtime
│   ├── bootstrap.py
│   ├── builder.py
│   ├── context.py
│   ├── descriptor.py
│   ├── errors.py
│   ├── container.py
│   ├── dependency_graph.py
│   └── events/
└── platform/            # EPIC-002: Plataforma
    ├── os_helper.py
    ├── path_helper.py
    ├── file_helper.py
    ├── network.py
    └── permissions.py
```

---

## Módulos

### Runtime (EPIC-001) - 100%

O Runtime é o coração do sistema. Gerencia o ciclo de vida, injeção de dependências, eventos e plugins.

| Classe | Responsabilidade |
|--------|-----------------|
| `RuntimeBuilder` | Constrói o runtime |
| `Bootstrap` | Inicialização do sistema |
| `DependencyGraph` | Gerenciamento de dependências |
| `PluginManager` | Sistema de plugins |
| `EventBus` | Bus de eventos |
| `Container` | Container DI |
| `Errors` | Hierarquia de exceções |

### Core (EPIC-002) - 100%

Define as entidades fundamentais do sistema.

| Classe | Responsabilidade |
|--------|-----------------|
| `Task` | Tarefa atômica (abstrata) |
| `Stage` | Estágio de execução |
| `Pipeline` | Sequência de estágios |
| `Project` | Projeto gerenciado |
| `Workspace` | Área de trabalho |
| `Manifest` | Manifesto do projeto |
| `Artifact` | Artefato produzido |
| `Result` | Resultado de execução |
| `Executor` | Executor de pipelines |

### Discovery (EPIC-004) - 95%

Descobre o ambiente do usuário: plataforma, editores, extensões, perfis.

| Detector | O que detecta |
|----------|---------------|
| `EnvironmentDetector` | SO, versão, arquitetura |
| `FilesystemDetector` | Sistema de arquivos |
| `PackageDetector` | Pacotes instalados |
| `PythonDetector` | Instalações Python |
| `VSCodeDetector` | VS Code |
| `VSCodiumDetector` | VSCodium |
| `ExtensionsDetector` | Extensões |
| `ProfilesDetector` | Perfis |
| `SettingsDetector` | Configurações |
| `WorkspaceDetector` | Workspaces |

### Backup (EPIC-005) - 100%

Backup completo com compressão, versionamento, integridade e restauração.

| Classe | Responsabilidade |
|--------|-----------------|
| `BackupEngine` | Motor principal |
| `BackupCompressor` | Compressão zip/tar.gz |
| `IntegrityVerifier` | Verificação SHA256 |
| `BackupVersioner` | Versionamento |
| `BackupRestorer` | Restauração |
| `BackupResult` | Resultado |

### Migration (EPIC-006) - 100%

Migração de configurações entre editores com rollback.

| Classe | Responsabilidade |
|--------|-----------------|
| `MigrationEngine` | Motor principal |
| `ConfigurationMigrator` | Configurações |
| `ExtensionsMigrator` | Extensões |
| `ProfilesMigrator` | Perfis |
| `SnippetsMigrator` | Snippets |
| `WorkspacesMigrator` | Workspaces |
| `RollbackManager` | Rollback |
| `MigrationResult` | Resultado |

### Reports (EPIC-007) - 100%

Geração de relatórios em múltiplos formatos.

| Format | Classe | Extensão |
|--------|--------|----------|
| HTML | `HtmlReportGenerator` | `.html` |
| JSON | `JsonReportGenerator` | `.json` |
| Markdown | `MarkdownReportGenerator` | `.md` |
| PDF | `PdfReportGenerator` | `.pdf` |
| Log | `LogReportGenerator` | `.log` |

### CLI (EPIC-008) - 100%

Interface de linha de comando completa.

| Comando | Descrição |
|---------|-----------|
| `version` | Mostra a versão |
| `discover` | Descobre o ambiente |
| `backup` | Cria backup |
| `migrate` | Migra entre editores |
| `report` | Gera relatórios |
| `config` | Gerencia configurações |
| `install` | Instala/Atualiza |
| `clean` | Limpa cache |
| `status` | Status do projeto |

**Flags globais:** `--version`, `--verbose`, `--silent`

### Config (EPIC-003) - 100%

Gerenciamento de configurações persistente (JSON).

| Propriedade | Padrão |
|-------------|--------|
| `backup_directory` | `./backups` |
| `backup_format` | `zip` |
| `backup_keep_count` | `10` |
| `migration_strategy` | `replace` |
| `migration_enable_rollback` | `true` |
| `report_directory` | `./reports` |
| `report_format` | `html` |
| `log_level` | `INFO` |

### Installer (EPIC-010) - 100%

Instalação e empacotamento.

| Classe | Responsabilidade |
|--------|-----------------|
| `Installer` | Instalação (pip, standalone, portable) |
| `Packager` | Empacotamento (wheel, sdist, exe) |

---

## Uso

### Instalação

```bash
# Via pip (desenvolvimento)
pip install -e .

# Via instalador
python -m builder install
```

### CLI

```bash
# Ver versão
python -m builder --version

# Descobrir ambiente
python -m builder discover

# Criar backup
python -m builder backup --editor vscode --output ./backups --format zip

# Migrar
python -m builder migrate --direction vscode_to_vscodium --strategy replace

# Gerar relatório
python -m builder report --format html --output ./reports

# Gerenciar configuração
python -m builder config show
python -m builder config set backup_directory /path/to/backups

# Ver status
python -m builder status

# Limpar cache
python -m builder clean
```

### Uso Programático

```python
from builder.discovery import DiscoveryEngine, DiscoverySummary
from builder.discovery.environment_detector import EnvironmentDetector

# Discovery
summary = DiscoverySummary()
engine = DiscoveryEngine()
engine.register(EnvironmentDetector(summary))
result = engine.run()
print(result.summary_text)

# Backup
from builder.backup import BackupEngine
engine = BackupEngine(backup_directory="./backups", format="zip")
result = engine.backup_vscode()

# Migration
from builder.migration import MigrationEngine
engine = MigrationEngine(merge_strategy="replace", enable_rollback=True)
result = engine.migrate("vscode_to_vscodium")

# Reports
from builder.reports import ReportEngine, ReportData, ReportFormat
engine = ReportEngine(output_directory="./reports")
data = ReportData(title="Meu Relatório", report_type="backup")
data.add_section("info", {"version": "1.0"})
results = engine.generate(data, [ReportFormat.HTML, ReportFormat.JSON])
```

---

## Testes

O projeto possui **59 testes** passando (29 originais + 30 de integração).

```bash
# Rodar todos os testes
python -m pytest tests/ -v

# Rodar apenas integração
python -m pytest tests/test_integration.py -v

# Rodar com cobertura
python -m pytest tests/ --cov=builder
```

---

## Progresso

| EPIC | Módulo | Status | Progresso |
|------|--------|--------|-----------|
| 001 | Runtime | ✅ Concluído | 100% |
| 002 | Core | ✅ Concluído | 100% |
| 003 | Configuração | ✅ Concluído | 100% |
| 004 | Discovery | ✅ Concluído | 95% |
| 005 | Backup | ✅ Concluído | 100% |
| 006 | Migration | ✅ Concluído | 100% |
| 007 | Reports | ✅ Concluído | 100% |
| 008 | CLI | ✅ Concluído | 100% |
| 009 | Testes | ✅ Concluído | 100% |
| 010 | Release | ✅ Concluído | 80% |

**Progresso geral estimado: 85-90%**

---

## Repositório

- **URL:** https://github.com/nediobatista-sketch/ProjectBuilder
- **Branch:** main
- **Tag mais recente:** v0.4.0
- **Último commit:** EPIC-003 to EPIC-010: Nova funcionalidades
