###############################################################################
# ProjectBuilder
#
# Arquivo....: tests/runtime/test_runtime.py
#
###############################################################################

import pytest

from builder.runtime import Runtime

from builder.runtime.exceptions import (
    RuntimeAlreadyRunning,
    RuntimeNotRunning,
)

from builder.runtime.lifecycle import RuntimeState


###############################################################################


def test_created():

    runtime = Runtime()

    assert runtime.status() is RuntimeState.CREATED


###############################################################################


def test_start():

    runtime = Runtime()

    runtime.start()

    assert runtime.status() is RuntimeState.RUNNING


###############################################################################


def test_stop():

    runtime = Runtime()

    runtime.start()

    runtime.stop()

    assert runtime.status() is RuntimeState.STOPPED


###############################################################################


def test_restart():

    runtime = Runtime()

    runtime.start()

    runtime.restart()

    assert runtime.status() is RuntimeState.RUNNING


###############################################################################


def test_double_start():

    runtime = Runtime()

    runtime.start()

    with pytest.raises(RuntimeAlreadyRunning):

        runtime.start()


###############################################################################


def test_stop_without_start():

    runtime = Runtime()

    with pytest.raises(RuntimeNotRunning):

        runtime.stop()