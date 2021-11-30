# Conda edgetest plugin

![python-3.7](https://img.shields.io/badge/python-3.7-green.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

[Full Documentation](https://capitalone.github.io/edgetest-conda/)

Table Of Contents
-----------------

- [Install](#install)
- [Getting Started](#getting-started)
- [Options](#options)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

Install
-------

Installation from PyPI:

```console
$ python -m pip install edgetest-conda
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
python_version = 3.8
upgrade =
    myupgrade
```

**NOTE**: The default python version is 3.7.

Contributing
------------
