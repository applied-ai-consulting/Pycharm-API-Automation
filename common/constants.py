# Paths
CONFIGS_PATH = "./configs/"
DATA_PATH = "./data/"
LOGS_PATH = "./logs/"

# File name extensions
JSON_FILE_EXT = ".json"
POSTMAN_COLLECTION_FILE_EXT = ".postman_collection"
LOG_FILE_EXT = ".log"
CSV_FILE_EXT = "csv"
CSV_FILE_TYPE = "text/csv"
JPEG_FILE_TYPE = "image/jpeg"
# Dictionary keys in scenario set file
NAME_KEY = "name"
DATA_DIRS_KEY = "data_dirs"
DATA_DIR_KEY = "data_dir"
PATTERNS_KEY = "patterns"

# Dictionary keys in test config file
TEST_TYPE_KEY = "test_type"
SUT_KEY = "system_under_test"
HOSTNAME_KEY = "hostname"
ENV_VARS_KEY = "environment_variables"
URL_KEY = "url"
API_PATH_KEY = "api_path"
ACTUAL_RESP_VAL_KEY = "actual_response_validation"
RESPONSE_BODY_KEY = "response_body"
EXCLUDED_PROPERTIES_KEY = "excluded_properties"

# Dictionary keys in Postman Collection JSON schema (format)
METHOD_KEY = "method"
BODY_KEY = "body"
HEADER_KEY = "header"
RAW_KEY = "raw"
VAR_KEY = "variable"
INFO_KEY = "info"
DESC_KEY = "description"
ITEM_KEY = "item"
REQUEST_KEY = "request"
RESPONSE_KEY = "response"
KEY_KEY = "key"
VALUE_KEY = "value"
CODE_KEY = "code"
STATUS_KEY = "status"
EVENT_KEY = "event"
LISTEN_KEY = "listen"
SCRIPT_KEY = "script"
EXEC_KEY = "exec"
FILE_KEY = "file"
TYPE_KEY = "type"
QUERY_KEY = "query"
SRC_KEY = "src"
FORMDATA_KEY = "formdata"
URLENCODED_KEY = "urlencoded"

# Dictionary keys in Deep Diff results
DICTIONARY_ITEM_REMOVED_KEY = "dictionary_item_removed"
VALUES_CHANGED_KEY = "values_changed"

# HTTP status codes
STATUS_CODE_200 = 200
STATUS_CODE_500 = 500
STATUS_OK_RESPONSE = "OK"

# Key values
PREREQUEST_KEY_VALUE = "prerequest"
TEST_KEY_VALUE = "test"
GET_METHOD_VALUE = "GET"
POST_METHOD_VALUE = "POST"
PUT_METHOD_VALUE = "PUT"
DELETE_METHOD_VALUE = "DELETE"
PATCH_METHOD_VALUE = "PATCH"
OPTIONS_METHOD_VALUE = "OPTIONS"

# Regex patterns
VAR_NAME_PATTERN = "{{[a-zA-Z0-9_$+-]+}}"
BODY_VAR_NAME_PATTERN = "{{([A-Za-z0-9_$]+)}}"
PROTOCOL_PATTERN = r'http(s)?:\/\/'
DATE_NUM_PATTERN = "[_+-].*"
ALPHA_ONLY_PATTERN = "[a-zA-Z]+"
NUM_ONLY_PATTERN = "[0-9]+"
PLUS_CHAR = '+'
MINUS_CHAR = '-'

# Names
DEFAULT_TEST_CONFIG_YAML_FILE_NAME = "test_config.yaml"
DEFAULT_SCENARIO_SET_YAML_FILE_NAME = "scenario_set.yaml"
DEFAULT_SCENARIO_SET_PATTERNS = "*"
DEFAULT_API_CALLS_CSV_FILE_NAME = "api_calls.csv"
TEST_LOGGER_NAME = "test_logger"
SCENARIO_LOGGER_NAME = "scenario_logger"

# Miscellaneous values
UTF_8_VALUE = "utf-8"
SPACE_CHAR = " "
DOLLAR_CHAR = "$"

