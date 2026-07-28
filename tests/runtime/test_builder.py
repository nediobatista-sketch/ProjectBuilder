###############################################################################
# FILE: tests/runtime/test_builder.py
###############################################################################

from builder.runtime.builder import RuntimeBuilder


class Logger:
    pass


def test_builder_created():

    builder = RuntimeBuilder()

    assert builder is not None


def test_builder_services():

    builder = RuntimeBuilder()

    assert builder.services is not None


def test_builder_graph():

    builder = RuntimeBuilder()

    assert builder.graph is not None


def test_build_runtime():

    builder = RuntimeBuilder()

    runtime = builder.build()

    assert runtime is not None


def test_register_service():

    builder = RuntimeBuilder()

    builder.services.add_singleton(Logger)

    runtime = builder.build()

    logger = runtime.container.resolve(Logger)

    assert isinstance(logger, Logger)

###############################################################################