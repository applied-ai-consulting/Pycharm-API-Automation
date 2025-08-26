import os
import sys
import re
import random
import string
import json
import pytest
from uuid import uuid4
from random import randint
from collections import OrderedDict
from common.constants import *
from common.test_run_error import *
from functools import reduce
import operator
import datetime
from datetime import timedelta, date
from pytz import timezone
from common.test_config import *


def get_guid():
    """
    Generate a GUID.

    Returns:
        str: A GUID.
    """
    return uuid4().hex


def get_random_positive_integer():
    """
    Generate a random positive integer in string format.

    Returns:
        str: A random positive integer in string format.
    """
    return str(randint(1, sys.maxsize))


def get_random_negative_integer():
    """
    Generate a random negative integer in string format.

    Returns:
        str: A random negative integer in string format.
    """
    return str(-randint(1, sys.maxsize))


def get_random_date_time_future(days_range):
    """
    Generate a future random datetime within a given days range relative to the current datetime.
    Args:
        days_range (int): Max number of days from which a number will randomly be picked.

    Returns:
        datetime: A future random datetime with default time zone in "%a, %d %b %Y %H:%M:%S %Z" format.

    """
    days_to_add = random.randint(0, days_range)
    random_future_datetime = datetime.datetime.now(timezone(DATETIME_DEFAULT_TIMEZONE)) + datetime.timedelta(
        days_to_add)
    return random_future_datetime


def get_datetime_specific_format(date_time, date_time_format):
    """
    Convert the datetime to a specific format
    Args:
        date_time (datetime): datetime string to be converted
        date_time_format (str): format to be converted to

    Returns:
        str: converted string in a specified datetime format

    """
    datetime_with_zone_str = date_time.strftime(date_time_format)
    return datetime_with_zone_str


def get_datetime_with_minutes_added(start_datetime, minutes_to_add):
    """
    Add minutes specified to the given datetime object

    Args:
        start_datetime (datetime): datetime string
        minutes_to_add (int): minutes to be added to start_datetime

    Returns:
        datetime: datetime with minutes added

    """
    delta_datetime = start_datetime + timedelta(minutes=minutes_to_add)
    return delta_datetime


def get_random_alpha_numeric(str_len):
    """
    Generate a random alpha numeric string of specified length.

    Args:
        str_len (int): Length of alpha numeric string to be generated.

    Returns:
        str: Random generated alpha numeric string of specified length.
    """
    random_source = string.ascii_letters + string.digits
    return ''.join(random.choice(random_source) for i in range(str_len))


def get_random_password(password_len):
    """
    Generate a random password of specified length consisting of letters,
    digits and special symbols.

    Args:
        password_len (int): Length of password to be generated.

    Returns:
        str: Random generated password of specified length.
    """
    random_source = string.ascii_letters + string.digits + RANDOM_SPECIAL_CHAR_SET
    return ''.join(random.choice(random_source) for i in range(password_len))


def get_current_date(offset_days):
    """
    Get today's date in YYYY-MM-DD format.

    Returns:
        str: Today's date in YYYY-MM-DD format.
    """
    if offset_days is None:
        return date.today().strftime(RANDOM_DATE_FORMAT)
    else:
        num_days = re.findall(NUM_ONLY_PATTERN, offset_days)
        operation = re.findall("[_+-]", offset_days)
        # Expecting only one group of digits to be extracted in num_days, therefore list size should be 1
        if num_days[0].isdigit() and len(num_days) == 1:
            if operation[0] == '-':
                return (date.today() - timedelta(days=int(num_days[0]))).strftime(RANDOM_DATE_FORMAT)
            elif operation[0] == '+':
                return (date.today() + timedelta(days=int(num_days[0]))).strftime(RANDOM_DATE_FORMAT)
            else:
                raise OperatorNotAllowed(operation[0])
        else:
            raise InvalidNumOfDaysInDynVariable(num_days)


def get_random_date_past(max_days):
    """
    Get a random past date in the previous max days relative to today's date in YYYY-MM-DD format.

    Args:
        max_days (int): Max number of days.

    Returns:
        str: A random past date in the previous max days relative to today's date in YYYY-MM-DD format.
    """
    return (date.today() + timedelta(days=-randint(1, max_days))).strftime(RANDOM_DATE_FORMAT)


