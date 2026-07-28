"""
Configuration Exceptions
"""


class ConfigurationException(Exception):
    """Base."""


class ConfigurationFileNotFound(ConfigurationException):
    """Arquivo inexistente."""


class InvalidConfiguration(ConfigurationException):
    """Configuração inválida."""


class ConfigurationProviderError(ConfigurationException):
    """Erro do Provider."""


---
