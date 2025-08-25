import os
import logging
from pathlib import Path
from common.constants import *
from common.utilities import get_file_name_without_extension
from common.scenario_set import ScenarioSet
from common.test_config import TestConfig


class TestLogger(object):
    """
    TestLogger class
    """

    # Public static attributes
    test_log_dir_path = None
    test_logger_obj = None
    scenario_logger_obj = None
    formatter_obj = None
    test_log_file_handler_obj = None
    scenario_log_file_handler_obj = None
    api_calls_dict = {}

    # Static methods
    @staticmethod
    def init_test_and_scenario_logger_obj(debug_test_flag):
        """
        Initialize test and scenario logger object.

        Args:
            debug_test_flag (bool): Debug test flag. True or False.
        Returns:
            Void
        """
        # Create a formatter
        if TestLogger.formatter_obj is None:
            TestLogger.formatter_obj = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(message)s")

        if TestLogger.test_logger_obj is None:
            TestLogger.test_logger_obj = logging.getLogger(TEST_LOGGER_NAME)
            if debug_test_flag:
                TestLogger.test_logger_obj.setLevel(logging.DEBUG)
            else:
                TestLogger.test_logger_obj.setLevel(logging.INFO)

        if TestLogger.scenario_logger_obj is None:
            TestLogger.scenario_logger_obj = logging.getLogger(SCENARIO_LOGGER_NAME)
            if debug_test_flag:
                TestLogger.scenario_logger_obj.setLevel(logging.DEBUG)
            else:
                TestLogger.scenario_logger_obj.setLevel(logging.INFO)

    # Static methods
    @staticmethod
    def create_test_log_file_handler(test_config_yaml_file_name):
        """
        Create test log file handler based on the test config YAML file name.
        A test log file will be created under logs/ directory, e.g.
        logs/<test-config-file>.log.

        Args:
            test_config_yaml_file_name(str): Test config YAML file name.
        Returns:
            Void
        """
        # Build test log dir path based on the name in test_config and scenario_set YAML file
        test_config_name = TestConfig.get_test_config_name()
        test_log_dir_path = os.path.join(LOGS_PATH, test_config_name + "." + ScenarioSet.get_scenario_set_name())
        Path(test_log_dir_path).mkdir(parents=True, exist_ok=True)

        TestLogger.test_log_dir_path = test_log_dir_path

        # Get test config file name
        test_config_file_name = get_file_name_without_extension(test_config_yaml_file_name)
        test_log_file_name = \
            TestLogger.test_log_dir_path + "/" + \
            test_config_file_name + \
            LOG_FILE_EXT

        TestLogger.test_log_file_handler_obj = logging.FileHandler(test_log_file_name,
                                                                   mode='w')
        TestLogger.test_log_file_handler_obj.setFormatter(TestLogger.formatter_obj)
        TestLogger.test_logger_obj.addHandler(TestLogger.test_log_file_handler_obj)
        TestLogger.test_logger_obj.info(f"Test log file handler for '{test_log_file_name} created.")

    @staticmethod
    def remove_test_log_file_handler():
        """
        Remove test log file handler from test logger.

        Returns:
            Void
        """
        if TestLogger.test_log_file_handler_obj:
            TestLogger.test_log_file_handler_obj.close()
            TestLogger.test_logger_obj.removeHandler(TestLogger.test_log_file_handler_obj)

    @staticmethod
    def create_scenario_log_file_handler(scenario_json_file_name):
        """
        Create scenario log file handler based on the scenario JSON file name.
        A scenario log file will be created under the logs/ directory and
        the same directory path as its corresponding scenario JSON file, e.g.
        logs/<api-path>/<feature>/<scenario-file>.log

        Args:
            scenario_json_file_name(str): Scenario JSON file name.

        Returns:
            Void
        """
        # Build list of parent dir names based on the scenario JSON file.
        # Note that file is under data/ directory
        parent_dir_name_list = []
        json_file_path = os.path.dirname(scenario_json_file_name)
        while not (json_file_path == DATA_PATH[0:-1]):
            base_name = os.path.basename(json_file_path)
            parent_dir_name_list.insert(0, base_name)
            json_file_path = os.path.dirname(json_file_path)
        TestLogger.test_logger_obj.info(
            f"Building list of parent dir names based on scenario JSON file name.\n"
            f"\tScenario JSON file: '{scenario_json_file_name}'\n"
            f"\tParent directory name list: {parent_dir_name_list}")

        # Under logs/, check parent dir name path's existence and create one
        # if it doesn't exist
        parent_dir_path = TestLogger.test_log_dir_path
        for parent_dir_name in parent_dir_name_list:
            parent_dir_path = os.path.join(parent_dir_path, parent_dir_name)
            # Create directory first
            Path(parent_dir_path).mkdir(parents=True, exist_ok=True)

        # Build scenario log file name based on the scenario JSON file
        test_data_path = DATA_PATH[0:-1]
        scenario_log_file_name = scenario_json_file_name.replace(test_data_path,
                                                                 TestLogger.test_log_dir_path)
        scenario_log_file_name = scenario_log_file_name.replace(JSON_FILE_EXT, LOG_FILE_EXT)

        TestLogger.test_logger_obj.info(f"Creating scenario file handler for '{scenario_log_file_name}'.")
        TestLogger.scenario_log_file_handler_obj = logging.FileHandler(scenario_log_file_name,
                                                                       mode='w')
        TestLogger.scenario_log_file_handler_obj.setFormatter(TestLogger.formatter_obj)
        TestLogger.scenario_logger_obj.addHandler(TestLogger.scenario_log_file_handler_obj)

    @staticmethod
    def remove_scenario_log_file_handler():
        """
        Remove scenario log file handler from scenario logger.

        Returns:
            Void
        """
        if TestLogger.scenario_log_file_handler_obj:
            TestLogger.scenario_log_file_handler_obj.close()
            TestLogger.scenario_logger_obj.removeHandler(TestLogger.scenario_log_file_handler_obj)

    @staticmethod
    def add_request_url_to_api_calls_dict(request_method, request_url):
        """
        Add (prepared) request URL to API calls dictionary and increment its occurrence.

        Args:
            request_method(str) Request method.
            request_url(str): Prepared request URL.

        Returns:
            Void.
        """
        # Construct dict key
        api_calls_dict_key = request_method + SPACE_CHAR + request_url
        # Update dict
        if api_calls_dict_key in TestLogger.api_calls_dict:
            TestLogger.api_calls_dict[api_calls_dict_key] += 1
        else:
            TestLogger.api_calls_dict[api_calls_dict_key] = 1
