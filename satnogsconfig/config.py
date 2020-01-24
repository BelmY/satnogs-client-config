"""
Configuration module
"""
import logging
from pathlib import Path

import yaml

LOGGER = logging.getLogger(__name__)


class Config():
    """
    Manage configuration file

    :param filename: File path of configuration
    :type filename: str
    """
    def __init__(self, filename):
        """
        Class constructor
        """
        self._filename = filename
        try:
            config = self._load_config()
        except FileNotFoundError:
            config = None
        self.config = config

    def _load_config(self):
        """
        Load and parse YAML configuration

        :return: Configuration dictionary
        :rtype: dict or NoneType
        """
        with open(self._filename, 'r') as file:
            return yaml.safe_load(file)

    def dump_config(self, to_file=False):
        """
        Dump configuration in YAML format

        :param to_file: Dump to file
        :type to_file: bool, optional
        :return: YAML configuration
        :rtype: str
        """
        if to_file:
            Path(self._filename
                 ).parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            with open(self._filename, 'w') as file:
                yaml_config = yaml.dump(
                    self.config, file, default_flow_style=False
                )
            self.config = self._load_config()
        else:
            yaml_config = yaml.dump(self.config, default_flow_style=False)

        return yaml_config

    def clear_config(self):
        """
        Clear configuration file
        """
        open(self._filename, 'w').close()
        self.config = self._load_config()

    def get_variable(self, variable):
        """
        Get variable value from configuration

        :param variable: Variable to get the value
        :type variable: str
        :return: Value of variable
        :rtype: str or bool or NoneType
        """
        if self.config:
            return self.config.get(variable)

        return None

    def set_variable(self, variable, value):
        """
        Set variable value in configuration

        :param variable: Variable to set the value
        :type variable: str
        :param value: Value of variable
        :type value: str or bool or NoneType
        """
        if not self.config:
            self.config = {}
        if value:
            self.config[variable] = value
        else:
            self.config.pop(variable, None)
        self.dump_config(to_file=True)