def get_random_date_future(max_days):
    """
    Get a random future date in the next max days relative to today's date in YYYY-MM-DD format.

    Args:
        max_days (int): Max number of days.

    Returns:
        str: A random future date in the next max days relative to today's date in YYYY-MM-DD format.
    """
    return (date.today() + timedelta(days=randint(1, max_days))).strftime(RANDOM_DATE_FORMAT)


def get_random_start_datetime_future(test_config_class, random_max_days):
    """
    Generate a random start datetime in future from current datetime with in the next max_days

    Args:
        test_config_class (class): TestConfig class
        random_max_days (int): Max number of days to ba added to the current date for random future date

   Returns:
       str: A future random start datetime with default time zone in "%a, %d %b %Y %H:%M:%S %Z" format.

    """

    start_datetime = get_random_date_time_future(random_max_days)
    start_datetime_formatted_str = get_datetime_specific_format(start_datetime, RANDOM_DATETIME_FORMAT)
    test_config_class.set_current_datetime(start_datetime)
    return start_datetime_formatted_str


def get_random_end_datetime_future(test_config_class):
    """
    Generate an end datetime in future relative to random start datetime with minutes_to_add

    Args:
        test_config_class (class): TestConfig class

    Returns:
        str: end datetime with default timezone in "%a, %d %b %Y %H:%M:%S %Z" format

    """

    end_datetime = get_datetime_with_minutes_added(test_config_class.get_current_datetime(),
                                                   RANDOM_DURATION_MINUTES)
    end_datetime_formatted_str = get_datetime_specific_format(end_datetime, RANDOM_DATETIME_FORMAT)
    return end_datetime_formatted_str


def eval_for_list_or_dict(list_or_dict_obj):
    """
    Evaluates the data for type 'list' or 'dict', if true, then converts the string to json format string and returns
    the value

    Args: list_or_dict_obj (str): Variable value to be evaluated for list or dict

    Returns:
        (str) list_or_dict_obj transformed as json string representation of list or dict if applicable,
         or returned without change as string
    """
    if isinstance(list_or_dict_obj, list) or isinstance(list_or_dict_obj, dict):
        return json.dumps(list_or_dict_obj)
    else:
        return list_or_dict_obj


def find_markup_elem_list(exec_str):
    """
    Find markup elements in an input string.

    Args:
        exec_str (str): An input string.

    Returns:
        list: List of markup elements
    """
    markup_elem_list = []
    markup_stmt = re.search(MARKUP_STMT_PATTERN, exec_str)
    if markup_stmt:
        # Remove angle brackets
        markup_stmt = markup_stmt.group()[1:-1]
        # Get the markup operation first
        markup_op = markup_stmt.split(MARKUP_DELIMITER, 1)[0]
        # Check if markup operation is valid.
        if markup_op in MARKUP_OP_LIST:
            # Split markup stmt based on the markup op and its arity (minus 1)
            markup_elem_list = markup_stmt.split(MARKUP_DELIMITER, MARKUP_ARITY_DICT[markup_op] - 1)
        else:
            # Raise unknown markup operation error.
            raise UnknownMarkupOperationError(markup_op)
    # Return result
    return markup_elem_list


def find_all_double_curly_braces_vars(input_str):
    """
    Find all variables enclosed by double curly braces in an input string.

    Args:
        input_str (str): Input string

    Returns:
        list: List of variables enclosed by double curly braces.
    """
    # Find all unique variables enclosed with curly braces
    double_curly_braces_var_list = list(OrderedDict.fromkeys(re.findall(VAR_NAME_PATTERN, input_str)))
    return double_curly_braces_var_list


