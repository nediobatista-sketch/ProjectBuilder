###############################################################################
# FILE: tests/runtime/test_dependency_graph.py
###############################################################################

from builder.runtime.dependency_graph import DependencyGraph


class Logger:
    pass


class Database:
    pass


def test_graph_created():

    graph = DependencyGraph()

    assert len(graph) == 0


def test_add_service():

    graph = DependencyGraph()

    graph.add_service(Logger)

    assert graph.contains(Logger)


def test_add_dependency():

    graph = DependencyGraph()

    graph.add_dependency(Database, Logger)

    deps = graph.dependencies_of(Database)

    assert Logger in deps


def test_clear():

    graph = DependencyGraph()

    graph.add_service(Logger)

    graph.clear()

    assert len(graph) == 0

###############################################################################