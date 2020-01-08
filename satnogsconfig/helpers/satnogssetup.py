"""
satnogs-setup module
"""
import subprocess
from pathlib import Path

import satnogsconfig.settings as settings


class SatnogsSetup():
    """
    Interract with satnogs-setup
    """
    def __init__(self):
        """
        Class constructor
        """
        self._tags = set()
        self._satnogs_stamp_dir = settings.SATNOGS_SETUP_STAMP_DIR
        self._satnogs_upgrade_script = settings.SATNOGS_SETUP_UPGRADE_SCRIPT

    def request_bootstrap(self):
        """
        Request bootstrapping from satnog-setup
        """
        try:
            Path(self._satnogs_stamp_dir
                 ).joinpath(settings.SATNOGS_SETUP_BOOTSTRAP_STAMP).unlink()
        except FileNotFoundError:
            pass

    def set_tags(self, tags):
        """
        Set satnogs-setup tag
        """
        self._tags.update(tags)
        tags_path = Path(self._satnogs_stamp_dir
                         ).joinpath(settings.SATNOGS_SETUP_INSTALL_STAMP)
        if tags_path.exists():
            with tags_path.open(mode='w') as file:
                file.write(','.join(self._tags))

    def upgrade_system(self):
        """
        Upgrade system packages
        """
        subprocess.run(self._satnogs_upgrade_script, shell=True, check=True)

    @property
    def satnogs_client_ansible_version(self):
        """
        Get installed SatNOGS Client Ansible version
        """
        raise NotImplementedError

    @property
    def satnogs_client_version(self):
        """
        Get installed SatNOGS Client version
        """
        raise NotImplementedError