def replace_double_curly_braces_var_in_string(input_str,
                                              double_curly_braces_var_list,
                                              environment_var_dict,
                                              scenario_var_dict,
                                              test_config_class
                                              ):
    """
    Replace all variables enclosed by double curly braces in an input string.

    Args:
        input_str (str): Input string
        double_curly_braces_var_list (list): List of variables enclosed in double curly braces
        environment_var_dict (dict): Dictionary of environment variables
        scenario_var_dict (dict): Dictionary of scenario variables
        test_config_class (class): TestConfig class

    Returns:
        str: Output string is input string with all variables replaced based on the given
        scenario var dictionary and environment var dictionary.
    """
    output_str = input_str
    for double_curly_braces_var in double_curly_braces_var_list:
        # Remove enclosing double curly braces
        var = double_curly_braces_var[2:-2]
        var_value = None

        # Check if var is a dynamic var and it's supported
        if DOLLAR_CHAR in var:
            var_split = var.split(DOLLAR_CHAR)
            offset_days = None
            if PLUS_CHAR in var_split[-1] or MINUS_CHAR in var_split[-1]:
                if var.find(CURRENT_DATE_DYN_VAR) == -1:
                    raise DynamicVariableOperatorNotAllowed(re.findall(ALPHA_ONLY_PATTERN, var_split[-1])[0])
                offset_days = (re.findall(DATE_NUM_PATTERN, var_split[-1]))[0]
                var_split[-1] = var_split[-1].replace(offset_days, '')
                # var_split[-1] = var_split[-1][:11]
            var_value = var_split[0] + replace_dynamic_variable(f'${var_split[-1]}', offset_days, test_config_class)
        elif var in scenario_var_dict:
            # Get var value from scenario var dict first
            # Evaluate the type of value in scenario var dict
            var_value = eval_for_list_or_dict(scenario_var_dict[var])
        elif var in environment_var_dict:
            # Get var value from environment var dict
            var_value = environment_var_dict[var]

        # Substitute substituted str
        if not (var_value is None):
            output_str = output_str.replace(double_curly_braces_var, str(var_value))

    return output_str


def replace_dynamic_variable(var, offset_days, test_config_class):
    """
    Replace string with dynamic variable
    Args:
        offset_days: variable days to be added in start date, if start date should be greater than today
        var: variable string to be replaced by dynamic variable
        test_config_class (class): TestConfig class

    Returns:
        String: string replacement

    """
    # It's a dynamic variable
    if var in DYNAMIC_VAR_LIST:
        # Generate a random value for var value based on the dynamic variable
        if var == GUID_DYN_VAR:
            return get_guid()
        if var == RANDOM_POSITIVE_INTEGER_DYN_VAR:
            return get_random_positive_integer()
        if var == RANDOM_NEGATIVE_INTEGER_DYN_VAR:
            return get_random_negative_integer()
        elif var == RANDOM_ALPHA_NUMERIC_DYN_VAR:
            return get_random_alpha_numeric(RANDOM_ALPHA_NUMERIC_LEN)
        elif var == RANDOM_PASSWORD_DYN_VAR:
            return get_random_password(RANDOM_PASSWORD_LEN)
        elif var == CURRENT_DATE_DYN_VAR:
            return get_current_date(offset_days)
        elif var == RANDOM_DATE_PAST_DYN_VAR:
            return get_random_date_past(RANDOM_MAX_DAYS)
        elif var == RANDOM_DATE_FUTURE_DYN_VAR:
            return get_random_date_future(RANDOM_MAX_DAYS)
        elif var == RANDOM_START_DATETIME_FUTURE_DYN_VAR:
            return get_random_start_datetime_future(test_config_class, RANDOM_MAX_DAYS)
        elif var == RANDOM_END_DATETIME_FUTURE_DYN_VAR:
            return get_random_end_datetime_future(test_config_class)
    else:
        raise DynamicVariableIsNotSupported(var)


def convert_key_value_dict_list_to_dict(key_value_dict_list):
    """
    Convert list of key value dictionaries to a dictionary

    Args:
        key_value_dict_list (list): List of key value dictionaries

    Returns:
        dict: A dict
    """
    result_dict = {}
    for key_value_dict in key_value_dict_list:
        if KEY_KEY in key_value_dict:
            result_dict[key_value_dict[KEY_KEY]] = key_value_dict[VALUE_KEY]
    return result_dict


