###############################################################################
# ProjectBuilder
#
# Arquivo....: tests/runtime/test_context.py
#
###############################################################################

from builder.runtime import Runtime


def test_context():

    runtime = Runtime()

    ctx = runtime.context

    assert ctx.metadata.version is not None

    assert ctx.paths.project_root.exists()

    #
    # O Runtime inicia sem serviços registrados.
    #
    assert len(ctx.registry) == 0