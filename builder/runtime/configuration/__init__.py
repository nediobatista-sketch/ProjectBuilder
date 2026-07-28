from .settings import Settings
from .provider import ConfigurationProvider
from .loader import ConfigurationLoader
from .environment import EnvironmentProvider
from .toml_provider import TomlProvider

__all__ = [
    "Settings",
    "ConfigurationProvider",
    "ConfigurationLoader",
    "EnvironmentProvider",
    "TomlProvider",
]


---

# Estrutura

Agora temos:

configuration/

__init__.py

provider.py

loader.py

settings.py

environment.py

exceptions.py

toml_provider.py


---

# ADR-0008


# ADR-0008

Título

Configuration Providers

Status

ACEITA

Descrição


Providers oficiais:

EnvironmentProvider

TomlProvider

Futuramente:

YamlProvider

JsonProvider

VaultProvider

RemoteProvider


---

# Revisão Arquitetural

Neste momento temos:

Runtime
        │
        ▼
Configuration
        │
        ├── Loader
        ├── Settings
        ├── Providers
        └── Exceptions


---

# Atualização do Índice

Adicionar:

0011 builder/runtime/configuration/environment.py

0012 builder/runtime/configuration/exceptions.py

0013 builder/runtime/configuration/toml_provider.py

---

# Histórico

Sprint 2

Módulo Configuration

Concluído

Arquivos adicionados

+ environment.py

+ exceptions.py

+ toml_provider.py

RFC

+ RFC-0001 Coding Standards

ADR

+ ADR-0008 Configuration Providers

# Próximo Sprint

Agora que o módulo **Configuration** está completo, eu mudaria o foco para um componente que será utilizado por praticamente todo o framework:

builder/runtime/events/


user
continue

ChatGPT

Essa é exatamente a forma como projetos grandes (Spring, ASP.NET Core, NestJS, IntelliJ Platform) evoluem: **quando um módulo está prestes a se tornar a base de todo o sistema, sua arquitetura é revisada antes de crescer.**

---

# Sprint 3

## RFC-0002



# RFC-0002

Título:
Arquitetura Orientada a Eventos

Status:
ACEITA

Descrição


Nenhum componente deverá depender diretamente de outro quando

Objetivos

- baixo acoplamento
- extensibilidade
- observabilidade
- plugins
- telemetria
- logging
- auditoria


---

# Revisão da arquitetura

Em vez de:

Runtime

↓

Executor

↓

Worker

Passaremos para:

Runtime

↓

EventBus

↓

Subscribers

↓

Workers

↓

Plugins

↓

CLI

↓

SDK


---

# Estrutura

builder/runtime/events/

__init__.py

event.py

subscriber.py

publisher.py

event_bus.py

dispatcher.py

exceptions.py



---

# ADR-0009


# ADR-0009

Título

Eventos Imutáveis

Status

ACEITA

Descrição


Motivação





---
