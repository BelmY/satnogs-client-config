"""
Menu module
"""

import logging
import subprocess
import sys

import yaml
from dialog import Dialog

import satnogsconfig.helpers as helpers
import satnogsconfig.helpers.apt as apt
import satnogsconfig.settings as settings

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


def _reboot():
    """
    Reboot system
    """
    subprocess.run(['sync'], check=True)
    subprocess.run(['reboot'], check=True)


def _clear_screen():
    """
    Clear screen
    """
    subprocess.run(['clear'], check=True)


def _get_variables(menu, name=None, mandatory=False):
    """
    Get all menu variable items

    :param menu: Menu dictionary
    :type menu: dict
    :param name: Name of menu item
    :type name: str, optional
    :param mandatory: Return only mandatory variables
    :type mandatory: bool
    :return: Menu variables dictionary
    :rtype: dict
    """
    variables = {}
    if menu['type'] == 'submenu':
        for key, value in menu['items'].items():
            variables.update(
                _get_variables(value, name=key, mandatory=mandatory)
            )
    if menu['type'] in ['variablebox', 'variableyesno']:
        if not mandatory or menu.get('mandatory'):
            variables[name] = menu
    return variables


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

    # pylint: disable=too-many-instance-attributes
    def __init__(self, menu, config, backtitle=None):
        """
        Class constructor
        """
        self._dialog = Dialog(autowidgetsize=True)
        self._satnogs_setup = helpers.SatnogsSetup()
        self._ansible = helpers.Ansible(settings.ANSIBLE_DIR)
        if backtitle:
            self.backtitle = backtitle
        else:
            self.backtitle = (
                'SatNOGS client configuration | Installed: '
                'satnogs-client-ansible-{}, '
                'satnogs-client-{}, '
                'gr-satnogs-{}'
            ).format(
                self._satnogs_setup.satnogs_client_ansible_version,
                self._satnogs_setup.satnogs_client_version,
                self._satnogs_setup.gr_satnogs_version
            )

        self._types = {
            'submenu': self._submenu,
            'variablebox': self._variablebox,
            'variableyesno': self._variableyesno,
            'configbox': self._configbox,
            'msgbox': self._msgbox,
            'update': self._update,
            'resetyesno': self._resetyesno,
            'apply': self._apply,
            'support': self._support,
            'reboot': self._reboot,
            'exit': self._exit
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

        options = dict(self._defaults) or {}

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
            menu = self._stack.pop()
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

        if response == Dialog.OK and menu.get('items'):
            self._stack.append(menu)
            self._stack.append(menu['items'][item])
        if response == Dialog.EXTRA and menu.get('extra'):
            self._stack.append(menu)
            self._stack.append(menu['extra'])
        if response == Dialog.CANCEL and menu.get('cancel'):
            self._stack.append(menu)
            self._stack.append(menu['cancel'])

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
        init_value = self._config.get_variable(menu['variable'])
        if init_value is None:
            init_value = ''
        options['init'] = str(init_value)

        response, value = self._dialog.inputbox(description, **options)

        if response == Dialog.OK and value != options['init']:
            self._config.set_variable(menu['variable'], value)
            if tags:
                self._satnogs_setup.tags = tags
        if response == Dialog.EXTRA and menu.get('extra'):
            self._stack.append(menu)
            self._stack.append(menu['extra'])
        if response == Dialog.CANCEL and menu.get('cancel'):
            self._stack.append(menu)
            self._stack.append(menu['cancel'])

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

        response = self._dialog.yesno(description, **options)

        if response == Dialog.CANCEL and menu.get('cancel'):
            self._stack.append(menu)
            self._stack.append(menu['cancel'])
        else:
            if response in [Dialog.OK, Dialog.CANCEL]:
                value = (response == Dialog.OK) or False
                if init_value != value:
                    self._config.set_variable(menu['variable'], value)
                    if tags:
                        self._satnogs_setup.tags = tags
        if response == Dialog.EXTRA and menu.get('extra'):
            self._stack.append(menu)
            self._stack.append(menu['extra'])

    def _configbox(self, menu):
        """
        Show scrollbox for viewing configuration

        :param menu: Menu dictionary
        :type menu: dict
        """
        options = self._get_common_options(menu)
        if not options.get('title'):
            options['title'] = menu['short_description']

        response = self._dialog.scrollbox(
            self._config.dump_config(), **options
        )
        if response == Dialog.EXTRA and menu.get('extra'):
            self._stack.append(menu)
            self._stack.append(menu['extra'])

    def _msgbox(self, menu):
        """
        Show msgbox

        :param menu: Menu dictionary
        :type menu: dict
        """
        options = self._get_common_options(menu)
        if not options.get('title'):
            options['title'] = menu['short_description']

        response = self._dialog.msgbox(menu['message'], **options)
        if menu.get('pop'):
            self._stack.pop()
        if response == Dialog.EXTRA and menu.get('extra'):
            self._stack.append(menu)
            self._stack.append(menu['extra'])

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

        response = self._dialog.yesno(description, **options)

        if response == Dialog.CANCEL and menu.get('cancel'):
            self._stack.append(menu)
            self._stack.append(menu['cancel'])
        else:
            if response in [Dialog.OK, Dialog.CANCEL]:
                value = (response == Dialog.OK) or False
                if value:
                    _clear_screen()
                    self._config.clear_config()
                    self._satnogs_setup.restart(boot=True)
        if response == Dialog.EXTRA and menu.get('extra'):
            self._stack.append(menu)
            self._stack.append(menu['extra'])

    def _update(self, _):
        """
        Request tool update
        """
        _clear_screen()
        self._ansible.pull(
            [settings.ANSIBLE_PLAYBOOK],
            settings.ANSIBLE_URL,
            branch=settings.ANSIBLE_BRANCH,
            tags=['satnogs-setup'],
            extra_args=['-o']
        )
        if apt.has_updates() or apt.get_distro()['CODENAME'] != 'buster':
            self._satnogs_setup.upgrade_system()
        self._satnogs_setup.restart()

    def _apply(self, menu):
        """
        Request setup from configuration management tool
        """
        _clear_screen()
        for value in _get_variables(self._stack[0], mandatory=True).values():
            if self._config.get_variable(value['variable']) is None:
                description = menu.get('description'
                                       ) or menu['short_description']
                options = self._get_common_options(menu)
                if not options.get('title'):
                    options['title'] = menu['short_description']

                response = self._dialog.yesno(description, **options)

                if response == Dialog.CANCEL and menu.get('cancel'):
                    self._stack.append(menu)
                    self._stack.append(menu['cancel'])
                else:
                    if response in [Dialog.OK, Dialog.CANCEL]:
                        value = (response == Dialog.OK) or False
                        if value:
                            break
                        return
                if response == Dialog.EXTRA and menu.get('extra'):
                    self._stack.append(menu)
                    self._stack.append(menu['extra'])
                break
        tags = self._satnogs_setup.tags
        if not self._satnogs_setup.is_applied:
            _clear_screen()
            if self._ansible.run([settings.ANSIBLE_PLAYBOOK], tags=tags):
                self._satnogs_setup.is_applied = True
            else:
                sys.exit(1)

    def _support(self, _):
        """
        Show support information
        """
        _clear_screen()
        sys.stdout.write(
            '------------[ copy here ]------------\n' +
            helpers.Support(self._config, self._satnogs_setup, self._ansible
                            ).dump(indent=4) +
            '\n------------[ copy end ]-------------\n\n'
        )
        input('Press Enter to continue...')

    def _reboot(self, menu):
        """
        Reboot system

        :param menu: Menu dictionary
        :type menu: dict
        """
        description = menu.get('description') or menu['short_description']
        options = self._get_common_options(menu)
        if not options.get('title'):
            options['title'] = menu['short_description']

        response = self._dialog.yesno(description, **options)

        if response == Dialog.CANCEL and menu.get('cancel'):
            self._stack.append(menu)
            self._stack.append(menu['cancel'])
        else:
            if response in [Dialog.OK, Dialog.CANCEL]:
                value = (response == Dialog.OK) or False
                if value:
                    _reboot()
        if response == Dialog.EXTRA and menu.get('extra'):
            self._stack.append(menu)
            self._stack.append(menu['extra'])

    def _exit(self, menu):
        """
        Exit the utility

        :param menu: Menu dictionary
        :type menu: dict
        """
        if self._satnogs_setup.is_applied:
            _clear_screen()
            sys.exit()
        description = menu.get('description') or menu['short_description']
        options = self._get_common_options(menu)
        if not options.get('title'):
            options['title'] = menu['short_description']

        response = self._dialog.yesno(description, **options)

        if response == Dialog.CANCEL and menu.get('cancel'):
            self._stack.append(menu)
            self._stack.append(menu['cancel'])
        else:
            if response in [Dialog.OK, Dialog.CANCEL]:
                value = (response == Dialog.OK) or False
                if value:
                    _clear_screen()
                    sys.exit()
        if response == Dialog.EXTRA and menu.get('extra'):
            self._stack.append(menu)
            self._stack.append(menu['extra'])
