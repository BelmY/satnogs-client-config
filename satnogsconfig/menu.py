"""
Menu module
"""

import logging
import subprocess
import sys

import yaml
from dialog import Dialog

import satnogsconfig.helpers as helpers

LOGGER = logging.getLogger(__name__)


def _load_menu(file):
    """
    Load menu structure from YAML file

    :param file: Menu file stream
    :type file: file
    :return: Menu dictionary
    :rtype: dict
    """
    try:
        return yaml.safe_load(file)
    except yaml.YAMLError:
        LOGGER.exception("Could not load YAML menu file")


def _clear_screen():
    subprocess.run(['clear'], check=True)


class Menu():
    """
    Show a menu structure based on dialog

    :param menu: Menu dictionary
    :type menu: dict
    :param config: Configuration dictionary
    :type config: dict
    :param backtitle: Default dialog backtitle
    :type backtitle: str, optional
    """
    def __init__(self, menu, config, backtitle=None):
        """
        Class constructor
        """
        self._dialog = Dialog(autowidgetsize=True)
        self.backtitle = backtitle

        self._satnogs_setup = helpers.SatnogsSetup()
        self._types = {
            'submenu': self._submenu,
            'variablebox': self._variablebox,
            'variableyesno': self._variableyesno,
            'configbox': self._configbox,
            'msgbox': self._msgbox,
            'upgrade': self._upgrade,
            'update': self._update,
            'resetyesno': self._resetyesno,
            'apply': self._apply,
        }
        self._stack = [
            _load_menu(menu),
        ]
        self._config = config
        self._defaults = None

    def _get_common_options(self, menu):
        """
        Get dialog common options

        :param menu: Menu dictionary
        :type menu: dict
        :return: Common option dictionary
        :rtype: dict
        """
        common_options = [
            'ascii_lines',
            'aspect',
            'backtitle',
            'begin',
            'colors',
            'cancel_label',
            'default_button',
            'defaultno',
            'default_item',
            'exit_label',
            'extra_button',
            'extra_label',
            'help_button',
            'help_label',
            'help_status',
            'help_tags',
            'hline',
            'insecure',
            'iso_week',
            'item_help',
            'keep_tite',
            'max_input',
            'no_cancel',
            'no_collapse',
            'no_items',
            'no_kill',
            'no_label',
            'no_lines',
            'no_mouse',
            'no_nl_expand',
            'no_ok',
            'no_shadow',
            'no_tags',
            'ok_label',
            'reorder',
            'scrollbar',
            'shadow',
            'sleep',
            'tab_correct',
            'tab_len',
            'time_format',
            'timeout',
            'title',
            'week_start',
            'trim',
            'visit_items',
            'yes_label',
        ]

        if menu.get('defaults'):
            self._defaults = menu['defaults']

        options = self._defaults or {}

        for key in common_options:
            if key in menu:
                options[key] = menu[key]

        return options

    @property
    def backtitle(self):
        """
        Get default backtitle

        :return: Background title
        :rtype: str
        """
        return self.backtitle

    @backtitle.setter
    def backtitle(self, backtitle):
        """
        Set default backtitle

        :param backtitle: Background title
        :type backtitle: str or NoneType
        """
        if backtitle:
            self._dialog.set_background_title(backtitle)

    def show(self):
        """
        Show dialog menu structure
        """
        while True:
            try:
                menu = self._stack.pop()
            except IndexError:
                sys.exit(1)
            self._types[menu['type']](menu)

    def _submenu(self, menu):
        """
        Show submenu

        :param menu: Menu dictionary
        :type menu: dict
        """
        description = menu.get('description') or menu['short_description']
        options = self._get_common_options(menu)
        if not options.get('title'):
            options['title'] = menu['short_description']
        options['choices'] = []

        for key, value in menu['items'].items():
            short_description = value['short_description']

            if value.get('variable'):
                init_value = self._config.get_variable(value['variable'])
                if init_value:
                    short_description += ' [{}]'.format(init_value)

            options['choices'].append((key, short_description))
        response, item = self._dialog.menu(description, **options)
        menu['default_item'] = item

        if response == Dialog.OK:
            self._stack.append(menu)
            self._stack.append(menu['items'][item])

    def _variablebox(self, menu):
        """
        Show inputbox for setting a variable

        :param menu: Menu dictionary
        :type menu: dict
        """
        description = menu.get('description') or menu['short_description']
        tags = menu.get('tags')
        options = self._get_common_options(menu)
        if not options.get('title'):
            options['title'] = menu['short_description']
        options['init'] = self._config.get_variable(menu['variable']) or ''

        response, value = self._dialog.inputbox(description, **options)

        if response == Dialog.OK and value != options['init']:
            self._config.set_variable(menu['variable'], value)
            if tags:
                self._satnogs_setup.set_tags(tags)

    def _variableyesno(self, menu):
        """
        Show boolean selection for setting a variable

        :param menu: Menu dictionary
        :type menu: dict
        """
        description = menu.get('description') or menu['short_description']
        tags = menu.get('tags')
        options = self._get_common_options(menu)
        if not options.get('title'):
            options['title'] = menu['short_description']
        init_value = self._config.get_variable(menu['variable']) or False
        options['defaultno'] = not init_value

        response = (
            self._dialog.yesno(description, **options) == Dialog.OK
        ) or False

        if init_value != response:
            self._config.set_variable(menu['variable'], response)
            if tags:
                self._satnogs_setup.set_tags(tags)

    def _configbox(self, menu):
        """
        Show scrollbox for viewing configuration

        :param menu: Menu dictionary
        :type menu: dict
        """
        options = self._get_common_options(menu)
        if not options.get('title'):
            options['title'] = menu['short_description']

        _ = self._dialog.scrollbox(self._config.dump_config(), **options)

    def _msgbox(self, menu):
        """
        Show msgbox

        :param menu: Menu dictionary
        :type menu: dict
        """
        options = self._get_common_options(menu)
        if not options.get('title'):
            options['title'] = menu['short_description']

        _ = self._dialog.msgbox(menu['message'], **options)

    def _resetyesno(self, menu):
        """
        Reset configuration

        :param menu: Menu dictionary
        :type menu: dict
        """
        description = menu.get('description') or menu['short_description']
        options = self._get_common_options(menu)
        if not options.get('title'):
            options['title'] = menu['short_description']

        response = (
            self._dialog.yesno(description, **options) == Dialog.OK
        ) or False

        if response:
            self._config.clear_config()
            self._satnogs_setup.request_bootstrap()
            sys.exit()

    def _upgrade(self, _):
        """
        Run system upgrade
        """
        _clear_screen()
        self._satnogs_setup.upgrade_system()

    def _update(self, _):
        """
        Request tool update
        """
        _clear_screen()
        self._satnogs_setup.request_bootstrap()
        sys.exit()

    @staticmethod
    def _apply(_):
        """
        Request setup from configuration management tool
        """
        _clear_screen()
        sys.exit()
