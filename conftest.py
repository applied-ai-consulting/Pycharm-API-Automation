import pytest
import csv
from common.constants import *
from common.test_config import TestConfig
from common.scenario_set import ScenarioSet
from common.test_logger import TestLogger


def pytest_addoption(parser):
    """
    Adding custom pytest option --test-config-file and --generate-scenario-file

    Args:
        parser: Builtin pytest parser object
    """
    parser.addoption("--test-config-file",
                     action="store",
                     default=DEFAULT_TEST_CONFIG_YAML_FILE_NAME,
                     help="Test config file name in YAML format.")
    parser.addoption("--scenario-set-file",
                     action="store",
                     default=DEFAULT_SCENARIO_SET_YAML_FILE_NAME,
                     help="scenario config file name in YAML format.")
    parser.addoption("--debug-test",
                     action="store_true",
                     help="Add debug information to scenario test run log files.")


@pytest.fixture(scope="session",
                params=ScenarioSet.get_scenario_files("configs/scenario_set.yaml")
                )
def scenario_file(request):
    """ Fixture for scenario_file

    Parameterized fixture for scenario_file with args:
        scope: session
        params: list of collection files from ScenarioSet.get_scenario_files('configs/scenario_set.yaml')

    Args:
        request: Builtin pytest request object

    Returns:
        str: request.param which contains a scenario file
    """
    # Define scenario_file finalizer
    def scenario_file_finalizer():
        TestLogger.test_logger_obj.info(f"Executing finalizer.")

        # Write api_calls_dict to a CSV file
        if TestLogger.test_log_dir_path is not None:
            api_calls_csv_filename = TestLogger.test_log_dir_path + \
                "/" + DEFAULT_API_CALLS_CSV_FILE_NAME
            TestLogger.test_logger_obj.info(f"Write API calls to file '{api_calls_csv_filename}'.")
            with open(api_calls_csv_filename, mode='w') as api_calls_csv_file:
                api_calls_csv_writer = csv.writer(api_calls_csv_file)
                for api_call_key in sorted(TestLogger.api_calls_dict):
                    api_calls_csv_writer.writerow([api_call_key, TestLogger.api_calls_dict[api_call_key]])

        # Close request session object
        requests_session_obj = TestConfig.get_requests_session_obj()
        if requests_session_obj:
            TestLogger.test_logger_obj.info(f"Closing requests session object.")
            requests_session_obj.close()
        # Remove log handlers starting from the scenario file handler first
        if TestLogger.scenario_log_file_handler_obj:
            TestLogger.test_logger_obj.info(f"Removing scenario log handler object.")
            TestLogger.remove_scenario_log_file_handler()
        if TestLogger.test_log_file_handler_obj:
            TestLogger.test_logger_obj.info(f"Removing test log file handler object.")
            TestLogger.remove_test_log_file_handler()

    # Add fixture finalizer
    request.addfinalizer(scenario_file_finalizer)

    # This is the start of pytest API test framework code.
    # Try it. If any exception occurs, log it, and perform clean up by calling its finalizer.
    try:
        # Get custom option --test-config-file and initialize it
        test_config_yaml_file = str(request.config.getoption("--test-config-file"))
        # Load test config YAML file
        TestConfig.load_test_config_yaml(CONFIGS_PATH + test_config_yaml_file)

        # Get custom option --debug-test
        debug_test_flag = request.config.getoption("--debug-test")
        # Initialize test logger and get it
        TestLogger.init_test_and_scenario_logger_obj(debug_test_flag)
        # Create test log file handler
        TestLogger.create_test_log_file_handler(test_config_yaml_file)
        # Log above activities
        if not(TestConfig.get_test_config_yaml() is None):
            TestLogger.test_logger_obj.info(f"Test config YAML file '{CONFIGS_PATH}{test_config_yaml_file}' loaded.")

        # Get request session
        if not(TestConfig.get_requests_session_obj() is None):
            TestLogger.test_logger_obj.info(f"Requests session object created.")

    # Intercept any exception and log it with the current scenario logger
    except Exception as any_exception:
        TestLogger.test_logger_obj.error(any_exception)
        raise

    # Clean up
    finally:
        scenario_file_finalizer()

    # Pass a scenario file to tests
    return request.param
