from __future__ import annotations

from .provider import ConfigurationProvider
from .settings import Settings


class ConfigurationLoader:
    """
    """

    def __init__(self, provider: ConfigurationProvider) -> None:
        self._provider = provider

    def load(self) -> Settings:
        settings = Settings()
        settings.update(self._provider.load())
        return settings


---

# Atualização do Índice

Adicionar:

0010 builder/runtime/configuration/loader.py

---

# Histórico

Sprint 2

Alterados

* builder/runtime/registry.py

Adicionados

+ builder/runtime/configuration/loader.py

ADR

+ ADR-0007 Service Registry baseado em Tipos

---

# Próxima etapa

Antes de criar o `EventBus`, eu recomendaria concluir totalmente o módulo de configuração implementando:

- `environment.py` (leitura de variáveis de ambiente);
- `exceptions.py` (erros específicos de configuração);


user
continue

ChatGPT


---

# RFC-0001

## Coding Standards


# RFC-0001

Título:
Padrões de Implementação

Status:
ACEITA

Todo código do ProjectBuilder deverá seguir:

- Python 3.13+
- Type Hints obrigatórios
- dataclass(slots=True) quando aplicável
- Docstrings Google Style
- Ruff
- Black
- Pyright (strict)
- pytest
- UTF-8
- Arquivos < 500 linhas
- Funções < 50 linhas
- Classes < 300 linhas



---

# Sprint 2

## Finalizando Configuration

---
