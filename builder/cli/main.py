import platform

from builder.version import __version__


def main():
    print("ProjectBuilder")
    print(f"Version : {__version__}")
    print(f"Python  : {platform.python_version()}")
    print(f"Platform: {platform.system()}")
