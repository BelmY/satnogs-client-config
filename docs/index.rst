SatNOGS Config utility
======================

SatNOGS Config is a utility for generating the configuration for a Debian-based SatNOGS client system.
It is a menu driven configuration tool built on-top of ``pythondialog``.
The main purpose of this utility is to create the YAML configuration file for SatNOGS Client Ansible which provisions the system.
In addition to that, it interacts with ``satnogs-setup``, which is a wrapper to bootstrap Ansible, upgrades the system packages using APT and probes the hardware to show the user a more limited set of configuration options.

Table of Contents
=================

.. toctree::
   :maxdepth: 4

   userguide
   devguide
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
