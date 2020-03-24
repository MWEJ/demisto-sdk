import json
from demisto_sdk.commands.common.tools import print_color, LOG_COLORS
from demisto_sdk.commands.common.constants import DEFAULT_VERSION
from demisto_sdk.commands.format.update_generic import BaseUpdate


class BaseUpdateJSON(BaseUpdate):
    """BaseUpdateJSON is the base class for all json updaters.
        Attributes:
            input (str): the path to the file we are updating at the moment.
            output (str): the desired file name to save the updated version of the YML to.
            data (Dict): JSON file data arranged in a Dict.
    """

    def __init__(self, input: str = '', output: str = '', path: str = '', from_version: str = ''):
        super().__init__(input=input, output=output, path=path, from_version=from_version)

    def set_version_to_default(self):
        """Replaces the version of the YML to default."""
        print(F'Setting JSON version to default: {DEFAULT_VERSION}')

        self.data['version'] = DEFAULT_VERSION

    def set_default_values_as_needed(self, ARGUMENTS_DEFAULT_VALUES):
        """Sets basic arguments of reputation commands to be default, isArray and required."""
        print(F'Updating required default values')
        for field in ARGUMENTS_DEFAULT_VALUES:
            self.data[field] = ARGUMENTS_DEFAULT_VALUES[field]

    def save_json_to_destination_file(self):
        """Save formatted JSON data to destination file."""
        print(F'Saving output JSON file to {self.output_file}')
        with open(self.output_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def update_json(self):
        """Manager function for the generic JSON updates."""
        print_color(F'=======Starting updates for JSON: {self.source_file}=======', LOG_COLORS.YELLOW)

        self.set_version_to_default()
        self.remove_unnecessary_keys()
        self.set_fromVersion(from_version=self.from_version)

        print_color(F'=======Finished generic updates for JSON: {self.output_file}=======', LOG_COLORS.YELLOW)

    def format_file(self):
        pass
