###############################################################################
# FILE: builder/cli/main.py
###############################################################################

from __future__ import annotations

import sys
from builder import __version__


def main() -> int:
    """
    Função principal da CLI do ProjectBuilder.
    """
    if len(sys.argv) > 1 and sys.argv[1] in ("--version", "-v"):
        print(f"ProjectBuilder\nVersion : {__version__}\nPython  : {sys.version.split()[0]}")
        return 0

    print("ProjectBuilder CLI. Use --version para ver a versão.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

###############################################################################
# END FILE
###############################################################################