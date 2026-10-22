"""AutoDOC's installable command-line interface."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import tomllib

try:
    __version__ = version("autodoc")
except PackageNotFoundError:  # source checkout without installed distribution metadata
    try:
        project_file = Path(__file__).resolve().parents[1] / "pyproject.toml"
        with project_file.open("rb") as stream:
            __version__ = tomllib.load(stream)["project"]["version"]
    except (OSError, KeyError, tomllib.TOMLDecodeError):
        __version__ = "0+unknown"

__all__ = ["__version__"]
