###############################################################################
# FILE: tests/test_cli.py
###############################################################################

from __future__ import annotations

import subprocess
import sys


def test_version_command() -> None:
    """Valida se o comando --version retorna o código 0 e imprime a versão."""
    result = subprocess.run(
        [sys.executable, "-m", "builder", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "ProjectBuilder" in result.stdout
    assert "Version" in result.stdout or "v" in result.stdout

###############################################################################
# END FILE
###############################################################################
