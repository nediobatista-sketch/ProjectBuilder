###############################################################################
# ProjectBuilder
#
# EPIC.......: 002
# Sprint.....: 2.3
# Arquivo....: tests/runtime/test_container.py
# Versão.....: 1.0
#
# DESCRIÇÃO
#   Testes do ServiceContainer.
#
###############################################################################

from __future__ import annotations

from builder.runtime.container import ServiceContainer
from builder.runtime.lifetime import ServiceLifetime


###############################################################################
# Classes auxiliares
###############################################################################


class Logger:
    pass


class Database:

    def __init__(self, logger: Logger):

        self.logger = logger


###############################################################################
# Testes
###############################################################################


def test_register():

    container = ServiceContainer()

    container.register(Logger)

    assert container.contains(Logger)


def test_singleton():

    container = ServiceContainer()

    container.register(Logger)

    a = container.resolve(Logger)

    b = container.resolve(Logger)

    assert a is b


def test_transient():

    container = ServiceContainer()

    container.register(
        Logger,
        lifetime=ServiceLifetime.TRANSIENT,
    )

    a = container.resolve(Logger)

    b = container.resolve(Logger)

    assert a is not b


def test_dependency_resolution():

    container = ServiceContainer()

    container.register(Logger)

    container.register(Database)

    database = container.resolve(Database)

    assert isinstance(database.logger, Logger)


def test_register_instance():

    logger = Logger()

    container = ServiceContainer()

    container.register_instance(
        Logger,
        logger,
    )

    assert container.resolve(Logger) is logger


def test_remove():

    container = ServiceContainer()

    container.register(Logger)

    container.remove(Logger)

    assert not container.contains(Logger)


def test_clear():

    container = ServiceContainer()

    container.register(Logger)

    container.register(Database)

    container.clear()

    assert len(container) == 0


def test_statistics():

    container = ServiceContainer()

    container.register(Logger)

    stats = container.statistics()

    assert stats.services == 1

    assert stats.singletons == 1

    assert stats.transients == 0

    assert stats.instances == 0


###############################################################################
# END FILE
###############################################################################