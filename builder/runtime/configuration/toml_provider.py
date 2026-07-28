from __future__ import annotations

from pathlib import Path
import tomllib

from .provider import ConfigurationProvider
from .exceptions import ConfigurationFileNotFound


class TomlProvider(ConfigurationProvider):

    def __init__(self, filename: str):

        self._file = Path(filename)

    def load(self) -> dict:

        if not self._file.exists():

            raise ConfigurationFileNotFound(
                str(self._file)
            )

        with self._file.open("rb") as fp:

            return tomllib.load(fp)


---

# Atualização do __init__

O arquivo 0007 passa a ficar assim:
