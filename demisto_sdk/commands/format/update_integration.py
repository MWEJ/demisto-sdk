from typing import List
from demisto_sdk.commands.common.constants import BANG_COMMAND_NAMES
from demisto_sdk.commands.common.tools import print_color, LOG_COLORS
from demisto_sdk.commands.format.update_generic_yml import BaseUpdateYML
from demisto_sdk.commands.common.hook_validations.integration import IntegrationValidator


class IntegrationYMLFormat(BaseUpdateYML):
    """IntegrationYMLFormat class is designed to update integration YML file according to Demisto's convention.

        Attributes:
            input (str): the path to the file we are updating at the moment.
            output (str): the desired file name to save the updated version of the YML to.
    """
    ARGUMENTS_DESCRIPTION = {
        'insecure': 'Trust any certificate (not secure)',
        'unsecure': 'Trust any certificate (not secure)',
        'proxy': 'Use system proxy settings'
    }

    def __init__(self, input='', output='', path='', from_version=''):
        super().__init__(input, output, path, from_version)

    def update_proxy_insecure_param_to_default(self):
        """Updates important integration arguments names and description."""
        print(F'Updating proxy and insecure/unsecure integration arguments description to default')

        for integration_argument in self.data.get('configuration', {}):
            argument_name = integration_argument.get('name', '')

            if argument_name in self.ARGUMENTS_DESCRIPTION:
                integration_argument['display'] = self.ARGUMENTS_DESCRIPTION[argument_name]

    def set_reputation_commands_basic_argument_as_needed(self):
        """Sets basic arguments of reputation commands to be default, isArray and required."""
        print(F'Updating reputation commands\' basic arguments to be True for default, isArray and required')

        integration_commands = self.data.get('script', {}).get('commands', [])

        for command in integration_commands:
            command_name = command.get('name', '')
            current_command_default_argument_changed = False

            if command_name in BANG_COMMAND_NAMES:
                for argument in command.get('arguments', []):
                    if argument.get('name', '') == command_name:
                        argument.update({
                            'default': True,
                            'isArray': True,
                            'required': True
                        })
                        current_command_default_argument_changed = True
                        break

                if not current_command_default_argument_changed:
                    argument_list = command.get('arguments', [])  # type: List
                    argument_list.append(
                        {
                            'default': True,
                            'description': '',
                            'isArray': True,
                            'name': command_name,
                            'required': True,
                            'secret': False
                        }
                    )

                    command['arguments'] = argument_list

    def format_file(self):
        """Manager function for the integration YML updater."""
        super().update_yml()

        print_color(F'========Starting updates for integration: {self.source_file}=======', LOG_COLORS.YELLOW)
        self.update_proxy_insecure_param_to_default()
        self.set_reputation_commands_basic_argument_as_needed()
        self.save_yml_to_destination_file()

        print_color(F'========Finished updates for integration: {self.output_file}=======',
                    LOG_COLORS.YELLOW)

        return self.initiate_file_validator(IntegrationValidator)
