"""
satnogs-setup module
"""
import os
import subprocess
import sys
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
        self._satnogs_stamp_dir = settings.SATNOGS_SETUP_STAMP_DIR
        self._satnogs_upgrade_script = settings.SATNOGS_SETUP_UPGRADE_SCRIPT

    @staticmethod
    def restart(boot=False):
        """
        Restart satnogs-setup script

        :param boot: Whether to bootstrap or not
        :type boot: bool, optional
        """
        if boot:
            os.execlp('satnogs-setup', 'satnogs-setup', '-b')
        else:
            os.execlp('satnogs-setup', 'satnogs-setup')

    @property
    def is_applied(self):
        """
        Check whether configuration has been applied

        :return: Whether configuration has been applied
        :rtype: bool
        """
        install_stamp_path = Path(self._satnogs_stamp_dir).joinpath(
            settings.SATNOGS_SETUP_INSTALL_STAMP
        )
        if install_stamp_path.exists():
            with install_stamp_path.open(mode='r') as file:
                contents = file.read()
                if contents:
                    return False
            return True
        return False

    @is_applied.setter
    def is_applied(self, install):
        """
        Mark that configuration has been applied

        :param install: Configuration has been installed
        :type install: bool
        """
        install_stamp_path = Path(self._satnogs_stamp_dir).joinpath(
            settings.SATNOGS_SETUP_INSTALL_STAMP
        )
        if install:
            install_stamp_path.open(mode='w').close()
        else:
            try:
                install_stamp_path.unlink()
            except FileNotFoundError:
                pass

    @property
    def tags(self):
        """
        Get satnogs-setup tags

        :return: Set of tags
        :rtype: set
        """
        tags_path = Path(self._satnogs_stamp_dir
                         ).joinpath(settings.SATNOGS_SETUP_INSTALL_STAMP)
        if tags_path.exists():
            with tags_path.open(mode='r') as file:
                contents = file.read()
                if contents:
                    return set(contents.split(','))
        return None

    @tags.setter
    def tags(self, tags):
        """
        Set satnogs-setup tags

        :param tags: List of tags
        :type tags: list
        """
        if self.tags:
            new_tags = self.tags.copy()
        else:
            new_tags = set()
        new_tags.update(tags)
        tags_path = Path(self._satnogs_stamp_dir
                         ).joinpath(settings.SATNOGS_SETUP_INSTALL_STAMP)
        if tags_path.exists():
            with tags_path.open(mode='w') as file:
                file.write(','.join(new_tags))

    def upgrade_system(self):
        """
        Upgrade system packages
        """
        try:
            subprocess.run(
                self._satnogs_upgrade_script, shell=True, check=True
            )
        except subprocess.CalledProcessError:
            sys.exit(1)

    @property
    def satnogs_client_ansible_version(self):
        """
        Get installed SatNOGS Client Ansible version

        :return: Version of SatNOGS Client Ansible
        :rtype: str
        """
        try:
            result = subprocess.run(
                'cd "$HOME/.satnogs/ansible"'
                '&& git show -s --format=%cd --date="format:%Y%m%d%H%M"',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            return result.stdout.decode('utf-8').strip() or 'unknown'
        except subprocess.CalledProcessError:
            return 'unknown'

    @property
    def satnogs_client_version(self):
        """
        Get installed SatNOGS Client version

        :return: Version of SatNOGS Client
        :rtype: str
        """
        try:
            result = subprocess.run(
                "/var/lib/satnogs/bin/pip show satnogs-client 2>/dev/null"
                " | awk '/^Version: / { print $2 }'",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            return result.stdout.decode('utf-8').strip() or 'unknown'
        except subprocess.CalledProcessError:
            return 'unknown'

    @property
    def gr_satnogs_version(self):
        """
        Get installed gr-satnogs version

        :return: Version of gr-satnogs
        :rtype: str
        """
        try:
            result = subprocess.run(
                "dpkg-query --show -f='${Version}' gr-satnogs",
                shell=True,
                stdout=subprocess.PIPE,
                check=True
            )
            return result.stdout.decode('utf-8').strip() or 'unknown'
        except subprocess.CalledProcessError:
            return 'unknown'
