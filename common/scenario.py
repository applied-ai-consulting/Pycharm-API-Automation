import ast
import re
import json
from common.constants import *
from common.utilities import convert_key_value_dict_list_to_dict, \
    get_pre_and_post_request_event_list_of_exec_list, \
    expand_item_dict_list, merge_two_dicts, get_data_file_path
from common.test_logger import TestLogger
from common.scenario_set import ScenarioSet
from common.test_config import TestConfig


class Scenario(object):
    """
    Scenario class contains scenario JSON object and its methods.
    """

    # Private attributes
    _scenario_json_file = None
    _scenario_json = None
    _scenario_var_dict = None
    _name = None
    _description = None
    _pre_request_event_list_of_exec_list = None
    _post_request_event_list_of_exec_list = None

    # Constructor
    def __init__(self, scenario_json_file):
        """
        Scenario object constructor

        Args:
            scenario_json_file (str): A scenario file in JSON format

        Returns:
            object: Scenario object.
        """
        # Load scenario JSON file
        with open(scenario_json_file, "r") as json_file:
            self._scenario_json = json.load(json_file)
        # Extract additional info needed for this class
        self._scenario_json_file = scenario_json_file
        if self._scenario_json:
            if VAR_KEY in self._scenario_json:
                self._scenario_var_dict = convert_key_value_dict_list_to_dict(self._scenario_json[VAR_KEY])
            if INFO_KEY in self._scenario_json:
                info_dict = self._scenario_json[INFO_KEY]
                if NAME_KEY in info_dict:
                    self._name = info_dict[NAME_KEY]
                if DESC_KEY in info_dict:
                    self._description = info_dict[DESC_KEY]
            # Split pre-request and post-request (test) events with their exec steps
            self._pre_request_event_list_of_exec_list, self._post_request_event_list_of_exec_list = \
                get_pre_and_post_request_event_list_of_exec_list(self._scenario_json)

    def __str__(self):
        """
        Scenario object string representation..

        Returns:
            str: String representation of scenario object.
        """
        return f"\nSCENARIO object:\n" \
               f"\tname: {self._name}\n" \
               f"\tdescription: {self._description}\n" \
               f"\tscenario_var_dict: {self._scenario_var_dict}\n" \
               f"\titem_dict_list: {self.get_item_dict_list()}\n" \
               f"\tpre_request_event_list_of_exec_list: {self._pre_request_event_list_of_exec_list}\n" \
               f"\tpost_request_event_list_of_exec_list: {self._post_request_event_list_of_exec_list}"

    # Public methods
    def get_scenario_json(self):
        """
        Get the scenario JSON object

        Returns:
            json: Scenario JSON object.
        """
        return self._scenario_json

    def get_description(self):
        """
        Get the description of scenario JSON object

        Returns:
            str: Description of scenario JSON object.
        """
        desc = None
        if self._scenario_json:
            info_dict = self._scenario_json[INFO_KEY]
            if DESC_KEY in info_dict:
                desc = info_dict[DESC_KEY]
        return desc

    def expand_item_dict_list(self):
        """
        Expand the list of item dictionaries of scenario JSON object

        Returns:
            Void.
        """
        data_file_path = get_data_file_path(self._scenario_json_file)
        if ITEM_KEY in self._scenario_json:
            # Merge environment and scenario var dict into a single dict
            merged_var_dict = merge_two_dicts(TestConfig.get_environment_var_dict(),
                                              self._scenario_var_dict)
            # Update scenario json with the expanded item dict list in case scenario file references exist.
            self._scenario_json[ITEM_KEY] = \
                expand_item_dict_list(TestConfig,
                                      ScenarioSet,
                                      TestLogger,
                                      self,
                                      data_file_path,
                                      merged_var_dict,
                                      self._scenario_json[ITEM_KEY],
                                      [self._scenario_json_file])

    def get_item_dict_list(self):
        """
        Get the list of item dictionaries of scenario JSON object

        Returns:
            list: List of item dictionaries of scenario JSON object.
        """
        item_dict_list = []
        if ITEM_KEY in self._scenario_json:
            return self._scenario_json[ITEM_KEY]
        return item_dict_list

    def get_scenario_var_dict(self):
        """
        Get the scenario variable dictionary

        Returns:
            dict: Scenario variable dictionary
        """
        return self._scenario_var_dict

    def get_pre_request_event_list_of_exec_list(self):
        """
        Get pre-request event list of exec list

        Returns:
            list: Pre-request event list of exec list
        """
        return self._pre_request_event_list_of_exec_list

    def get_post_request_event_list_of_exec_list(self):
        """
        Get post-request event list of exec list

        Returns:
            list: Post-request event list of exec list
        """
        return self._post_request_event_list_of_exec_list

    def get_scenario_var_value(self, var_name):
        """
        Get the value of a scenario variable

        Args:
            var_name(str): Scenario variable name

        Returns:
            str: Scenario variable value
        """
        return self._scenario_var_dict[var_name]

    def set_scenario_var_value(self, var_name, var_value):
        """
        Set the value of a scenario variable if variable exists

        Args:
            var_name(str): Scenario variable name
            var_value(str): Scenario variable value

        Returns:
            Void
        """
        if var_name in self._scenario_var_dict:
            self._scenario_var_dict[var_name] = var_value

    def add_actual_response_dict_list_to_item(self, item_index, actual_response_dict_list):
        """
        Add an actual response to an item into the scenario JSON via its index

        Args:
            item_index(int): Item index
            actual_response_dict_list(obj): List of actual response dictionaries

        Returns:
            Void
        """
        TestLogger.scenario_logger_obj.debug(
            f"\n\titem_index: {item_index}"
            f"\n\tactual_response_dict_list: {actual_response_dict_list}")
        self._scenario_json[ITEM_KEY][item_index][RESPONSE_KEY] = actual_response_dict_list

    def create_scenario_file_with_expected_responses(self):
        """
        Create a scenario file with expected response(s) only if the scenario JSON file
        contains Postman collection extension '.postman_collection'.

        Returns:
            Void
        """
        if re.search(POSTMAN_COLLECTION_FILE_EXT, self._scenario_json_file):
            # Remove the Postman collection extension from the scenario file name
            scenario_with_expected_responses_json_file = self._scenario_json_file
            scenario_with_expected_responses_json_file =\
                scenario_with_expected_responses_json_file.replace(
                    POSTMAN_COLLECTION_FILE_EXT,
                    ""
                )
            # Dump the JSON with actual responses to the file
            TestLogger.scenario_logger_obj.debug(
                f"\n\tScenario file with expected response(s): '{scenario_with_expected_responses_json_file}'")
            json_file = open(scenario_with_expected_responses_json_file, "w")
            json.dump(self._scenario_json, json_file)
            json_file.close()

    def eval_scenario_var_value(self, var_value):
        """
        Evaluate for data type of a scenario variable to be 'list' or 'dict'

        Args:
            var_value(str): Scenario variable value

        Returns:
            var_value converted to a 'list' or 'dict' object if type is 'list' or 'dict', else return var_value
        """
        if (var_value[0] == '[' and var_value[-1] == ']') or (var_value[0] == '{' and var_value[-1] == '}'):
            return ast.literal_eval(var_value)
        else:
            return var_value
