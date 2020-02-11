"""
SatNOGS support info module
"""
import json
import platform

import psutil

import satnogsconfig.helpers.apt as apt
from satnogsconfig._version import get_versions

__version__ = get_versions()['version']

del get_versions


class Support():
    """
    Create support information to be used for reporting bugs
    """
    def __init__(self, config, satnogs_setup, ansible):
        """
        Class constructor
        """
        self._config = config
        self._satnogs_setup = satnogs_setup
        self._ansible = ansible

    @property
    def info(self):
        """
        Support information

        :return: Support information dictionary
        :rtype: dict
        """
        data = {
            "versions":
                {
                    "satnogs-client":
                        self._satnogs_setup.satnogs_client_version,
                    "satnogs-client-ansible":
                        self._satnogs_setup.satnogs_client_ansible_version,
                    "gr-satnogs": self._satnogs_setup.gr_satnogs_version,
                    "satnogs-config": __version__,
                },
            "state":
                {
                    "is-applied": self._satnogs_setup.is_applied,
                    "pending-tags": self._satnogs_setup.tags,
                },
            "system":
                {
                    "distribution": apt.get_distro(),
                    "pending-updates": apt.has_updates(),
                    "platform": dict(platform.uname()._asdict()),
                    "memory": dict(psutil.virtual_memory()._asdict()),
                    "disk": dict(psutil.disk_usage('/')._asdict()),
                },
            "configuration": self._config.config,
        }
        return data

    def dump(self, *args, **kwargs):
        """
        Dump support information

        :return: JSON dump of support information
        :rtype: str
        """
        return json.dumps(self.info, *args, **kwargs)