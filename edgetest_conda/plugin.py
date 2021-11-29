"""Plugin for environment creation through conda."""

import json
from pathlib import Path
from typing import Dict

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
            "Unable to run ``conda list``. Please check that you ``conda`` is available."
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
