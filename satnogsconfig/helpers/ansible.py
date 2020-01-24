"""
Ansible helper module
"""
import subprocess


class Ansible():
    """
    Call Ansible playbooks
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, ansible_dir):
        """
        Class constructor
        """
        self._ansible_dir = ansible_dir

    def run(self, playbooks, tags=None, extra_args=None):
        """
        Run Ansible playbook

        :param tags: List of tags
        :type tags: list
        :param playbooks: List of playbooks
        :type playbooks: list
        :param extra_args: List of extra arguments to pass to Ansible
        :type extra_args: list
        :return: Whether Ansible execution succeeded
        :rtype: bool
        """

        args = []
        if extra_args:
            args += extra_args
        if tags:
            args += ['-t', ','.join(tags)]
        if playbooks:
            args += playbooks

        try:
            subprocess.run(
                ['ansible-playbook'] + args, cwd=self._ansible_dir, check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
