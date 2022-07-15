"""Plugin for environment creation through conda."""

import json
from pathlib import Path
from typing import Dict, List

import pluggy
from edgetest.logger import get_logger
from edgetest.schema import Schema
from edgetest.utils import _run_command

LOG = get_logger(__name__)

hookimpl = pluggy.HookimplMarker("edgetest")


@hookimpl
def addoption(schema: Schema):
    """Add an environment-level variable for conda installation options.

    Parameters
    ----------
    schema : Schema
        The schema class.
    """

    def to_bool(x):
        return x.lower() in ["true", "1"]

    schema.add_envoption(
        "conda_install",
        {
            "type": "list",
            "schema": {"type": "string"},
            "coerce": "listify",
            "default": None,
            "nullable": True,
        },
    )
    schema.add_envoption(
        "python_version", {"type": "string", "default": "3.7", "coerce": str}
    )
    schema.add_envoption(
        "update_with_conda",
        {
            "type": "boolean",
            "coerce": to_bool,
            "required": False,
        },
    )


def _check_mamba() -> bool:
    """Check for ``mamba`` in the current environment.

    Parameters
    ----------
    None

    Returns
    -------
    bool
        A boolean status indicator. If ``True``, the environment has ``mamba``
        installed.
    """
    try:
        out, _ = _run_command("conda", "list", "--json")
        pkgs = json.loads(out)
        # Check for mamba
        status: bool = False
        for pkg in pkgs:
            if pkg["name"] == "mamba":
                status = True
                break
        else:
            LOG.debug("Unable to find ``mamba``. Using ``conda``.")
            status = False
    except RuntimeError:
        raise RuntimeError(
            "Unable to run ``conda list``. Please check that ``conda`` is available."
        )

    return status


@hookimpl
def create_environment(basedir: Path, envname: str, conf: Dict):
    """Create the conda environment.

    Parameters
    ----------
    basedir : Path
        The base directory location for the environment.
    envname : str
        The name of the virtual environment.
    conf : dict
        The configuration dictionary for the environment. We will look for ``conda_install``.

    Returns
    -------
    bool
        For ``firstresult`` mark compatability in Pluggy
        https://pluggy.readthedocs.io/en/stable/index.html#first-result-only


    Raises
    ------
    RuntimeError
        Error raised if the environment cannot be created.
    """
    # Create the conda environment
    env_manager = "mamba" if _check_mamba() else "conda"
    _run_command(
        env_manager,
        "create",
        "-p",
        str(basedir / envname),
        f"python={conf['python_version']}",
        "--yes",
    )

    # Install any conda packages
    if conf.get("conda_install"):
        LOG.info(f"Installing conda packages for {envname}")
        _run_command(
            env_manager,
            "install",
            "-p",
            str(basedir / envname),
            *conf["conda_install"],
            "--yes",
        )
        LOG.info(f"Successfully installed conda packages for {envname}")

    return True


@hookimpl
def run_update(basedir: Path, envname: str, upgrade: List, conf: Dict):
    """Update packages from upgrade list.

    Parameters
    ----------
    basedir : Path
        The base directory location for the environment.
    envname : str
        The name of the virtual environment.
    upgrade : list
        The list of packages to upgrade
    conf : dict
        The configuration dictionary for the environment. We will look for ``update_with_conda``.

    Returns
    -------
    bool
        For ``firstresult`` mark compatability in Pluggy
        https://pluggy.readthedocs.io/en/stable/index.html#first-result-only

    Raises
    ------
    RuntimeError
        Error raised if the packages cannot be updated.
    """
    if conf["update_with_conda"] is False:
        return None

    env_manager = "mamba" if _check_mamba() else "conda"
    try:
        _run_command(
            env_manager,
            "update",
            "-p",
            str(basedir / envname),
            *upgrade,
            "--yes",
        )
        return True
    except Exception:
        raise RuntimeError(f"Unable to {env_manager} update: {upgrade}")
