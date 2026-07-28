from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Settings:
    """
    """

    values: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self.values.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.values[key] = value

    def update(self, values: dict[str, Any]) -> None:
        self.values.update(values)


---

# Atualização da Estrutura

builder/runtime/

├── __init__.py
├── context.py
├── exceptions.py
├── lifecycle.py
├── registry.py
├── runtime.py
│
├── configuration/
│   ├── __init__.py      ✔
│   ├── provider.py      ✔
│   ├── settings.py      ✔
│   ├── loader.py
│   ├── environment.py
│   └── exceptions.py
│
├── events/
├── plugins/
└── bootstrap/

---

# Atualização do Índice


0007 builder/runtime/configuration/__init__.py
0008 builder/runtime/configuration/provider.py
0009 builder/runtime/configuration/settings.py

---

# Histórico

Sprint 2

Módulo Configuration

Arquivos adicionados

+ builder/runtime/configuration/__init__.py
+ builder/runtime/configuration/provider.py
+ builder/runtime/configuration/settings.py

ADR

+ ADR-0006 Sistema de Configuração baseado em Providers

---

## Revisão arquitetural


Em vez de manter o `ProjectBuilder_Master_Source.txt` apenas como um arquivo de documentação, podemos tratá-lo como um **artefato reconstruível** com metadados estruturados para cada arquivo, por exemplo:
