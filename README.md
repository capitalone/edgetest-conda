# Conda edgetest plugin

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/edgetest-conda)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPI version](https://badge.fury.io/py/edgetest-conda.svg)](https://badge.fury.io/py/edgetest-conda)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/edgetest-conda/badges/version.svg)](https://anaconda.org/conda-forge/edgetest-conda)

[Full Documentation](https://capitalone.github.io/edgetest-conda/)

Table Of Contents
-----------------

- [Install](#install)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

Install
-------

Installation from PyPI:

```console
$ python -m pip install edgetest-conda
```

Installation from conda-forge:

```console
$ conda install -c conda-forge edgetest-conda
```



**NOTE**: This plugin uses ``conda create ...``, so you need to be in a ``conda`` base environment
or you must run

```console
$ conda install conda
```

in your current environment.

Getting Started
---------------

This plugin allows users to create virtual environments using ``conda`` instead of ``venv``.
With this plugin installed, you can also specify packages that you want to install via ``conda``
as well as the python version for your environment(s):

```ini
[edgetest.envs.myenv]
conda_install =
    graphviz
python_version = 3.10
upgrade =
    myupgrade
```

**NOTE**: The default python version is 3.10.


Contributing
------------

See our [developer documentation](https://capitalone.github.io/edgetest-conda/developer.html).

We welcome and appreciate your contributions! Before we can accept any contributions, we ask that you please be sure to
sign the [Contributor License Agreement (CLA)](https://cla-assistant.io/capitalone/edgetest-conda)

This project adheres to the [Open Source Code of Conduct](https://developer.capitalone.com/resources/code-of-conduct/).
By participating, you are expected to honor this code.

License
-------

Apache-2.0
