"""
Settings module
"""
import os
from pathlib import Path

from dotenv import load_dotenv

try:
    load_dotenv()
except EnvironmentError:
    # XXX: Workaround for readthedocs  # pylint: disable=fixme
    pass

ENV_PREFIX = 'SATNOGS_CONFIG_'

SATNOGS_SETUP_UPGRADE_SCRIPT = os.getenv(
    ENV_PREFIX + 'SATNOGS_SETUP_UPGRADE_SCRIPT', 'satnogs-upgrade'
)
SATNOGS_SETUP_STAMP_DIR = os.getenv(
    ENV_PREFIX + 'SATNOGS_SETUP_STAMP_DIR',
    str(Path.home().joinpath('.satnogs'))
)
SATNOGS_SETUP_BOOTSTRAP_STAMP = os.getenv(
    ENV_PREFIX + 'SATNOGS_SETUP_BOOTSTRAP_STAMP', '.bootstrapped'
)
SATNOGS_SETUP_INSTALL_STAMP = os.getenv(
    ENV_PREFIX + 'SATNOGS_SETUP_INSTALL_STAMP', '.installed'
)
CONFIG_FILE_DIR = os.getenv(
    ENV_PREFIX + 'CONFIG_FILE_DIR', str(Path.home().joinpath('.satnogs'))
)
CONFIG_FILE = os.getenv(ENV_PREFIX + 'CONFIG_FILE', 'config.yml')
