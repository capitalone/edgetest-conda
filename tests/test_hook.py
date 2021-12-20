"""Test the conda hook."""

import platform
from pathlib import Path
from unittest.mock import call, patch, PropertyMock

from click.testing import CliRunner
from edgetest.interface import cli
from edgetest.schema import EdgetestValidator, Schema
from edgetest.utils import parse_cfg
import pytest

from edgetest_conda.plugin import addoption, _check_mamba

CFG = """
[edgetest.envs.myenv]
conda_install = 
    graphviz
python_version = 3.8
upgrade = 
    myupgrade
command = 
    pytest tests -m 'not integration'
"""

CFG_NOCONDA = """
[edgetest.envs.myenv]
upgrade = 
    myupgrade
command = 
    pytest tests -m 'not integration'
"""

PIP_LIST = """
[{"name": "myupgrade", "version": "0.2.0"}]
"""

PIP_LIST_MAMBA = """
[{"name": "myupgrade", "version": "0.2.0"}, {"name": "mamba", "version": "0.14.1"}]
"""

TABLE_OUTPUT = """

=============  ===============  ===================  =================
Environment    Passing tests    Upgraded packages    Package version
=============  ===============  ===================  =================
myenv          True             myupgrade            0.2.0
=============  ===============  ===================  =================
"""

@pytest.mark.parametrize("config", [CFG, CFG_NOCONDA])
def test_addoption(config, tmpdir):
    """Test the addoption hook."""
    location = tmpdir.mkdir("mylocation")
    conf_loc = Path(str(location), "myconfig.ini")
    with open(conf_loc, "w") as outfile:
        outfile.write(config)

    schema = Schema()
    addoption(schema=schema)

    cfg = parse_cfg(filename=conf_loc)

    validator = EdgetestValidator(schema=schema.schema)
    validator.validate(cfg)
    print(validator.errors)
    
    assert validator.validate(cfg)

@patch("edgetest.utils.Popen", autospec=True)
def test_mamba_check(mock_popen):
    """Test looking for ``mamba``."""
    mock_popen.return_value.communicate.return_value = ('[{"name": "mamba"}]', "error")
    type(mock_popen.return_value).returncode = PropertyMock(return_value=0)

    output = _check_mamba()

    assert mock_popen.call_args_list == [
        call(
            ("conda", "list", "--json"),
            stdout=-1,
            universal_newlines=True,
        )
    ]

    assert output

@patch("edgetest.core.Popen", autospec=True)
@patch("edgetest.utils.Popen", autospec=True)
def test_conda_create(mock_popen, mock_cpopen):
    """Test creating a basic conda environment."""
    mock_popen.return_value.communicate.return_value = (PIP_LIST, "error")
    type(mock_popen.return_value).returncode = PropertyMock(return_value=0)
    mock_cpopen.return_value.communicate.return_value = ("output", "error")
    type(mock_cpopen.return_value).returncode = PropertyMock(return_value=0)

    runner = CliRunner()

    with runner.isolated_filesystem() as loc:
        with open("config.ini", "w") as outfile:
            outfile.write(CFG)

        result = runner.invoke(cli, ["--config=config.ini"])

    assert result.exit_code == 0

    env_loc = str(Path(loc) / ".edgetest" / "myenv")
    if platform.system() == "Windows":
        py_loc = str(Path(env_loc)  / "Scripts" / "python")
    else:
        py_loc = str(Path(env_loc)  / "bin" / "python")


    assert mock_popen.call_args_list == [
        call(
            ("conda", "list", "--json"),
            stdout=-1,
            universal_newlines=True,
        ),
        call(
            ("conda", "create", "-p", env_loc, "python=3.8", "--yes"),
            stdout=-1,
            universal_newlines=True
        ),
        call(
            ("conda", "install", "-p", env_loc, "graphviz", "--yes"),
            stdout=-1,
            universal_newlines=True
        ),
        call(
            (f"{py_loc}", "-m", "pip", "install", "."),
            stdout=-1,
            universal_newlines=True,
        ),
        call(
            (f"{py_loc}", "-m", "pip", "install", "myupgrade", "--upgrade"),
            stdout=-1,
            universal_newlines=True,
        ),
        call(
            (f"{py_loc}", "-m", "pip", "list", "--format", "json"),
            stdout=-1,
            universal_newlines=True,
        ),
    ]
    assert mock_cpopen.call_args_list == [
        call(
            (f"{py_loc}", "-m", "pytest", "tests", "-m", "not integration"),
            universal_newlines=True,
        )
    ]

    assert result.output == TABLE_OUTPUT

@patch("edgetest.core.Popen", autospec=True)
@patch("edgetest.utils.Popen", autospec=True)
def test_mamba_create(mock_popen, mock_cpopen):
    """Test running ``edgetest`` with ``mamba``."""
    mock_popen.return_value.communicate.return_value = (PIP_LIST_MAMBA, "error")
    type(mock_popen.return_value).returncode = PropertyMock(return_value=0)
    mock_cpopen.return_value.communicate.return_value = ("output", "error")
    type(mock_cpopen.return_value).returncode = PropertyMock(return_value=0)

    runner = CliRunner()

    with runner.isolated_filesystem() as loc:
        with open("config.ini", "w") as outfile:
            outfile.write(CFG)

        result = runner.invoke(cli, ["--config=config.ini"])

    assert result.exit_code == 0

    env_loc = str(Path(loc) / ".edgetest" / "myenv")
    if platform.system() == "Windows":
        py_loc = str(Path(env_loc)  / "Scripts" / "python")
    else:
        py_loc = str(Path(env_loc)  / "bin" / "python")

    assert mock_popen.call_args_list == [
        call(
            ("conda", "list", "--json"),
            stdout=-1,
            universal_newlines=True,
        ),
        call(
            ("mamba", "create", "-p", env_loc, "python=3.8", "--yes"),
            stdout=-1,
            universal_newlines=True
        ),
        call(
            ("mamba", "install", "-p", env_loc, "graphviz", "--yes"),
            stdout=-1,
            universal_newlines=True
        ),
        call(
            (f"{py_loc}", "-m", "pip", "install", "."),
            stdout=-1,
            universal_newlines=True,
        ),
        call(
            (f"{py_loc}", "-m", "pip", "install", "myupgrade", "--upgrade"),
            stdout=-1,
            universal_newlines=True,
        ),
        call(
            (f"{py_loc}", "-m", "pip", "list", "--format", "json"),
            stdout=-1,
            universal_newlines=True,
        ),
    ]
    assert mock_cpopen.call_args_list == [
        call(
            (f"{py_loc}", "-m", "pytest", "tests", "-m", "not integration"),
            universal_newlines=True,
        )
    ]

    assert result.output == TABLE_OUTPUT