def convert_postman_header_dict_list_to_header_dict(postman_header_dict_list):
    """
    Convert Postman header dictionary list to a single header dictionary

    Args:
        postman_header_dict_list (list): Input string

    Returns:
        dict: A header dict
    """
    header_dict = {}
    for postman_header_dict in postman_header_dict_list:
        header_dict[postman_header_dict[KEY_KEY]] = postman_header_dict[VALUE_KEY]
    return header_dict


def is_subset_dict(first_dict, second_dict, is_compare_key_value=False):
    """
    Check if expected the 1st dictionary is a subset of the 2nd dictionary.

    Args:
        first_dict (dict): 1st dictionary
        second_dict (dict): 2nd dictionary
        is_compare_key_value (bool): Compare key value of this is set to True.


    Returns:
        bool: True if the 1st dictionary is a subset of the 2nd dictionary. Otherwise False.
    """
    result = True
    for first_dict_key in first_dict.keys():
        if not (first_dict_key in second_dict):
            return False
        else:
            if is_compare_key_value:
                if not (first_dict[first_dict_key] == second_dict[first_dict_key]):
                    return False
    return result


def get_file_name_without_extension(file_name_with_extension):
    """
    Get file name without extension.

    Args:
        file_name_with_extension (str): A file name with extension.

    Returns:
        str: File name without extension.
    """
    return os.path.splitext(file_name_with_extension)[0]


def get_property_value(property_name, descendant_properties, input_json):
    """
    Get the value of a property from a JSON object via its parent properties.

    Args:
        property_name (str): Property name from which the value will be retrieved.
        descendant_properties (list): List of  descendant properties which leads to the property
        input_json (json): A JSON object

    Returns:
        str: Property value or None if the property doesn't exist in the input JSON object.
    """
    if type(input_json) is dict:
        if property_name in input_json:
            return input_json[property_name]
        else:
            if not descendant_properties:
                return None
            else:
                # Inspect child (direct descendant)
                child_prop = descendant_properties[0]
                if child_prop in input_json:
                    return get_property_value(property_name,
                                              descendant_properties[1:],
                                              input_json[child_prop])
                else:
                    return None
    elif type(input_json) is list:
        # Inspect the first list element
        prop_value = get_property_value(property_name, descendant_properties, input_json[0])
        if not (prop_value is None):
            # Return string representation
            return str(prop_value)
        else:
            # Inspect remaining list elements
            return get_property_value(property_name, descendant_properties, input_json[1:])
    else:
        return None


def get_pre_and_post_request_event_list_of_exec_list(input_dict):
    """
    Get pre-request and post-request (test) events with their exec steps.

    Args:
        input_dict (dict): A dictionary.

    Returns:
        list: Pre-request event list of exec list
        list: Post-request event list of exec list
    """
    pre_request_event_list_of_exec_list = []
    post_request_event_list_of_exec_list = []
    if EVENT_KEY in input_dict:
        for event_dict in input_dict[EVENT_KEY]:
            if (LISTEN_KEY in event_dict) and (SCRIPT_KEY in event_dict) and (EXEC_KEY in event_dict[SCRIPT_KEY]):
                if event_dict[LISTEN_KEY] == PREREQUEST_KEY_VALUE:
                    pre_request_event_list_of_exec_list.append(event_dict[SCRIPT_KEY][EXEC_KEY])
                elif event_dict[LISTEN_KEY] == TEST_KEY_VALUE:
                    post_request_event_list_of_exec_list.append(event_dict[SCRIPT_KEY][EXEC_KEY])
    return pre_request_event_list_of_exec_list, post_request_event_list_of_exec_list


