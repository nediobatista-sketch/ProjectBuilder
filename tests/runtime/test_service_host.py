###############################################################################
# FILE: tests/runtime/test_service_host.py
###############################################################################

from builder.runtime.container import ServiceContainer
from builder.runtime.service_host import HostState
from builder.runtime.service_host import ServiceHost


def test_created():

    host = ServiceHost(ServiceContainer())

    assert host.state is HostState.CREATED


def test_start():

    host = ServiceHost(ServiceContainer())

    host.start()

    assert host.state is HostState.RUNNING

    assert host.is_running


def test_stop():

    host = ServiceHost(ServiceContainer())

    host.start()

    host.stop()

    assert host.state is HostState.STOPPED

    assert not host.is_running


def test_double_start():

    host = ServiceHost(ServiceContainer())

    host.start()

    host.start()

    assert host.state is HostState.RUNNING


def test_double_stop():

    host = ServiceHost(ServiceContainer())

    host.stop()

    host.stop()

    assert host.state is HostState.STOPPED

###############################################################################