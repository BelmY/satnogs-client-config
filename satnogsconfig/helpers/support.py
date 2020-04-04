"""
SatNOGS support info module
"""
import json
import platform
from datetime import datetime, timezone

import psutil

from satnogsconfig._version import get_versions
from satnogsconfig.helpers import apt

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
        config = self._config.config.copy()
        redacted_keys = ['satnogs_api_token']
        for key in redacted_keys:
            if config.get(key) is not None:
                config[key] = '[redacted]'
        data = {
            "versions":
                {
                    "satnogs-client":
                        self._satnogs_setup.satnogs_client_version,
                    "satnogs-client-ansible":
                        self._satnogs_setup.satnogs_client_ansible_version,
                    "satnogs-flowgraphs":
                        self._satnogs_setup.satnogs_flowgraphs_version,
                    "gr-satnogs": self._satnogs_setup.gr_satnogs_version,
                    "gr-soapy": self._satnogs_setup.gr_soapy_version,
                    "gnuradio": self._satnogs_setup.gnuradio_version,
                    "satnogs-config": __version__,
                },
            "state":
                {
                    "is-applied": self._satnogs_setup.is_applied,
                    "pending-tags": None,
                },
            "system":
                {
                    "date": datetime.now(timezone.utc).isoformat(),
                    "distribution": apt.get_distro(),
                    "pending-updates": apt.has_updates(),
                    "platform": dict(platform.uname()._asdict()),
                    "memory": dict(psutil.virtual_memory()._asdict()),
                    "disk": dict(psutil.disk_usage('/')._asdict()),
                },
            "configuration": config,
        }

        tags = self._satnogs_setup.tags
        if tags:
            data['state']['pending-tags'] = list(tags)

        return data

    def dump(self, *args, **kwargs):
        """
        Dump support information

        :return: JSON dump of support information
        :rtype: str
        """
        return json.dumps(self.info, *args, **kwargs)