# Markup-related constants
# ------------------------
# Markup delimiter
MARKUP_DELIMITER = ":"
RESPONSE_PROPERTY_VALUE_DELIMITER = "."

# Markup Regex pattern
MARKUP_STMT_PATTERN = "<[a-zA-Z0-9_:.@$%\\/\\s\\-{}\\\\+\[\]]+>"

# Markup operations
SKIP_MARKUP_OP = "skip"
XFAIL_MARKUP_OP = "xfail"
SET_VARIABLE_MARKUP_OP = "set-variable"
REFER_SCENARIO_FILE_MARKUP = "refer-scenario-file"
PARTIAL_RESPONSE_VALIDATION_MARKUP_OP = "is-partial-response-validation"

# Markup objects
VALUE_MARKUP_OBJ = "value"
RESPONSE_MARKUP_OBJ = "response"
KEYS_AND_VALUES_MARKUP_OBJ = "keys_and_values"
KEYS_ONLY_MARKUP_OBJ = "keys_only"

# Markup dictionary
MARKUP_ARITY_DICT = {
    SKIP_MARKUP_OP: 2,
    XFAIL_MARKUP_OP: 2,
    SET_VARIABLE_MARKUP_OP: 4,
    REFER_SCENARIO_FILE_MARKUP: 4,
    PARTIAL_RESPONSE_VALIDATION_MARKUP_OP: 2
}

# Markup lists
MARKUP_OP_LIST = MARKUP_ARITY_DICT.keys()
MARKUP_OBJ_LIST = [
    VALUE_MARKUP_OBJ,
    RESPONSE_MARKUP_OBJ,
    KEYS_AND_VALUES_MARKUP_OBJ,
    KEYS_ONLY_MARKUP_OBJ
]
MARKUP_ARITY_LIST = list(set(MARKUP_ARITY_DICT.values()))

# Dynamic variables
GUID_DYN_VAR = "$guid"
RANDOM_POSITIVE_INTEGER_DYN_VAR = "$randomPositiveInteger"
RANDOM_NEGATIVE_INTEGER_DYN_VAR = "$randomNegativeInteger"
RANDOM_ALPHA_NUMERIC_DYN_VAR = "$randomAlphaNumeric"
RANDOM_PASSWORD_DYN_VAR = "$randomPassword"
CURRENT_DATE_DYN_VAR = "$currentDate"
RANDOM_DATE_PAST_DYN_VAR = "$randomDatePast"
RANDOM_DATE_FUTURE_DYN_VAR = "$randomDateFuture"
RANDOM_START_DATETIME_FUTURE_DYN_VAR = "$randomStartDateTimeFuture"
RANDOM_END_DATETIME_FUTURE_DYN_VAR = "$randomEndDateTimeFuture"

# Dynamic variable list
DYNAMIC_VAR_LIST = {
    GUID_DYN_VAR,
    RANDOM_POSITIVE_INTEGER_DYN_VAR,
    RANDOM_NEGATIVE_INTEGER_DYN_VAR,
    RANDOM_ALPHA_NUMERIC_DYN_VAR,
    RANDOM_PASSWORD_DYN_VAR,
    CURRENT_DATE_DYN_VAR,
    RANDOM_DATE_PAST_DYN_VAR,
    RANDOM_DATE_FUTURE_DYN_VAR,
    RANDOM_START_DATETIME_FUTURE_DYN_VAR,
    RANDOM_END_DATETIME_FUTURE_DYN_VAR,
}

# Dynamic variable related miscellaneous constants
RANDOM_ALPHA_NUMERIC_LEN = 16
RANDOM_PASSWORD_LEN = 8
RANDOM_SPECIAL_CHAR_SET = "%$@#!&"
RANDOM_MAX_DAYS = 365
RANDOM_DATE_FORMAT = "%Y-%m-%d"
RANDOM_DURATION_MINUTES = 3
RANDOM_DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
DATETIME_DEFAULT_TIMEZONE = 'GMT'
UPLOAD_CSV_1 = 'LB-1141_10K_A.csv'
UPLOAD_CSV_2 = 'LB-1141_10K_B.csv'
UPLOAD_CSV_3 = 'LB-1141_10K_C.csv'
