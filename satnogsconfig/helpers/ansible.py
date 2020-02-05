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

        :param playbooks: List of playbooks
        :type playbooks: list
        :param tags: List of tags
        :type tags: list, optional
        :param extra_args: List of extra arguments to pass to Ansible
        :type extra_args: list, optional
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

    def pull(self, playbooks, url, branch=None, tags=None, extra_args=None):
        """
        Pull and run Ansible playbook

        :param playbooks: List of playbooks
        :type playbooks: list
        :param url: Git URL to pull playbooks
        :type url: str
        :param branch: Git branch to pull playbooks
        :type branch: str, optional
        :param tags: List of tags
        :type tags: list, optional
        :param extra_args: List of extra arguments to pass to Ansible
        :type extra_args: list, optional
        :return: Whether Ansible execution succeeded
        :rtype: bool
        """
        # pylint: disable=too-many-arguments
        args = []
        if extra_args:
            args += extra_args
        if tags:
            args += ['-t', ','.join(tags)]
        if playbooks:
            args += playbooks
        if branch:
            args += ['-C', branch]
        try:
            subprocess.run(
                ['ansible-pull', '-d', self._ansible_dir, '-U', url] + args,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
