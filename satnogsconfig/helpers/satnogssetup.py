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
        self.tags = []
        self._satnogs_stamp_dir = settings.SATNOGS_SETUP_STAMP_DIR
        self._satnogs_upgrade_script = settings.SATNOGS_SETUP_UPGRADE_SCRIPT

    def request_bootstrap(self):
        """
        Request bootstrapping from satnog-setup
        """
        try:
            Path.joinpath(  # pylint: disable=no-member
                self._satnogs_stamp_dir, settings.SATNOGS_SETUP_BOOTSTRAP_STAMP
            ).unlink()
        except FileNotFoundError:
            pass

    def request_setup(self):
        """
        Request installation from satnogs-setup
        """
        try:
            Path.joinpath(  # pylint: disable=no-member
                self._satnogs_stamp_dir, settings.SATNOGS_SETUP_INSTALL_STAMP
            ).unlink()
        except FileNotFoundError:
            pass

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
