from __future__ import annotations

from abc import ABC, abstractmethod

from .event import Event


class EventPublisher(ABC):

    @abstractmethod
    def publish(self, event: Event) -> None:
        raise NotImplementedError


---

# Revisão importante


**Eu não faria o EventBus síncrono.**

Ele já nascerá preparado para os dois modos:

publish()

↓

Dispatcher

↓

Sync

ou

Async


---

# Nova estrutura

Runtime

↓

Dispatcher

↓

Sync Dispatcher

↓

Async Dispatcher

↓

Subscribers

Assim:


---

# ADR-0010


# ADR-0010

Título

Dispatcher Separado do EventBus

Status

ACEITA

Descrição


Quem executa os Subscribers

Benefícios

- execução síncrona

- execução assíncrona

- filas futuras

- paralelismo


---

# Atualização do Índice

Adicionar:

0014 builder/runtime/events/event.py

0015 builder/runtime/events/subscriber.py

0016 builder/runtime/events/publisher.py

---

# Atualização do Histórico

Sprint 3

Novo módulo

Events

Arquivos

+ event.py

+ subscriber.py

+ publisher.py

RFC

+ RFC-0002 Arquitetura Orientada a Eventos

ADR

+ ADR-0009 Eventos Imutáveis

+ ADR-0010 Dispatcher Separado do EventBus

---

# Revisão de Engenharia



Por isso, eu adicionaria uma nova seção ao Master Source:

# PRODUCT BACKLOG

PB-0001 Runtime Foundation          [Em andamento]
PB-0002 Configuration Module        [Concluído]
PB-0003 Event System                [Em andamento]
PB-0004 Bootstrap                   [Pendente]
PB-0005 Dependency Injection        [Pendente]
PB-0006 Planner                     [Pendente]
PB-0007 Execution Plan              [Pendente]
PB-0008 Executor                    [Pendente]
PB-0009 Workers                     [Pendente]
PB-0010 Template Engine             [Pendente]


user
continue

ChatGPT

Até agora estávamos implementando **arquivos**. Em projetos reais, normalmente implementamos **uma funcionalidade completa**, incluindo:

- código;
- testes;
- documentação;
- exemplos;


---

# Sprint 3

## Product Backlog


# PRODUCT BACKLOG

ID        ITEM                              STATUS

PB-0001   Runtime Foundation                Em andamento
PB-0002   Configuration Module              Concluído
PB-0003   Event System                      Em andamento
PB-0004   Bootstrap                         Pendente
PB-0005   Dependency Injection              Pendente
PB-0006   Planner                           Pendente
PB-0007   Execution Plan                    Pendente
PB-0008   Executor                          Pendente
PB-0009   Workers                           Pendente
PB-0010   Template Engine                   Pendente
PB-0011   Plugin Manager                    Pendente
PB-0012   Marketplace                       Pendente
PB-0013   CLI                               Pendente
PB-0014   SDK                               Pendente
PB-0015   Test Infrastructure               Pendente


---

# Arquitetura do Event System


                   EventBus
                       │
          ┌────────────┴────────────┐
          │                         │
     Subscription              Publication
          │                         │
          └────────────┬────────────┘
                       │
                  Dispatcher
                ┌──────┴──────┐
                │             │
           Sync Mode     Async Mode
                │             │
           Subscribers   Subscribers


---

# ADR-0011


# ADR-0011

Título

Subscribers múltiplos por evento

Status

ACEITA

Descrição


Benefícios

- extensibilidade

- plugins

- logging

- métricas

- auditoria


---
