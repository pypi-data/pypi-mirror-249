import json
import os

from cdh_dav_python.cdc_admin_service import (
    environment_tracing as cdc_env_tracing,
    environment_logging as cdc_env_logging,
)


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class EnvironmentString:
    """
    A utility class for working with environment strings.
    """

    @staticmethod
    def is_valid_json(json_string):
        """
        Check if a given string is a valid JSON.

        Args:
            json_string (str): The string to be checked.

        Returns:
            bool: True if the string is a valid JSON, False otherwise.
        """

        try:
            json.loads(json_string)
            return True
        except ValueError:
            return False
