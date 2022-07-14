Quick Start
===========

Install
-------

Installation from PyPI:

.. code:: console

    $ python -m pip install edgetest-conda


Installation from conda-forge:

.. code:: console

    $ conda install -c conda-forge edgetest-conda


.. important::

    This package uses ``conda`` to create virtual environments. This means you have to be either
    in the base conda environment or run

    .. code-block:: console

        $ conda install conda

Usage
-----

This plugin allows users to create virtual environments using ``conda`` instead of ``venv``. Once
installed, you don't need to supply any additional configuration options; however, if you want to
install dependencies via ``conda`` instead of ``pip`` or specify a python version for the environment(s),
you will need to modify the configuration file:

.. code-block:: ini

    [edgetest.envs.myenv]
    conda_install =
        graphviz
    python_version = 3.8
    upgrade =
        myupgrade
    update_with_conda = True

.. important::

    If you have `mamba <https://github.com/mamba-org/mamba>`_ installed (via ``conda``) in your
    execution environment, this plugin will use ``mamba`` to create your individual testing
    environments.

``update_with_conda`` is optional. The default behaviour is ``False``. Accepted values are ``True`` or ``False`` if
provided. If ``True`` the update command will be excuted using ``conda``. If ``False`` the update command will be
excuted using the default beahviour using ``pip``.
