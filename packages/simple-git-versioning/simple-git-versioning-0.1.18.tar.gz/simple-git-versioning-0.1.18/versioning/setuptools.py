import logging
import tomllib
from pathlib import Path

from setuptools import Distribution
from versioning import pep440, semver2
from versioning.project import NotAGitWorkTree, NoVersion

LOGGER = logging.getLogger(__name__)


def finalize_distribution_options(distribution: Distribution) -> None:  # pragma: no cover
    with open("pyproject.toml", mode="rb") as stream:
        pyproject = tomllib.load(stream)

    try:
        flavor = pyproject["tool"]["simple-git-versioning"]["setuptools"]
    except KeyError:
        LOGGER.debug("simple-git-versioning is not enabled")
        return

    if not isinstance(flavor, str):
        raise TypeError(
            "unexpected value for `tool.simple-git-versioning.setuptools`:"
            f" '{pyproject['tool']['simple-git-versioning']['setuptools']}', expected 'pep440' or 'semver2'"
        )

    flavor = flavor.casefold()
    if flavor == "pep440":
        Project = pep440.Project
        options = dict(dev=0)
    elif flavor == "semver2":
        Project = semver2.Project
        options = dict()
    else:
        raise ValueError(
            f"unexpected value for `tool.simple-git-versioning.setuptools`: '{flavor}', expected 'pep440' or 'semver2'"
        )

    if distribution.metadata.name is None:
        distribution.metadata.name = pyproject["project"]["name"]

    if distribution.metadata.version is None:
        try:
            with Project(path=Path(".")) as proj:
                try:
                    distribution.metadata.version = str(proj.version())
                except NoVersion:
                    distribution.metadata.version = str(proj.release(**options))
        except NotAGitWorkTree:
            with open("PKG-INFO") as stream:
                for line in stream:
                    key, value = line.split(": ", maxsplit=1)
                    if key == "Version":
                        distribution.metadata.version = value
                        break
    else:
        LOGGER.debug(f"version is set already to: {distribution.metadata.version}")