def process_event_list_of_exec_list(test_config_class,
                                    test_logger_class,
                                    event_list_of_exec_list,
                                    scenario_obj,
                                    response_obj=None):
    """
    Process event list consisting of exec lists.

    Args:
        test_config_class (class): TestConfig class
        test_logger_class (class): TestLogger class
        event_list_of_exec_list (list): Event list consisting of exec lists.
        scenario_obj (obj): A scenario object.
        response_obj (obj): A response object.

    Returns:
        Void.
    """
    for exec_list in event_list_of_exec_list:
        for exec_string in exec_list:
            markup_elem_list = find_markup_elem_list(exec_string)
            if markup_elem_list:
                # There is a markup stmt in the exec string and execute it.
                markup_op = markup_elem_list[0]
                if markup_op == SKIP_MARKUP_OP:
                    test_logger_class.scenario_logger_obj.debug(
                        f"Markup statement:\n"
                        f"\tmarkup_op: {markup_op}\n"
                        f"\treason: {markup_elem_list[1]}")
                    pytest.skip(markup_elem_list[1])
                elif markup_op == XFAIL_MARKUP_OP:
                    test_logger_class.scenario_logger_obj.debug(
                        f"Markup statement:\n"
                        f"\tmarkup_op: {markup_op}\n"
                        f"\treason: {markup_elem_list[1]}")
                    pytest.xfail(markup_elem_list[1])
                elif markup_op == PARTIAL_RESPONSE_VALIDATION_MARKUP_OP:
                    test_logger_class.scenario_logger_obj.debug(
                        f"Markup statement:\n"
                        f"\tmarkup_op: {markup_op}\n"
                        f"\ttype: {markup_elem_list[1]}")
                elif markup_op == SET_VARIABLE_MARKUP_OP:
                    var_name = markup_elem_list[1]
                    right_obj = markup_elem_list[2]
                    right_val = markup_elem_list[3]
                    test_logger_class.scenario_logger_obj.debug(
                        f"Markup statement:\n"
                        f"\top_markup: {markup_op}\n"
                        f"\tvar_name: {var_name}\n"
                        f"\tright_obj: {right_obj}\n"
                        f"\tright_val: {right_val}")
                    # Set variable
                    if right_obj == VALUE_MARKUP_OBJ:
                        # Check if right_val is a variable
                        double_curly_braces_var_list = find_all_double_curly_braces_vars(right_val)
                        if len(double_curly_braces_var_list) > 0:
                            right_val = replace_double_curly_braces_var_in_string(
                                right_val,
                                double_curly_braces_var_list,
                                test_config_class.get_environment_var_dict(),
                                scenario_obj.get_scenario_var_dict(),
                                test_config_class
                            )

                        # Set scenario variable to a value (if any)
                        scenario_obj.set_scenario_var_value(var_name, right_val)
                        # Set environment variable if any
                        test_config_class.set_environment_var_value(var_name, right_val)
                        test_logger_class.scenario_logger_obj.debug(
                            f"Set variable to a value:\n"
                            f"\tvar_name: {var_name}\n"
                            f"\tresp_prop_value: {right_val}")
                    elif right_obj == RESPONSE_MARKUP_OBJ:
                        # Get actual response property value
                        if not (response_obj is None):
                            # There might be more than one properties delimited by dot(s) and
                            # the last property should be the one which holds the value to be set.
                            resp_prop_list = right_val.split(RESPONSE_PROPERTY_VALUE_DELIMITER)
                            resp_prop_list_len = len(resp_prop_list)
                            last_resp_prop = resp_prop_list[resp_prop_list_len - 1]

                            # Get if this props containing regex
                            regex = re.compile(r'^/.*/$')
                            # get the regex pattern
                            patterns = [i for i in resp_prop_list if regex.match(i)]
                            # filtered out the regex pattern
                            resp_prop_list = [i for i in resp_prop_list if not regex.match(i)]
                            resp_obj_json = response_obj.json()
                            resp_prop_value = get_from_dict(resp_obj_json, resp_prop_list)
                            if patterns:
                                values_found = re.findall(patterns[0].strip('/'), resp_prop_value)
                                if values_found:
                                    resp_prop_value = values_found[0]
                                else:
                                    resp_prop_value = ''

                            if not (resp_prop_value is None):
                                # Response property exist
                                # Evaluate the data type of resp_prop_value
                                resp_prop_value = scenario_obj.eval_scenario_var_value(resp_prop_value)
                                # Set scenario variable to a response property value (if any)
                                scenario_obj.set_scenario_var_value(var_name, resp_prop_value)
                                # Set environment variable to a response property value (if any)
                                test_config_class.set_environment_var_value(var_name, resp_prop_value)
                                test_logger_class.scenario_logger_obj.debug(
                                    f"Set scenario and environment variable to a response property value:\n"
                                    f"\tvar_name: {var_name}\n"
                                    f"\tresp_prop_name: {right_val}\n"
                                    f"\tresp_prop_value: {resp_prop_value}")
                            else:
                                # Response property doesn't exist, raise error
                                raise PropertyDoesNotExistInActualResponseBody(right_val)


