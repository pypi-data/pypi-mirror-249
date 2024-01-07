import json
import os
import sys

from dotenv import load_dotenv

from .LoggerOutputEnum import LoggerOutputEnum
from .MessageSeverity import MessageSeverity

load_dotenv()

# TODO If there is no .logger.json file, please write to the console in which directory we should create it.
# TODO If there is .logger.json file (we support only one right?) , please write to the console the configuration.
# TODO Can we use SeverityLevelName instead of SeverityLevelId in the .logger.json? - Please add .logger.json.examples
# TODO Can we add the component name in addition to the component id in the .logger.json? - Please add .logger.json.examples
# TODO Can we add comments to the .logger.json file?

DEFAULT_MIN_SEVERITY = 600

LOGGER_CONFIGURATION_JSON = os.getenv('LOGGER_CONFIGURATION_JSON_PATH')
LOGGER_MINIMUM_SEVERITY = os.getenv('LOGGER_MINIMUM_SEVERITY')
PRINTED_ENVIRONMENT_VARIABLES = False


class DebugMode:
    def __init__(self, logger_minimum_severity: int | str = None):
        global PRINTED_ENVIRONMENT_VARIABLES
        # set default values that may be overridden
        self.debug_everything = False
        self.logger_json = {}

        # Minimal severity in case there is not LOGGER_MINIMUM_SEVERITY environment variable
        logger_minimum_severity = logger_minimum_severity or LOGGER_MINIMUM_SEVERITY
        if logger_minimum_severity is None:
            self.logger_minimum_severity = DEFAULT_MIN_SEVERITY
            if not PRINTED_ENVIRONMENT_VARIABLES:
                print(f"Using LOGGER_MINIMUM_SEVERITY={DEFAULT_MIN_SEVERITY} from Logger default "
                      "(can be overridden by LOGGER_MINIMUM_SEVERITY environment variable or .logger.json file "
                      "per component and logger output")

        else:
            self.logger_minimum_severity = self.__get_severity_level(logger_minimum_severity)
            if not PRINTED_ENVIRONMENT_VARIABLES:
                print(f"Using LOGGER_MINIMUM_SEVERITY={LOGGER_MINIMUM_SEVERITY} from environment variable. "
                      f"Can be overridden by .logger.json file per component and logger output.")
        PRINTED_ENVIRONMENT_VARIABLES = True

        try:
            logger_configuration_json = LOGGER_CONFIGURATION_JSON
            if not LOGGER_CONFIGURATION_JSON:
                caller_dir_parent = os.path.dirname(sys.path[0])
                logger_configuration_json = os.path.join(caller_dir_parent, '.logger.json')

            if os.path.exists(logger_configuration_json):
                with open(logger_configuration_json, 'r') as file:
                    self.logger_json = json.load(file)
                for component_id, component_info in self.logger_json.items():
                    for logger_output, severity_level in component_info.items():
                        component_info[logger_output] = self.__get_severity_level(severity_level)
            else:
                self.debug_everything = True
        # TODO MiniLogger.exception() in all exceptions
        except Exception:
            raise

    def is_logger_output(self, component_id: str, logger_output: LoggerOutputEnum, severity_level: int) -> bool:
        # Debug everything that has a severity level higher than the minimum required
        if self.debug_everything:
            return severity_level >= self.logger_minimum_severity

        severity_level = max(severity_level, self.logger_minimum_severity)
        if component_id not in self.logger_json:
            component_id = "default"

        if component_id in self.logger_json:
            output_info = self.logger_json[component_id]
            if logger_output.value in output_info:
                result = severity_level >= output_info[logger_output.value]
                return result

        # In case the component does not exist in the logger configuration file or the logger_output was not specified
        return True

    @staticmethod
    def __get_severity_level(severity_level: int | str) -> int:
        if str(severity_level) == "Info":
            severity_level = "Information"

        if hasattr(MessageSeverity, str(severity_level)):
            severity_level = MessageSeverity[severity_level].value
        elif str(severity_level).isdigit():
            severity_level = int(severity_level)
        else:
            raise Exception(f"invalid severity level {severity_level}")
        return severity_level
