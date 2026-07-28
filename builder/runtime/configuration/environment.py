"""
Environment Configuration Provider
"""

from __future__ import annotations

import os

from .provider import ConfigurationProvider


class EnvironmentProvider(ConfigurationProvider):
    """
    """

    def __init__(self, prefix: str = "PROJECTBUILDER_") -> None:

        self._prefix = prefix

    def load(self) -> dict[str, str]:

        result: dict[str, str] = {}

        for key, value in os.environ.items():

            if key.startswith(self._prefix):

                name = key[len(self._prefix):].lower()

                result[name] = value

        return result


---