def get_from_dict(data_dict, list_keys):
    """
    Get value from dictionary based on list of keys
    Args:
        data_dict: parent dictionary
        list_keys: list of keys to traverse

    Returns:

    """
    keys = list(map(maybe_make_number, list_keys))
    try:
        result_item = reduce(operator.getitem, keys, data_dict)
    except KeyError:
        result_item = ''
    return str(result_item)


def maybe_make_number(s):
    """Returns a string 's' into a integer if possible, or
    returns it as is."""
    # handle None, "", 0
    if not s:
        return s
    try:
        f = float(s)
        i = int(f)
        return i if f == i else f
    except ValueError:
        return s


def find_first_referred_scenario_json_file(scenario_set_class,
                                           test_logger_class,
                                           data_file_path,
                                           event_list_of_exec_list):
    """
    Find the first referred scenario JSON file in the given event list consisting of exec lists.

    Args:
        scenario_set_class (class): ScenarioSet class
        test_logger_class (class): TestLogger class
        data_file_path (str) Data file path of a scenario file
        event_list_of_exec_list (list): Event list consisting of exec lists.

    Returns:
        str: The first referred scenario JSON file
    """
    # Find the first markup statement for referring a scenario file
    referred_scenario_json_file = None
    for exec_list in event_list_of_exec_list:
        for exec_string in exec_list:
            markup_elem_list = find_markup_elem_list(exec_string)
            if markup_elem_list:
                # There is a markup stmt in the exec string and execute it.
                markup_op = markup_elem_list[0]
                if markup_op == REFER_SCENARIO_FILE_MARKUP:
                    referred_scenario_json_file = markup_elem_list[1]
                    referred_scenario_json_file = os.path.join(data_file_path, referred_scenario_json_file)
                    test_logger_class.scenario_logger_obj.debug(
                        f"Markup statement:\n"
                        f"\tmarkup_op: {markup_op}\n"
                        f"\treferred_scenario_file: {referred_scenario_json_file}")
                    return referred_scenario_json_file
    # No referred scenario file found
    return referred_scenario_json_file


def merge_two_dicts(first_dict, second_dict):
    """
    Merge to dictionaries into a new dictionary.

    Args:
        first_dict (dict): First dictionary to be merged.
        second_dict (dict): Second dictionary to be merged.
    Returns:
        dict: A new dictionary as the result of the merging of the 1st and 2nd dictionary.
    """
    merged_dict = first_dict.copy()
    merged_dict.update(second_dict)
    return merged_dict


