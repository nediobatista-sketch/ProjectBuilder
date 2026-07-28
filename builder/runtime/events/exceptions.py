class EventException(Exception):
    """Exceção base do sistema de eventos."""


class SubscriberAlreadyRegistered(EventException):
    """Subscriber já registrado."""


class InvalidEvent(EventException):
    """Evento inválido."""


---

# Testes



tests/runtime/events/

test_event.py

test_event_bus.py

test_dispatcher.py

test_subscriber.py


---

# Atualização do Índice

Adicionar:

0017 builder/runtime/events/event_bus.py
0018 builder/runtime/events/exceptions.py

---

# Histórico

Sprint 3

Módulo Events

Arquivos adicionados

+ event_bus.py
+ exceptions.py

ADR

+ ADR-0011 Subscribers múltiplos por evento

Backlog

+ Product Backlog

---

# Revisão de engenharia


Atualmente estamos registrando **ADRs**, **RFCs**, **Backlog**, **Histórico** e **Arquivos** em um único documento. Em projetos grandes, esses artefatos costumam ser separados. Para manter o objetivo do `ProjectBuilder_Master_Source.txt` como um documento reconstruível, eu faria a seguinte organização lógica dentro dele:



user
continue

ChatGPT


## Checkpoint Arquitetural — Sprint 3


Temos aproximadamente:

Runtime
    ✔ Lifecycle
    ✔ Registry
    ✔ Context
    ✔ Runtime
    ✔ Configuration
    ✔ Event Base

Ainda faltam

    □ Bootstrap
    □ Dependency Injection
    □ Plugin Manager
    □ Dispatcher
    □ Runtime Builder

---

# Revisão 1 — Separação de Contratos



Hoje:

runtime/

registry.py

event_bus.py

provider.py

Novo desenho:

builder/

contracts/

runtime/

events/

configuration/

plugins/

---

## Exemplo

Em vez de:

from builder.runtime.registry import ServiceRegistry

teremos:

from builder.contracts.runtime import IServiceRegistry

e

from builder.runtime.registry import ServiceRegistry


---

# ADR-0012


# ADR-0012

Título

Separação entre Contratos e Implementações

Status

ACEITA

Descrição



Objetivos

- reduzir dependências

- facilitar testes

- permitir múltiplas implementações


---

# Nova árvore

builder/

contracts/

runtime/

configuration/

events/

plugins/

application/

domain/

infrastructure/


---

# Revisão 2 — Eventos Tipados

Os eventos não serão apenas:

Event()


RuntimeStarted

RuntimeStopped

WorkerStarted

WorkerFinished

ProjectGenerated

TemplateRendered

PluginLoaded

PluginFailed

ConfigurationLoaded


---

# Nova hierarquia

Event

↓

RuntimeEvent

↓

RuntimeStarted

---
