import traceback
from json import JSONDecodeError
from deepdiff import DeepDiff

from common.utilities import *
from common.test_run_error import *
from common.constants import *
from common.test_config import TestConfig
from common.test_logger import TestLogger


class Item(object):
    """
    Item class contains name, request, and a list of expected responses.
    """

    # Private attributes
    _index = None
    _name = None
    _description = None
    _request_method = None
    _request_url = None
    _request_dict = None
    _response_dict_list = None
    _environment_var_dict = None
    _scenario_obj = None
    _actual_response_obj = None
    _pre_request_event_list_of_exec_list = None
    _post_request_event_list_of_exec_list = None

    # Constructor
    def __init__(self, index, item_dict, environment_var_dict, scenario_obj):
        """
        Item object constructor

        Args:
            index (int): Index of the item in item dictionary list of a scenario
            item_dict (dict): An item dictionary
            environment_var_dict (dict): Environment variable dictionary
            scenario_obj (obj): Scenario object

        Returns:
            object: Item object.
        """
        # Initialize all static variables
        self._index = index
        if NAME_KEY in item_dict:
            self._name = item_dict[NAME_KEY]
        if DESC_KEY in item_dict:
            self._description = item_dict[DESC_KEY]
        if REQUEST_KEY in item_dict:
            self._request_dict = item_dict[REQUEST_KEY]
            if METHOD_KEY in self._request_dict:
                self._request_method = self._request_dict[METHOD_KEY].upper()
        if RESPONSE_KEY in item_dict:
            self._response_dict_list = item_dict[RESPONSE_KEY]

        # Set var dictionaries
        self._environment_var_dict = environment_var_dict
        self._scenario_obj = scenario_obj

        # Split pre-request and post-request (test) events with their exec steps
        self._pre_request_event_list_of_exec_list, self._post_request_event_list_of_exec_list = \
            get_pre_and_post_request_event_list_of_exec_list(item_dict)

    def __str__(self):
        """
        Item object string representation..

        Returns:
            str: String representation of item object.
        """
        return f"\nITEM object:\n"\
               f"\tindex: {self._index}\n"\
               f"\tname: {self._name}\n"\
               f"\tdescription: {self._description}\n"\
               f"\tpre_request_event_list_of_exec_list: {self._pre_request_event_list_of_exec_list}\n"\
               f"\tpost_request_event_list_of_exec_list: {self._post_request_event_list_of_exec_list}"

    # Private methods
    def _prepare_request_url(self):
        """
        Prepare request URL by replacing all variable occurrences with their respective value
        and set it to self._request_url

        Returns:
            Void.
        """
        if URL_KEY in self._request_dict:
            if RAW_KEY in self._request_dict[URL_KEY]:
                request_url = self._request_dict[URL_KEY][RAW_KEY]
                # Find all variables with double curly braces first and then replace them with their values
                double_curly_braces_vars_in_request_url = find_all_double_curly_braces_vars(request_url)
                TestLogger.scenario_logger_obj.debug(f"Prior variable replacement:\n"
                                                     f"\trequest_url: {request_url}\n"
                                                     f"\tvariables: {double_curly_braces_vars_in_request_url}"
                                                     )
                # remove protocol if already exist in the raw.
                # Exported json from postman sometimes already have protocol in the raw.
                if '{{url}}' in double_curly_braces_vars_in_request_url:
                    request_url = re.sub(PROTOCOL_PATTERN, '', request_url)
                request_url = replace_double_curly_braces_var_in_string(
                    request_url,
                    double_curly_braces_vars_in_request_url,
                    self._environment_var_dict,
                    self._scenario_obj.get_scenario_var_dict(),
                    TestConfig
                )
            else:
                raise RawKeyDoesNotExistInDict(self._request_dict[URL_KEY])
        else:
            raise UrlKeyDoesNotExistInDict(self._request_dict)

        TestLogger.scenario_logger_obj.debug(
            f"After variable replacement:\n"
            f"\trequest_url: {request_url}"
            )
        self._request_url = request_url

    def _prepare_request_query_params(self):
        """
        Prepare request query params from URL's query by replacing all variable occurrences with
        their respective value.

        Returns:
            str: Prepared request query params.
        """
        request_query_params = {}
        if URL_KEY in self._request_dict:
            if QUERY_KEY in self._request_dict[URL_KEY]:
                for query in self._request_dict[URL_KEY][QUERY_KEY]:
                    # Find all variables with double curly braces first and then replace them with their values
                    double_curly_braces_vars_in_request_url = find_all_double_curly_braces_vars(query[VALUE_KEY])
                    request_query_params[query[KEY_KEY]] = replace_double_curly_braces_var_in_string(
                        query[VALUE_KEY],
                        double_curly_braces_vars_in_request_url,
                        self._environment_var_dict,
                        self._scenario_obj.get_scenario_var_dict(),
                        TestConfig)
        else:
            raise UrlKeyDoesNotExistInDict(self._request_dict)

        TestLogger.scenario_logger_obj.debug(
            f"After variable replacement:\n"
            f"\trequest_query_params: {request_query_params}"
            )
        return request_query_params

    def _prepare_request_header(self):
        """
        Prepare request header.

        Returns:
            str: Prepared request header.
        """
        # Convert Postman header dict lists to a single Python request header dict
        request_header_dict = convert_postman_header_dict_list_to_header_dict(self._request_dict[HEADER_KEY])
        # Find all variables with double curly braces first and then replace them with their values
        for header_key in request_header_dict.keys():
            header_key_value = request_header_dict[header_key]
            vars_in_header_key_value = find_all_double_curly_braces_vars(header_key_value)
            TestLogger.scenario_logger_obj.debug(
                f"Prior variable replacement:\n"
                f"\theader_key: {header_key}\n"
                f"\theader_key_value: {header_key_value}\n"
                f"\tvars_in_header_key_value: {vars_in_header_key_value}"
            )
            header_key_value = replace_double_curly_braces_var_in_string(
                header_key_value,
                vars_in_header_key_value,
                self._environment_var_dict,
                self._scenario_obj.get_scenario_var_dict(),
                TestConfig
            )
            # Update header key value
            request_header_dict[header_key] = header_key_value

        TestLogger.scenario_logger_obj.debug(
            f"After variable replacement:\n"
            f"\trequest_header_dict: {request_header_dict}")
        return request_header_dict

    def _prepare_request_file(self):
        """
        Prepare request file

        Returns:
            Dict: Prepared files

        """
        files = []
        try:
            form_data = self._request_dict[BODY_KEY][FORMDATA_KEY]
        except KeyError:
            return None
        for data in form_data:
            if data[TYPE_KEY] == FILE_KEY:
                file_path = data[SRC_KEY]
                filename = file_path.split('/')[-1]
                file_ext = filename.split('.')[-1]
                file_type = CSV_FILE_TYPE if file_ext == CSV_FILE_EXT else JPEG_FILE_TYPE
                file_obj = ('file', (filename, open(data[SRC_KEY], 'rb'), file_type))
                files.append(file_obj)
                TestLogger.scenario_logger_obj.debug(
                    f"File path is specified:\n"
                    f"\tfile_path: '{file_path}'\n"
                    f"\tfile_path_exists: {os.path.exists(file_path)}\n")
        return files

    def _prepare_request_body(self):
        """
        Prepare request body by replacing all variable occurrences with their respective value.

        Returns:
            str: Prepared request body.
        """
        request_body = None
        if BODY_KEY in self._request_dict:
            if RAW_KEY in self._request_dict[BODY_KEY]:
                request_body = self._request_dict[BODY_KEY][RAW_KEY]
                # Find all variables with double curly braces first and then  replace them with their values
                vars_in_request_body = find_all_double_curly_braces_vars(request_body)
                TestLogger.scenario_logger_obj.debug(
                    f"Prior variable replacement:\n"
                    f"\tbody_key: {BODY_KEY}\n"
                    f"\trequest_body: {request_body}\n"
                    f"\tvars_in_request_body: {vars_in_request_body}"
                )
                request_body = replace_double_curly_braces_var_in_string(
                    request_body,
                    vars_in_request_body,
                    self._environment_var_dict,
                    self._scenario_obj.get_scenario_var_dict(),
                    TestConfig
                )
            elif FORMDATA_KEY in self._request_dict[BODY_KEY]:
                for data in self._request_dict[BODY_KEY][FORMDATA_KEY]:
                    if data[TYPE_KEY] != FILE_KEY:
                        request_body = {data[KEY_KEY]: data[VALUE_KEY]}
            elif URLENCODED_KEY in self._request_dict[BODY_KEY]:
                body_list = []
                for data in self._request_dict[BODY_KEY][URLENCODED_KEY]:
                    # check if value is variable
                    search_result = re.search(BODY_VAR_NAME_PATTERN, data[VALUE_KEY])
                    var_value = ''
                    if search_result:
                        var = search_result.group(1)
                        # Check if var is a dynamic var and it's supported
                        if DOLLAR_CHAR in var:
                            var_split = var.split(DOLLAR_CHAR)
                            offset_days = None
                            var_value = var_split[0]+replace_dynamic_variable(f'${var_split[-1]}', offset_days,
                                                                              TestConfig)
                        elif var in self._scenario_obj.get_scenario_var_dict():
                            # Get var value from scenario var dict first
                            var_value = self._scenario_obj.get_scenario_var_dict()[var]
                        elif var in self._environment_var_dict:
                            # Get var value from environment var dict
                            var_value = self._environment_var_dict[var]
                    else:
                        var_value = data[VALUE_KEY]
                    body_list.append(f'{data[KEY_KEY]}={var_value}')
                request_body = '&'.join(body_list)
            else:
                raise RawKeyDoesNotExistInDict(self._request_dict[BODY_KEY])

        TestLogger.scenario_logger_obj.debug(
            f"After variable replacement:\n"
            f"\trequest_body: {request_body}")
        return request_body

    def _process_post_request(self):
        """
        Prepare POST request, process pre-request events, submit request,
        validate its actual response, and process post-request events.

        Returns:
            Void
        """
        # Process pre-request events prior request preparation.
        TestLogger.scenario_logger_obj.info(
            f"Processing pre-request events:\n"
            f"\tList of exec list: {self._pre_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        self._pre_request_event_list_of_exec_list,
                                        self._scenario_obj,
                                        self._actual_response_obj)

        # Prepare request url.
        self._prepare_request_url()

        # Prepare request header.
        request_header = self._prepare_request_header()

        # Prepare request body.
        request_body = self._prepare_request_body()

        # Prepare request file
        request_file = self._prepare_request_file()

        # Submit request and keep its actual response.
        TestLogger.scenario_logger_obj.info(f"Submitting {self._request_method} request.")
        request_sessions_obj = TestConfig.get_requests_session_obj()

        # if there is request_file the request_body cannot be string or else the server going to throw error
        if request_file is None and request_body is not None:
            request_body = request_body.encode(UTF_8_VALUE)
        self._actual_response_obj = \
            request_sessions_obj.post(self._request_url,
                                      headers=request_header, data=request_body, files=request_file)
        TestLogger.scenario_logger_obj.debug(
            f"actual_response_obj:"
            f"\nRESPONSE object: {self._actual_response_obj}\n"
            f"\tstatus_code: {self._actual_response_obj.status_code}\n"
            f"\treason: {self._actual_response_obj.reason}\n"
            f"\ttext: {self._actual_response_obj.text}"
        )

        # Validate actual response
        self.validate_actual_response()

        # Process post-request events once an actual response is received.
        TestLogger.scenario_logger_obj.info(
            f"Processing post-request events:\n"
            f"\tList of exec list:{self._post_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        self._post_request_event_list_of_exec_list,
                                        self._scenario_obj,
                                        self._actual_response_obj)

    def _process_get_request(self):
        """
        Prepare GET request, process pre-request events, submit request,
        validate its actual response, and process post-request events.

        Returns:
            Void
        """
        # Process pre-request events prior request preparation.
        TestLogger.scenario_logger_obj.info(
            f"Processing pre-request events:\n"
            f"\tList of exec list: {self._pre_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        self._pre_request_event_list_of_exec_list,
                                        self._scenario_obj,
                                        self._actual_response_obj)

        # Prepare request url.
        self._prepare_request_url()

        # Prepare request header.
        request_header = self._prepare_request_header()

        # Prepare request query params.
        request_query_params = self._prepare_request_query_params()

        # Submit request and keep its actual response.
        TestLogger.scenario_logger_obj.info(f"Submitting {self._request_method} request.")
        request_sessions_obj = TestConfig.get_requests_session_obj()
        if request_query_params is None:
            self._actual_response_obj = \
                request_sessions_obj.get(self._request_url,
                                         headers=request_header)
        else:
            self._actual_response_obj = \
                request_sessions_obj.get(self._request_url,
                                         headers=request_header,
                                         params=request_query_params)
        TestLogger.scenario_logger_obj.debug(
            f"actual_response_obj:"
            f"\nRESPONSE object: {self._actual_response_obj}\n"
            f"\tstatus_code: {self._actual_response_obj.status_code}\n"
            f"\treason: {self._actual_response_obj.reason}\n"
            f"\ttext: {self._actual_response_obj.text}"
        )

        # Validate actual response
        self.validate_actual_response()

        # Process post-request events once an actual response is received.
        TestLogger.scenario_logger_obj.info(
            f"Processing post-request events:\n"
            f"\tList of exec list:{self._post_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        self._post_request_event_list_of_exec_list,
                                        self._scenario_obj,
                                        self._actual_response_obj)

    def _process_put_request(self):
        """
        Prepare PUT request, process pre-request events, submit request,
        validate its actual response, and process post-request events.

        Returns:
            Void
        """
        # Process pre-request events prior request preparation.
        TestLogger.scenario_logger_obj.info(
            f"Processing pre-request events:\n"
            f"\tList of exec list: {self._pre_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        self._pre_request_event_list_of_exec_list,
                                        self._scenario_obj,
                                        self._actual_response_obj)

        # Prepare request url.
        self._prepare_request_url()

        # Prepare request header.
        request_header = self._prepare_request_header()

        # Prepare request body.
        request_body = self._prepare_request_body()

        # Submit request and keep its actual response.
        TestLogger.scenario_logger_obj.info(f"Submitting {self._request_method} request.")
        request_sessions_obj = TestConfig.get_requests_session_obj()
        if request_body is None:
            self._actual_response_obj = \
                request_sessions_obj.put(self._request_url,
                                         headers=request_header)
        else:
            self._actual_response_obj = \
                request_sessions_obj.put(self._request_url,
                                         headers=request_header,
                                         data=request_body.encode(UTF_8_VALUE))
        TestLogger.scenario_logger_obj.debug(
            f"actual_response_obj:"
            f"\nRESPONSE object: {self._actual_response_obj}\n"
            f"\tstatus_code: {self._actual_response_obj.status_code}\n"
            f"\treason: {self._actual_response_obj.reason}\n"
            f"\ttext: {self._actual_response_obj.text}"
        )

        # Validate actual response
        self.validate_actual_response()

        # Process post-request events once an actual response is received.
        TestLogger.scenario_logger_obj.info(
            f"Processing post-request events:\n"
            f"\tList of exec list:{self._post_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        self._post_request_event_list_of_exec_list,
                                        self._scenario_obj,
                                        self._actual_response_obj)

    def _process_delete_request(self):
        """
        Prepare DELETE request, process pre-request events, submit request,
        validate its actual response, and process post-request events.

        Returns:
            Void
        """
        # Process pre-request events prior request preparation.
        TestLogger.scenario_logger_obj.info(
            f"Processing pre-request events:\n"
            f"\tList of exec list: {self._pre_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        self._pre_request_event_list_of_exec_list,
                                        self._scenario_obj,
                                        self._actual_response_obj)

        # Prepare request url.
        self._prepare_request_url()

        # Prepare request header.
        request_header = self._prepare_request_header()

        # Prepare request body.
        request_body = self._prepare_request_body()

        # Submit request and keep its actual response.
        TestLogger.scenario_logger_obj.info(f"Submitting {self._request_method} request.")
        request_sessions_obj = TestConfig.get_requests_session_obj()
        if request_body is None:
            self._actual_response_obj = \
                request_sessions_obj.delete(self._request_url,
                                            headers=request_header)
        else:
            self._actual_response_obj = \
                request_sessions_obj.delete(self._request_url,
                                            headers=request_header,
                                            data=request_body.encode(UTF_8_VALUE))
        TestLogger.scenario_logger_obj.debug(
            f"actual_response_obj:"
            f"\nRESPONSE object: {self._actual_response_obj}\n"
            f"\tstatus_code: {self._actual_response_obj.status_code}\n"
            f"\treason: {self._actual_response_obj.reason}\n"
            f"\ttext: {self._actual_response_obj.text}"
        )

        # Validate actual response
        self.validate_actual_response()

        # Process post-request events once an actual response is received.
        TestLogger.scenario_logger_obj.info(
            f"Processing post-request events:\n"
            f"\tList of exec list:{self._post_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        self._post_request_event_list_of_exec_list,
                                        self._scenario_obj,
                                        self._actual_response_obj)

    def _process_patch_request(self):
        """
        Prepare PATCH request, process pre-request events, submit request,
        validate its actual response, and process post-request events.

        Returns:
            Void
        """
        # Process pre-request events prior request preparation.
        TestLogger.scenario_logger_obj.info(
            f"Processing pre-request events:\n"
            f"\tList of exec list: {self._pre_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        self._pre_request_event_list_of_exec_list,
                                        self._scenario_obj,
                                        self._actual_response_obj)

        # Prepare request url.
        self._prepare_request_url()

        # Prepare request header.
        request_header = self._prepare_request_header()

        # Prepare request body.
        request_body = self._prepare_request_body()

        # Submit request and keep its actual response.
        TestLogger.scenario_logger_obj.info(f"Submitting {self._request_method} request.")
        request_sessions_obj = TestConfig.get_requests_session_obj()
        if request_body is None:
            self._actual_response_obj = \
                request_sessions_obj.patch(self._request_url,
                                           headers=request_header)
        else:
            self._actual_response_obj = \
                request_sessions_obj.patch(self._request_url,
                                           headers=request_header,
                                           data=request_body.encode(UTF_8_VALUE))
        TestLogger.scenario_logger_obj.debug(
            f"actual_response_obj:"
            f"\nRESPONSE object: {self._actual_response_obj}\n"
            f"\tstatus_code: {self._actual_response_obj.status_code}\n"
            f"\treason: {self._actual_response_obj.reason}\n"
            f"\ttext: {self._actual_response_obj.text}"
        )

        # Validate actual response
        self.validate_actual_response()

        # Process post-request events once an actual response is received.
        TestLogger.scenario_logger_obj.info(
            f"Processing post-request events:\n"
            f"\tList of exec list:{self._post_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        self._post_request_event_list_of_exec_list,
                                        self._scenario_obj,
                                        self._actual_response_obj)

    def _process_options_request(self):
        """
        Prepare PATCH request, process pre-request events, submit request,
        validate its actual response, and process post-request events.

        Returns:
            Void
        """
        # Process pre-request events prior request preparation.
        TestLogger.scenario_logger_obj.info(
            f"Processing pre-request events:\n"
            f"\tList of exec list: {self._pre_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        self._pre_request_event_list_of_exec_list,
                                        self._scenario_obj,
                                        self._actual_response_obj)

        # Prepare request url.
        self._prepare_request_url()

        # Prepare request header.
        request_header = self._prepare_request_header()

        # Prepare request body.
        request_body = self._prepare_request_body()

        # Submit request and keep its actual response.
        TestLogger.scenario_logger_obj.info(f"Submitting {self._request_method} request.")
        request_sessions_obj = TestConfig.get_requests_session_obj()
        if request_body is None:
            self._actual_response_obj = \
                request_sessions_obj.options(self._request_url,
                                             headers=request_header)
        else:
            self._actual_response_obj = \
                request_sessions_obj.options(self._request_url,
                                             headers=request_header,
                                             data=request_body.encode(UTF_8_VALUE))
        TestLogger.scenario_logger_obj.debug(
            f"actual_response_obj:"
            f"\nRESPONSE object: {self._actual_response_obj}\n"
            f"\tstatus_code: {self._actual_response_obj.status_code}\n"
            f"\treason: {self._actual_response_obj.reason}\n"
            f"\ttext: {self._actual_response_obj.text}"
        )

        # Validate actual response
        self.validate_actual_response()

        # Process post-request events once an actual response is received.
        TestLogger.scenario_logger_obj.info(
            f"Processing post-request events:\n"
            f"\tList of exec list:{self._post_request_event_list_of_exec_list}"
        )
        process_event_list_of_exec_list(TestConfig,
                                        TestLogger,
                                        self._post_request_event_list_of_exec_list,
                                        self._scenario_obj,
                                        self._actual_response_obj)

    # Public methods
    def process_request(self):
        """
        Prepare request and submit it depending on its method and keep its actual response.

        Returns:
            Void
        """
        self._actual_response_obj = None
        if self._request_method == POST_METHOD_VALUE:
            self._process_post_request()
            TestLogger.add_request_url_to_api_calls_dict(self._request_method, self._request_url)
        elif self._request_method == OPTIONS_METHOD_VALUE:
            self._process_options_request()
        elif self._request_method == GET_METHOD_VALUE:
            self._process_get_request()
            TestLogger.add_request_url_to_api_calls_dict(self._request_method, self._request_url)
        elif self._request_method == PUT_METHOD_VALUE:
            self._process_put_request()
            TestLogger.add_request_url_to_api_calls_dict(self._request_method, self._request_url)
        elif self._request_method == DELETE_METHOD_VALUE:
            self._process_delete_request()
            TestLogger.add_request_url_to_api_calls_dict(self._request_method, self._request_url)
        elif self._request_method == PATCH_METHOD_VALUE:
            self._process_patch_request()
            TestLogger.add_request_url_to_api_calls_dict(self._request_method, self._request_url)
        else:
            # Raise error for request method that isn't supported
            raise RequestMethodNotSupportedError(self._request_method)

    def validate_actual_response(self):
        """
        Validate actual response.

        Returns:
            Void
        """
        # Validate actual response against expected response(s), only if response(s)
        # exist in the scenario JSON.
        if self._response_dict_list is not None and self._response_dict_list:
            # Response dict list exists, so validate the response(s) in the list.
            # Note that the list can be empty and thus there is no response to validate.
            TestLogger.scenario_logger_obj.info(f"Validating expected response(s).")

            # Set result dictionary
            result = {CODE_KEY: True, STATUS_KEY: True, BODY_KEY: True}
            expected_response_code = ''
            expected_response_status = ''
            expected_response_body_dict = {}
            actual_response_dict = {}

            for expected_response_dict in self._response_dict_list:
                if CODE_KEY in expected_response_dict:
                    expected_response_code = expected_response_dict[CODE_KEY]
                    TestLogger.scenario_logger_obj.debug(
                        f"Validating response code:\n"
                        f"\texpected_response_code: {expected_response_code}\n"
                        f"\tactual_response_code: {self._actual_response_obj.status_code}")
                    result[CODE_KEY] = (expected_response_code == self._actual_response_obj.status_code)

                if STATUS_KEY in expected_response_dict:
                    expected_response_status = expected_response_dict[STATUS_KEY]
                    TestLogger.scenario_logger_obj.debug(
                        f"Validating response status:\n"
                        f"\texpected_response_status: {expected_response_status}\n"
                        f"\tactual_response_status: {self._actual_response_obj.reason}")
                    # response.ok returns True if status_code is less than 400, otherwise False
                    if expected_response_status == STATUS_OK_RESPONSE:
                        result[STATUS_KEY] = self._actual_response_obj.ok
                    else:
                        result[STATUS_KEY] = (expected_response_status == self._actual_response_obj.reason)

                if BODY_KEY in expected_response_dict:
                    # Check first if request was successful
                    if result[CODE_KEY]:
                        # Request was successful, expected response body and actual response text
                        # need to be converted to dictionaries using json.loads() first.
                        try:
                            actual_response_dict = json.loads(self._actual_response_obj.text)
                            expected_response_body = expected_response_dict[BODY_KEY]
                            # Find all variables with double curly braces first and then  replace them with their values
                            vars_in_response_body = find_all_double_curly_braces_vars(expected_response_body)
                            TestLogger.scenario_logger_obj.debug(
                                f"Prior variable replacement:\n"
                                f"\tbody_key: {BODY_KEY}\n"
                                f"\tresponse_body: {expected_response_body}\n"
                                f"\tvars_in_response_body: {vars_in_response_body}"
                            )
                            expected_response_body = replace_double_curly_braces_var_in_string(
                                expected_response_body,
                                vars_in_response_body,
                                self._environment_var_dict,
                                self._scenario_obj.get_scenario_var_dict(),
                                TestConfig
                            )
                            expected_response_body_dict = json.loads(expected_response_body)

                            # Check if expected response body dictionary matches the
                            # actual response body dictionary.

                            # check if partial response validation is required
                            # returns <validation_method> if partial validation required, None otherwise
                            is_partial_response_validation = get_is_partial_response_validation \
                                (self._pre_request_event_list_of_exec_list)

                            # if the value is not None, then partial validation is required
                            if is_partial_response_validation is not None:
                                TestLogger.scenario_logger_obj.debug(
                                    f"Partially validating response body dict: "
                                    f"{is_partial_response_validation}\n"
                                    f"\texpected response body dict: {expected_response_body_dict}\n"
                                    f"\tactual response body dict: {actual_response_dict}")
                                # Perform partial validation without excluding properties
                                # True if partial response validation is success, False otherwise
                                result[BODY_KEY] = perform_partial_response_validation(
                                    DeepDiff(expected_response_body_dict, actual_response_dict),
                                    is_partial_response_validation)
                            else:
                                # Remove excluded properties from the actual dict and expected resp body dict
                                actual_response_excl_props = TestConfig.get_actual_resp_body_excluded_properties()
                                deep_delete_keys_from_object(actual_response_excl_props,
                                                             actual_response_dict)
                                deep_delete_keys_from_object(actual_response_excl_props,
                                                             expected_response_body_dict)

                                # Perform full validation of expected and actual resp body object
                                TestLogger.scenario_logger_obj.debug(
                                    f"Fully Validating response body dict after removing exclude properties:\n"
                                    f"\texpected response body dict: {expected_response_body_dict}\n"
                                    f"\tactual response body dict: {actual_response_dict}")
                                result[BODY_KEY] = (expected_response_body_dict == actual_response_dict)

                        except ValueError:
                            # Compare expected response body text and actual response text directly
                            TestLogger.scenario_logger_obj.debug(
                                f"Exception in validating response body text:\n"
                                f"\texpected response body text: {expected_response_dict[BODY_KEY]}\n"
                                f"\tactual response body text: {self._actual_response_obj.text}")

                            if not (expected_response_dict[BODY_KEY] == self._actual_response_obj.text):
                                # Raise no match error
                                raise ExpectedResponseBodyDoesNotMatchError(
                                    expected_response_dict[BODY_KEY],
                                    self._actual_response_obj.text)

                if all(result.values()):
                    break

            if not all(result.values()):
                if not result[CODE_KEY]:
                    raise ExpectedResponseCodeDoesNotMatchError(
                        expected_response_code,
                        self._actual_response_obj.status_code)
                if not result[STATUS_KEY]:
                    raise ExpectedResponseStatusDoesNotMatchError(
                        expected_response_status,
                        self._actual_response_obj.reason)
                if not result[BODY_KEY]:
                    TestLogger.scenario_logger_obj\
                        .debug(f'Diff Response: {DeepDiff(expected_response_body_dict, actual_response_dict)}')
                    raise ExpectedResponseBodyDoesNotMatchError(
                        expected_response_body_dict,
                        actual_response_dict)

        else:
            TestLogger.scenario_logger_obj.info(
                f"Nothing to validate. Expected response(s) is either empty or not specified in the scenario file.")

        # At his point response validation was successful, build the response body dict text
        # If there are excluded properties from the response body and the response body,
        # is a dict, then remove them from the response body dict. Otherwise, do nothing.
        response_body_dict_text = self._actual_response_obj.text
        if self._actual_response_obj.status_code == STATUS_CODE_200:
            excluded_properties = TestConfig.get_actual_resp_body_excluded_properties()
            if not(excluded_properties is None) and response_body_dict_text:
                try:
                    response_body_obj = json.loads(response_body_dict_text)
                    # If response_body_obj is a dict,
                    # then delete the excluded properties from the response_body_obj
                    if type(response_body_obj) is dict:
                        for excluded_property in excluded_properties:
                            if excluded_property in response_body_obj:
                                del response_body_obj[excluded_property]
                    response_body_dict_text = json.dumps(response_body_obj)
                except JSONDecodeError:
                    # some body response is image so couldn't be decoded by json
                    pass

        # Build actual response dict list from actual response obj
        actual_response_dict_list = []
        actual_response_dict = {
            CODE_KEY: self._actual_response_obj.status_code,
            STATUS_KEY: self._actual_response_obj.reason,
            BODY_KEY: response_body_dict_text
        }
        actual_response_dict_list.append(actual_response_dict)
        # Add actual response dict list to its corresponding item in _scenario_obj using its _index
        self._scenario_obj.add_actual_response_dict_list_to_item(self._index, actual_response_dict_list)
