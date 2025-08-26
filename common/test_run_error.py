class TestRunError(Exception):
    """
    Basic exception for errors raised by Test Scenario Runner.
    """

    def __init__(self, msg=None):
        if msg is None:
            # Set default error message
            msg = "An error occurred during a test scenario execution."
        super(TestRunError, self).__init__(msg)


class RequestMethodNotSupportedError(TestRunError):
    """
    Error for request method that is not supported by the test framework yet.
    """

    def __init__(self, request_method):
        msg = f"Request method {request_method} is not supported by the test framework yet."
        super(RequestMethodNotSupportedError, self).__init__(msg)


class ExpectedResponseCodeDoesNotMatchError(TestRunError):
    """
    Error for expected response code doesn't match the actual one.
    """

    def __init__(self, exp_value, act_value):
        msg = f"The expected response code '{exp_value}' does not match the actual response code '{act_value}'."
        super(ExpectedResponseCodeDoesNotMatchError, self).__init__(msg)


class ExpectedResponseStatusDoesNotMatchError(TestRunError):
    """
    Error for expected response status doesn't match the actual one.
    """

    def __init__(self, exp_value, act_value):
        msg = f"The expected response status '{exp_value}' does not match the actual response status '{act_value}'."
        super(ExpectedResponseStatusDoesNotMatchError, self).__init__(msg)


class ExpectedResponseBodyDoesNotMatchError(TestRunError):
    """
    Error for expected response body doesn't match the actual one.
    """

    def __init__(self, exp_value, act_value):
        msg = f"The expected response body '{exp_value}' does not match the actual response body '{act_value}'."
        super(ExpectedResponseBodyDoesNotMatchError, self).__init__(msg)


class UnknownMarkupOperationError(TestRunError):
    """
    Error for unknown markup operation.
    """

    def __init__(self, markup_op):
        msg = f"Unknown markup operation '{markup_op}'."
        super(UnknownMarkupOperationError, self).__init__(msg)


class ReferredScenarioVarsNotSubsetError(TestRunError):
    """
    Error for referred scenario variables are not a subset of its referrer's scenario variables.
    """

    def __init__(self, referred_scenario_var_dict, referrer_scenario_var_dict):
        msg = f"Referred scenario vars '{referred_scenario_var_dict}' are not a subset of " \
              f"its referrer's scenario vars '{referrer_scenario_var_dict}'."
        super(ReferredScenarioVarsNotSubsetError, self).__init__(msg)


class ScenarioFileReferenceCycleError(TestRunError):
    """
    Error for scenario file reference cycle existence.
    """

    def __init__(self, referred_scenario_json_file):
        msg = f"Reference cycle exists when referring scenario JSON file'{referred_scenario_json_file}'."
        super(ScenarioFileReferenceCycleError, self).__init__(msg)


class PropertyDoesNotExistInActualResponseBody(TestRunError):
    """
    Error for expected response body doesn't match the actual one.
    """

    def __init__(self, property_name):
        msg = f"The property {property_name} doesn't exist in the actual response body."
        super(PropertyDoesNotExistInActualResponseBody, self).__init__(msg)


class RawKeyDoesNotExistInDict(TestRunError):
    """
    Error for RAW key which doesn't exist in dictionary.
    """

    def __init__(self, input_dict):
        msg = f"RAW key doesn't exist in the dictionary {input_dict}."
        super(RawKeyDoesNotExistInDict, self).__init__(msg)


class BodyKeyDoesNotExistInDict(TestRunError):
    """
    Error for BODY key which doesn't exist in dictionary.
    """

    def __init__(self, input_dict):
        msg = f"BODY key doesn't exist in the dictionary {input_dict}."
        super(BodyKeyDoesNotExistInDict, self).__init__(msg)


class UrlKeyDoesNotExistInDict(TestRunError):
    """
    Error for URL key which doesn't exist in dictionary.
    """

    def __init__(self, input_dict):
        msg = f"URL key doesn't exist in the dictionary {input_dict}."
        super(UrlKeyDoesNotExistInDict, self).__init__(msg)


class ItemProcessingErrorsEncountered(TestRunError):
    """
    Error for error occurrence during item processing.
    """

    def __init__(self, error_count, item_index_list):
        msg = f"During item processing, {error_count} error(s) were encountered " \
              f"which occurred in the following item index(es) {item_index_list}."

        super(ItemProcessingErrorsEncountered, self).__init__(msg)


class NameKeyDoesNotExistInObject(TestRunError):
    """
    Error for NAME key which doesn't exist in an object.
    """

    def __init__(self, obj_name):
        msg = f"NAME key doesn't exist in {obj_name}."
        super(NameKeyDoesNotExistInObject, self).__init__(msg)


class DynamicVariableIsNotSupported(TestRunError):
    """
    Error for a dynamic variable which is not supported.
    """

    def __init__(self, obj_name):
        msg = f"Dynamic variable {obj_name} is not supported."
        super(DynamicVariableIsNotSupported, self).__init__(msg)


class DynamicVariableOperatorNotAllowed(TestRunError):
    """
    Error for '+' or '-' operator not allowed for Dynamic variable
    """

    def __init__(self, dyn_var):
        msg = f"'+' or '-' is not supported for {dyn_var}"
        super(DynamicVariableOperatorNotAllowed, self).__init__(msg)


class OperatorNotAllowed(TestRunError):
    """
    Error for operator other than '+' or '-' if used in dynamic variable $currentDate
    """

    def __init__(self, operator):
        msg = f"{operator} is not supported"
        super(OperatorNotAllowed, self).__init__(msg)


class InvalidNumOfDaysInDynVariable(TestRunError):
    """
    Invalid days provided along with Dynamic Variable $currentDate. e.g., $currentDate+1-2
    """

    def __init__(self, num_days):
        msg = f"{num_days} is not supported"
        super(InvalidNumOfDaysInDynVariable, self).__init__(msg)
