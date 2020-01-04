"""
Settings module
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ENV_PREFIX = 'SATNOGS_CONFIG_'

SATNOGS_SETUP_UPGRADE_SCRIPT = os.getenv(
    ENV_PREFIX + 'SATNOGS_SETUP_UPGRADE_SCRIPT', 'satnogs-upgrade'
)
SATNOGS_SETUP_STAMP_DIR = os.getenv(
    ENV_PREFIX + 'SATNOGS_SETUP_STAMP_DIR',
    str(Path.joinpath(Path.home(), '.satnogs'))
)
SATNOGS_SETUP_BOOTSTRAP_STAMP = os.getenv(
    ENV_PREFIX + 'SATNOGS_SETUP_BOOTSTRAP_STAMP', '.bootstrapped'
)
SATNOGS_SETUP_INSTALL_STAMP = os.getenv(
    ENV_PREFIX + 'SATNOGS_SETUP_INSTALL_STAMP', '.installed'
)
