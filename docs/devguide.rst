Developer guide
===============

Installation
------------

To install the required dependencies in Debian run::

  $ apt-get install python3-apt lsb-release


It is recommended to install SatNOGS Config in a virtualenv.
The virtualenv needs to have access to system Python bindings.
To create the virtualenv, you can use ``virtualenvwrapper``.
On the first time, create the virtualenv by running::

  $ mkvirtualenv --system-site-packages -a . satnogs-config

To activate the virtualenv after it is created run::

  $ workon satnogs-config

To install SatNOGS Config for development run in the project root directory::

  $ pip install -e .


Configuration
-------------

This project uses ``python-dotenv``.
Configuration of ``satnogsconfig/settings.py`` can be overridden by setting the respective environment variables or an ``.env`` file placed on the project root directory.


Extending
---------

SatNOGS Config functionality can be extended by implementing additional helpers.
The helpers are used to enhance menu functionality beyond the core function of generating a YAML file for Ansible.


Modifying the menu
------------------

The menu itself is also expressed in YAML format.
The menu structure is defined in ``menu.yml`` file and shipped along with the package.


Code Quality Assurance
----------------------

The following code quality assurance tools are used in this project:

  * ``flake8``
  * ``isort``
  * ``yapf``
  * ``pylint``


Automation
----------

``tox`` is used to automate development tasks.
To execute the default list of tasks run::

  $ tox
