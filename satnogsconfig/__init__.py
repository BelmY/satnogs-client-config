"""
SatNOGS Setup module initialization
"""
import sys

import pkg_resources

from satnogsconfig.config import CONFIG
from satnogsconfig.menu import Menu

from ._version import get_versions

__version__ = get_versions()['version']

del get_versions

MENU_FILE = 'menu.yml'


def main():
    """
    SatNOGS Setup utility
    """

    menu = Menu(pkg_resources.resource_stream(__name__, MENU_FILE), CONFIG)
    try:
        menu.show()
    except KeyboardInterrupt:
        sys.exit(0)
