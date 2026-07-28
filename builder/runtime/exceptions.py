###############################################################################
# FILE: builder/runtime/exceptions.py
###############################################################################

"""
Runtime Exceptions.
"""

from __future__ import annotations


class RuntimeException(Exception):
    """
    Exceção base do Runtime.
    """


class RuntimeAlreadyRunning(RuntimeException):
    """
    Runtime já está em execução.
    """


class RuntimeNotRunning(RuntimeException):
    """
    Runtime não está em execução.
    """


class InvalidRuntimeState(RuntimeException):
    """
    Transição inválida entre estados.
    """


###############################################################################
# END FILE
###############################################################################