def expand_item_dict_list(test_config_class,
                          scenario_set_class,
                          test_logger_class,
                          scenario_obj,
                          data_file_path,
                          referrer_merged_var_dict,
                          item_dict_list,
                          referred_scenario_file_list):
    """
    Expand scenario JSON object if there are items which refer to other scenario files.
    This is a recursive function which uses the parameter referred_scenario_file_list for
    reference cycle detection.

    Args:
        test_config_class (class): TestConfig class
        scenario_set_class (class): ScenarioSet class
        test_logger_class (class): TestLogger class
        scenario_obj (obj): A scenario object
        data_file_path (str): Data fiile path of the scenario
        referrer_merged_var_dict (dict): Referrer's merged dict of env and scenario variable dict
        item_dict_list (list): List of item dictionaries.
        referred_scenario_file_list (list): List of referred scenario files used for cycle detection.
    Returns:
        Void
    """
    # Inspect item dict list
    item_index = 0
    while item_index < len(item_dict_list):
        item_dict = item_dict_list[item_index]
        # Find OPTIONS request in which refer-scenario-file markup can be specified
        if item_dict[REQUEST_KEY][METHOD_KEY] == OPTIONS_METHOD_VALUE:
            # Get pre- and post-request event exec list
            pre_request_event_list_of_exec_list, post_request_event_list_of_exec_list = \
                get_pre_and_post_request_event_list_of_exec_list(item_dict)
            # Build pre-request exec list containing set-variable markups only
            pre_request_exec_list = []
            for pre_request_event_exec_list in pre_request_event_list_of_exec_list:
                for pre_request_exec in pre_request_event_exec_list:
                    markup_elem_list = find_markup_elem_list(pre_request_exec)
                    if len(markup_elem_list) > 0:
                        if markup_elem_list[0] == SET_VARIABLE_MARKUP_OP:
                            pre_request_exec_list.append(pre_request_exec)

            # Find first referred scenario json file
            referred_scenario_json_file = \
                find_first_referred_scenario_json_file(scenario_set_class,
                                                       test_logger_class,
                                                       data_file_path,
                                                       pre_request_event_list_of_exec_list +
                                                       post_request_event_list_of_exec_list
                                                       )
            if not (referred_scenario_json_file is None):
                # Check for the existence of reference cycle and raise error if any.
                if referred_scenario_json_file in referred_scenario_file_list:
                    raise ScenarioFileReferenceCycleError(referred_scenario_json_file)

                # Found a referred scenario file
                test_logger_class.scenario_logger_obj.debug(
                    f"Load referred scenario JSON file:\n"
                    f"\treferred_scenario_file: '{referred_scenario_json_file}'.")

                # Load referred scenario JSON file
                with open(referred_scenario_json_file, "r") as json_file:
                    referred_scenario_json = json.load(json_file)

                # Get its scenario var dict and ensure it is a subset of the referrer's scenario var dict
                referred_scenario_var_dict = {}
                if VAR_KEY in referred_scenario_json:
                    referred_scenario_var_dict = \
                        convert_key_value_dict_list_to_dict(referred_scenario_json[VAR_KEY])
                # Check if referred scenario var dict is a subset of referrer's scenario var dict
                if not (is_subset_dict(referred_scenario_var_dict, referrer_merged_var_dict)):
                    raise ReferredScenarioVarsNotSubsetError(referred_scenario_var_dict,
                                                             referrer_merged_var_dict)

                # Get its item dict list
                referred_item_dict_list = []
                if ITEM_KEY in referred_scenario_json:
                    referred_item_dict_list = referred_scenario_json[ITEM_KEY]
                    # Propagate the dummy OPTIONS' pre-request events to the first item's pre-request
                    # events of the referred item dict list
                    first_referred_item_dict = referred_item_dict_list[0]
                    is_event_found = False
                    if EVENT_KEY in first_referred_item_dict:
                        is_event_found = True
                        is_prerequest_event_found = False
                        for event_dict in first_referred_item_dict[EVENT_KEY]:
                            if LISTEN_KEY in event_dict:
                                if event_dict[LISTEN_KEY] == PREREQUEST_KEY_VALUE:
                                    # If there is an existing prerequest event,
                                    # then append the dummy OPTIONS' prerequest event to it
                                    is_prerequest_event_found = True
                                    event_dict[SCRIPT_KEY][EXEC_KEY] = \
                                        event_dict[SCRIPT_KEY][EXEC_KEY] + \
                                        pre_request_exec_list
                        if not is_prerequest_event_found:
                            # No prerequest event in the first referred item is found,
                            # so add prerequest event to it
                            prerequest_event = \
                                {LISTEN_KEY: PREREQUEST_KEY_VALUE,
                                 SCRIPT_KEY: {EXEC_KEY: pre_request_exec_list}
                                 }
                            first_referred_item_dict[EVENT_KEY].append(prerequest_event)
                    if not is_event_found:
                        # No event found, then add the event dict to the first referred item dict
                        first_referred_item_dict[EVENT_KEY] = \
                            {LISTEN_KEY: PREREQUEST_KEY_VALUE,
                             SCRIPT_KEY: {EXEC_KEY: pre_request_exec_list}
                             }

                # Call this function itself recursively with the item dict list parts that are not
                # inspected for refer-scenario-file markup yet.
                return \
                    item_dict_list[:item_index] + \
                    expand_item_dict_list(test_config_class,
                                          scenario_set_class,
                                          test_logger_class,
                                          scenario_obj,
                                          data_file_path,
                                          referred_scenario_var_dict,
                                          referred_item_dict_list,
                                          referred_scenario_file_list + list(referred_scenario_json_file)) + \
                    expand_item_dict_list(test_config_class,
                                          scenario_set_class,
                                          test_logger_class,
                                          scenario_obj,
                                          data_file_path,
                                          referrer_merged_var_dict,
                                          item_dict_list[item_index + 1:],
                                          referred_scenario_file_list)
        # Next item
        item_index += 1
    # If no markup is found, then return item dict list
    return item_dict_list


