import yaml
import glob
import os
from collections import OrderedDict
from common.constants import *
from common.test_run_error import *


class ScenarioSet(object):
    """
    ScenarioSet class contains scenario set YAML object.
    """

    # Private static attributes
    _scenario_set_yaml = None

    # Static methods
    @staticmethod
    def load_scenario_set_yaml(scenario_set_yaml_file):
        """
        Load the scenario set YAML file.

        Args:
            scenario_set_yaml_file (str): The scenario set file name in YAML format

        Returns:
            yaml: Scenario set YAML object.
        """
        abs_path = os.path.dirname(os.path.abspath(__file__))
        if ScenarioSet._scenario_set_yaml is None:
            with open(abs_path + "/../" + scenario_set_yaml_file, 'r') as yaml_file:
                ScenarioSet._scenario_set_yaml = yaml.safe_load(yaml_file)
        return ScenarioSet._scenario_set_yaml

    @staticmethod
    def get_scenario_set_yaml():
        """
        Get scenario set YAML object.

        Returns:
            yaml: Scenario set YAML obj
        """
        return ScenarioSet._scenario_set_yaml

    @staticmethod
    def get_scenario_files(scenario_set_yaml_file):
        """
        Get unique and alphabetically sorted list of scenario files based on
        the collection set patterns specified in a scenario set YAML file.

        Args:
            scenario_set_yaml_file (str): The scenario set file name in YAML format

        Returns:
            list: A unique and alphabetically list of strings representing scenario files.
        """
        # Load scenario set YAML file
        scenario_set_yaml = ScenarioSet.load_scenario_set_yaml(scenario_set_yaml_file)

        # Retrieve scenario set patterns and merge their globbed files
        scenario_files = []

        # Check if data_dir key is specified
        if (DATA_DIR_KEY in scenario_set_yaml):
            data_path = DATA_PATH + scenario_set_yaml[DATA_DIR_KEY]
            # Check if patterns key is specified
            if (PATTERNS_KEY in scenario_set_yaml):
                scenario_set_patterns = scenario_set_yaml[PATTERNS_KEY]
                for pattern in scenario_set_patterns:
                    glob_pattern = data_path + "/**/" + pattern + JSON_FILE_EXT
                    scenario_files = scenario_files + glob.glob(glob_pattern, recursive=True)
                # Remove duplicates from the list and sort it
                scenario_files = list(OrderedDict.fromkeys(scenario_files))

        # Check if data_dirs key is specified
        if (DATA_DIRS_KEY in scenario_set_yaml):
            data_dir_dict_list = scenario_set_yaml[DATA_DIRS_KEY]
            for data_dir_dict in data_dir_dict_list:
                data_dir_scenario_files = []
                if (DATA_DIR_KEY in data_dir_dict):
                    data_path = DATA_PATH + data_dir_dict[DATA_DIR_KEY]
                    if (PATTERNS_KEY in data_dir_dict):
                        data_dir_scenario_set_patterns = data_dir_dict[PATTERNS_KEY]
                        for pattern in data_dir_scenario_set_patterns:
                            glob_pattern = data_path + "/**/" + pattern + JSON_FILE_EXT
                            data_dir_scenario_files = \
                                data_dir_scenario_files + glob.glob(glob_pattern, recursive=True)
                        # Remove duplicates from the list and sort it
                        data_dir_scenario_files = \
                            list(OrderedDict.fromkeys(data_dir_scenario_files))

                if (data_dir_scenario_files):
                    # Append scenario files found in a data dir to the result
                    for data_dir_scenario_file in data_dir_scenario_files:
                        scenario_files.append(data_dir_scenario_file)

        # The order of the scenario files will remain as it's specified in the scenario set's patterns
        return scenario_files

    @staticmethod
    def get_scenario_set_name():
        """
        Get scenario set name.

        Returns:
            str: Scenario set name
        """
        if NAME_KEY in ScenarioSet._scenario_set_yaml:
            return ScenarioSet._scenario_set_yaml[NAME_KEY]
        else:
            raise NameKeyDoesNotExistInObject("scenario set YAML file")
