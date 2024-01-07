import json
import os

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
LOGGER_CONFIGURATION_JSON = '.logger.json'
LOGGER_MINIMUM_SEVERITY = os.getenv('LOGGER_MINIMUM_SEVERITY')
PRINTED_ENVIRONMENT_VARIABLES = False


class DebugMode:
    def __init__(self, logger_minimum_severity: int | str = LOGGER_MINIMUM_SEVERITY):
        global PRINTED_ENVIRONMENT_VARIABLES
        # set default values that may be overridden
        self.debug_everything = False
        self.logger_json = {}

        # Minimal severity in case there is not LOGGER_MINIMUM_SEVERITY environment variable
        if logger_minimum_severity is None:
            self.logger_minimum_severity = DEFAULT_MIN_SEVERITY
            if not PRINTED_ENVIRONMENT_VARIABLES:
                print(f"Using LOGGER_MINIMUM_SEVERITY={DEFAULT_MIN_SEVERITY} from Logger default "
                      "(can be overridden by LOGGER_MINIMUM_SEVERITY environment variable or .logger.json file "
                      "per component and logger output")

        else:
            if str(logger_minimum_severity) == "Info":
                logger_minimum_severity = "Information"
            if hasattr(MessageSeverity, str(logger_minimum_severity)):
                self.logger_minimum_severity = MessageSeverity[logger_minimum_severity].value
            elif str(logger_minimum_severity).isdigit():
                self.logger_minimum_severity = int(logger_minimum_severity)
            else:
                raise Exception("LOGGER_MINIMUM_SEVERITY must be a valid LoggerOutputEnum or a number or None "
                                f"(not {logger_minimum_severity})")
            if not PRINTED_ENVIRONMENT_VARIABLES:
                print(f"Using LOGGER_MINIMUM_SEVERITY={LOGGER_MINIMUM_SEVERITY} from environment variable. "
                      f"Can be overridden by .logger.json file per component and logger output.")
        PRINTED_ENVIRONMENT_VARIABLES = True

        try:
            with open(LOGGER_CONFIGURATION_JSON, 'r') as file:
                self.logger_json = json.load(file)
        except FileNotFoundError:
            self.debug_everything = True
        # TODO MiniLogger.exception() in all exceptions
        except Exception:
            raise

    def is_logger_output(self, component_id: str, logger_output: LoggerOutputEnum, severity_level: int) -> bool:
        # Debug everything that has a severity level higher than the minimum required
        if self.debug_everything:
            return True

        severity_level = max(severity_level, self.logger_minimum_severity)
        if component_id in self.logger_json:
            output_info = self.logger_json[component_id]
            if logger_output in output_info:
                result = severity_level >= output_info[logger_output]
                return result

        # In case the component does not exist in the logger configuration file or the logger_output was not specified
        return True
