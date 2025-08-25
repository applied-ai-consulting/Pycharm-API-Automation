import yaml
import requests
from common.constants import *
from common.test_run_error import *
import datetime
from pytz import timezone


class TestConfig(object):
    """
    TestConfig class contains test configuration YAML object.
    """

    # Private static attributes
    _test_config_yaml = None
    _actual_response_excluded_properties = None
    _environment_var_dict = None
    _requests_session_obj = None
    _log_level = None
    _current_datetime = None

    # Static methods
    @staticmethod
    def load_test_config_yaml(test_config_yaml_file):
        """
        load the test config YAML object.

        Args:
            test_config_yaml_file (str): The test config file name in YAML format

        Returns:
            yaml: Test config YAML object.
        """

        # Load test config YAML file
        if TestConfig._test_config_yaml is None:
            with open(test_config_yaml_file, 'r') as yaml_file:
                TestConfig._test_config_yaml = yaml.safe_load(yaml_file)
            # Set excluded properties in actual response
            if (ACTUAL_RESP_VAL_KEY in TestConfig._test_config_yaml) and \
                    (RESPONSE_BODY_KEY in
                     TestConfig._test_config_yaml[ACTUAL_RESP_VAL_KEY]) and \
                    (EXCLUDED_PROPERTIES_KEY in
                     TestConfig._test_config_yaml[ACTUAL_RESP_VAL_KEY][RESPONSE_BODY_KEY]):
                TestConfig._actual_response_excluded_properties = \
                    TestConfig._test_config_yaml[ACTUAL_RESP_VAL_KEY][RESPONSE_BODY_KEY][EXCLUDED_PROPERTIES_KEY]
        if (ACTUAL_RESP_VAL_KEY in TestConfig._test_config_yaml) and \
                (RESPONSE_BODY_KEY in
                 TestConfig._test_config_yaml[ACTUAL_RESP_VAL_KEY]) and \
                (EXCLUDED_PROPERTIES_KEY in
                 TestConfig._test_config_yaml[ACTUAL_RESP_VAL_KEY][RESPONSE_BODY_KEY]):
            TestConfig._actual_response_excluded_properties = \
                TestConfig._test_config_yaml[ACTUAL_RESP_VAL_KEY][RESPONSE_BODY_KEY][EXCLUDED_PROPERTIES_KEY]
        return TestConfig._test_config_yaml

    @staticmethod
    def get_test_config_yaml():
        """
        Get the test config YAML object.

        Returns:
            yaml: Test config YAML object.
        """
        return TestConfig._test_config_yaml

    @staticmethod
    def get_test_config_name():
        """
        Get test config name.

        Returns:
            str: Test config name
        """
        if NAME_KEY in TestConfig._test_config_yaml:
            return TestConfig._test_config_yaml[NAME_KEY]
        else:
            raise NameKeyDoesNotExistInObject("test config YAML file")

    @staticmethod
    def get_actual_resp_body_excluded_properties():
        """
        Get excluded properties in actual response body.

        Returns:
            list: Excluded properties in actual response body.
        """
        return TestConfig._actual_response_excluded_properties

    @staticmethod
    def get_requests_session_obj():
        """
        Create requests session object.

        Returns:
            Void
        """

        # Get request session
        if TestConfig._requests_session_obj is None:
            TestConfig._requests_session_obj = requests.Session()
        return TestConfig._requests_session_obj

    @staticmethod
    def get_environment_var_dict():
        """
        Get environment variable dictionary and return it.

        Returns:
            dict: Environment variable dictionary
        """
        if TestConfig._test_config_yaml:
            if ENV_VARS_KEY in TestConfig._test_config_yaml and TestConfig._environment_var_dict is None:
                TestConfig._environment_var_dict = TestConfig._test_config_yaml[ENV_VARS_KEY]
        return TestConfig._environment_var_dict

    @staticmethod
    def set_environment_var_value(var_name, var_value):
        """
        Set the value of an environment variable if variable exists

        Args:
            var_name(str): Environment variable name
            var_value(str): Environment variable value

        Returns:
            Void
        """
        if var_name in TestConfig._environment_var_dict:
            TestConfig._environment_var_dict[var_name] = var_value

    @staticmethod
    def get_current_datetime():
        """
        Get the value of _current_datetime variable
        Returns: Current datetime if _current_datetime is null else value of _current_datetime

        """
        if TestConfig._current_datetime is None:
            return datetime.datetime.now(timezone(DATETIME_DEFAULT_TIMEZONE))
        else:
            return TestConfig._current_datetime

    @staticmethod
    def set_current_datetime(date_time):
        """
        Set value for _current_datetime variable
        Args:
            date_time(str): Datetime value to be set to _current_datetime variable

        Returns:

        """
        TestConfig._current_datetime = date_time
