import time
from common.test_config import TestConfig
from common.scenario import Scenario
from common.item import Item
from common.test_logger import TestLogger
from common.utilities import process_event_list_of_exec_list
from common.test_run_error import ItemProcessingErrorsEncountered


def test_scenario(scenario_file):
    """
    Test runner for a scenario.

    Args:
        scenario_file (str): The scenario file name in JSON format.

    Returns:
        Pass, skip, or xfail
    """
    try:
        # Create scenario test handler and get it
        TestLogger.create_scenario_log_file_handler(scenario_file)
        TestLogger.scenario_logger_obj.info(f"Creating scenario log file handler object for '{scenario_file}'.")
        # TestLogger.scenario_logger_obj.info(f"Path '{update_file_path(scenario_file)}'.")

        # Get the environment variable dictionary
        environment_var_dict = TestConfig.get_environment_var_dict()
        TestLogger.scenario_logger_obj.info(f"environment_var_dict: {environment_var_dict}")

        # Instantiate a scenario object
        scenario_obj = Scenario(scenario_file)
        scenario_obj.expand_item_dict_list()
        TestLogger.scenario_logger_obj.info(f"scenario_obj: {str(scenario_obj)}")

        # Process scenario's pre-request events.
        scenario_pre_request_event_list_of_exec_list = scenario_obj.get_pre_request_event_list_of_exec_list()
        TestLogger.scenario_logger_obj.info(
            f"Processing pre-request events:\n"
            f"\tList of exec list: {scenario_pre_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        scenario_pre_request_event_list_of_exec_list,
                                        scenario_obj)

        # Get the scenario item dictionaries list and process it
        item_dict_list = scenario_obj.get_item_dict_list()
        item_index = 0
        item_processing_error_count = 0
        failed_item_index_list = []
        for item_dict in item_dict_list:
            # Instantiate an item object
            item_obj = Item(item_index, item_dict, environment_var_dict, scenario_obj)
            TestLogger.scenario_logger_obj.info(f"item_obj: {str(item_obj)}")
            start_time = time.time()

            try:
                # Prepare request and submit it
                item_obj.process_request()

            # Catch any exception during item processing, log it and increment the error count.
            except Exception as any_exception:
                TestLogger.scenario_logger_obj.error(any_exception)
                item_processing_error_count += 1
                failed_item_index_list.append(item_index)

            TestLogger.scenario_logger_obj.info(f"Scenario Duration: {time.time()-start_time} seconds")
            # Increment item index
            item_index += 1

        # Create a scenario file with actual response(s) in it.
        scenario_obj.create_scenario_file_with_expected_responses()

        # Process scenario's post-request events.
        scenario_post_request_event_list_of_exec_list = scenario_obj.get_post_request_event_list_of_exec_list()
        TestLogger.scenario_logger_obj.info(
            f"Processing post-request events:\n"
            f"\tList of exec list: {scenario_post_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        scenario_post_request_event_list_of_exec_list,
                                        scenario_obj)

        # Log the total number of items/requests processed.
        TestLogger.scenario_logger_obj.info(f"Total number of items processed: {item_index}.")

        # If there were any errors occurred during item processing, then raise exception
        if item_processing_error_count > 0:
            raise ItemProcessingErrorsEncountered(item_processing_error_count,
                                                  failed_item_index_list)

    # At this point, catch an exception which occurs outside item processing and log it.
    except Exception as any_exception:
        TestLogger.scenario_logger_obj.error(any_exception)
        raise

    # Clean up
    finally:
        # Remove scenario log handler from scenario logger.
        if TestLogger.scenario_log_file_handler_obj:
            TestLogger.scenario_logger_obj.info(
                f"Removing scenario log file handler object for '{scenario_file}'.")
            TestLogger.remove_scenario_log_file_handler()