def delete_keys_from_dict(delete_key_list, input_dict):
    """
    Delete keys from a dictionary

    Args:
        delete_key_list (list): List of keys to be deleted.
        input_dict (dict): An input dictionary.

    Returns:
        Void.
    """
    for delete_key in delete_key_list:
        if delete_key in input_dict:
            del input_dict[delete_key]


def deep_delete_keys_from_object(delete_key_list, input_obj):
    """
    Deep delete keys from an object including its child/descendant dictionaries.

    Args:
        delete_key_list (list): List of keys to be deleted.
        input_obj (object): An input object.

    Returns:
        Void.
    """
    if type(input_obj) is dict:
        delete_keys_from_dict(delete_key_list, input_obj)
        for dict_value in input_obj.values():
            deep_delete_keys_from_object(delete_key_list, dict_value)
    elif type(input_obj) is list:
        for list_elem in input_obj:
            deep_delete_keys_from_object(delete_key_list, list_elem)


def get_data_file_path(scenario_json_file_name):
    """
    Get the data file path from a full path scenario JSON file name.

    Args:
        scenario_json_file_name (str): A full path scenario JSON file name.

    Returns:
        str: Data file path of a full path scenario JSON file name.
    """
    data_file_path = None
    json_file_path = os.path.dirname(scenario_json_file_name)
    while not (json_file_path == DATA_PATH[0:-1]):
        data_file_path = json_file_path
        base_name = os.path.basename(json_file_path)
        json_file_path = os.path.dirname(json_file_path)
    return data_file_path


def get_is_partial_response_validation(event_list_of_exec_list):
    """
    Checks if partial response validation is required
    Args:
        event_list_of_exec_list (list): Event list consisting of exec lists.

    Returns:
        str: method of partial validation if required , else None

    """
    partial_response_validation_type = None
    for exec_list in event_list_of_exec_list:
        for exec_string in exec_list:
            markup_elem_list = find_markup_elem_list(exec_string)
            if markup_elem_list:
                # There is a markup stmt in the exec string and execute it.
                markup_op = markup_elem_list[0]
                if markup_op == PARTIAL_RESPONSE_VALIDATION_MARKUP_OP:
                    partial_response_validation_type = markup_elem_list[1]

    return partial_response_validation_type


def perform_partial_response_validation(deep_diff_result_metadata, type_of_validation):
    """
    Infers partial validation from expected and actual response deep diff result metadata
    Args:
        deep_diff_result_metadata (dict): Deep diff metadata result from expected and actual response object
        type_of_validation (str): type of partial response validation

    Returns:
        boolean: True if partial validation is success, False if partial validation is fail

    """
    items_removed_key = []
    values_changed_key = []

    if DICTIONARY_ITEM_REMOVED_KEY in deep_diff_result_metadata:
        items_removed_key = deep_diff_result_metadata[DICTIONARY_ITEM_REMOVED_KEY]
    if VALUES_CHANGED_KEY in deep_diff_result_metadata:
        values_changed_key = deep_diff_result_metadata[VALUES_CHANGED_KEY]

    if type_of_validation == KEYS_ONLY_MARKUP_OBJ:
        return len(items_removed_key) <= 0
    else:
        return len(items_removed_key) <= 0 or len(values_changed_key) <= 0
