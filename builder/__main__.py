###############################################################################
# FILE: builder/__main__.py
###############################################################################

from __future__ import annotations

import sys
from builder.cli.main import main

raise SystemExit(main())


def main() -> int:
    """Ponto de entrada principal do módulo."""
    return app()


if __name__ == "__main__":
    sys.exit(main())

###############################################################################
# END FILE
###############################################################################