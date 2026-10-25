"""The --dist-dir guard: only an artifact set matching the declared version may be verified."""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("autodoc_test_package", ROOT / "scripts/test_package.py")
test_package = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(test_package)

VERSION = test_package.PROJECT_VERSION
STEM = test_package.PROJECT_FILE_STEM


def test_the_filename_stem_is_the_escaped_distribution_name():
    # PEP 427: "autodoc-docs" ships as "autodoc_docs". The guard must agree with the build.
    assert STEM == test_package.PROJECT_NAME.replace("-", "_")
    assert STEM != test_package.PROJECT_NAME


def test_matching_artifact_names_are_accepted():
    wheel = Path(f"{STEM}-{VERSION}-py3-none-any.whl")
    sdist = Path(f"{STEM}-{VERSION}.tar.gz")
    assert test_package.check_distribution_names([wheel], [sdist]) == (wheel, sdist)


def test_a_version_mismatch_is_refused():
    with pytest.raises(RuntimeError, match="do not match the declared project version"):
        test_package.check_distribution_names(
            [Path(f"{STEM}-{VERSION}-py3-none-any.whl")], [Path(f"{STEM}-9.9.9.tar.gz")]
        )


def test_an_ambiguous_artifact_set_is_refused():
    with pytest.raises(RuntimeError, match="exactly one wheel"):
        test_package.check_distribution_names([], [])
