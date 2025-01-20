import subprocess
import sys

from site_builder import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "site_builder", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
