"""
This module provides a class to interact with secret scopes in Databricks.
"""

import sys
import os
import json
import subprocess

OS_NAME = os.name
sys.path.append("../..")


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

from cdh_dav_python.cdc_admin_service import (
    environment_tracing as cdc_env_tracing,
    environment_logging as cdc_env_logging,
)

from cdh_dav_python.cdc_tech_environment_service import (
    environment_file as cdc_environment_file,
)


from cdh_dav_python.cdc_tech_environment_service import (
    environment_string as cdc_environment_string,
)


class SecretScope:
    """
    A class that provides methods to interact with secret scopes in Databricks.
    """

    @classmethod
    def list_secret_scopes(cls, dbutils):
        """
        Lists all the secret scopes in Databricks.

        Parameters:
        - dbutils: The dbutils object used to interact with Databricks.

        Returns:
        - secret_scopes: A list of secret scopes.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("list_secret_scopes"):
            try:
                running_local = (
                    "dbutils" in locals() or "dbutils" in globals()
                ) is not True

                if running_local is True or dbutils is None:
                    secret_scopes = cls.list_secret_scopes_with_cli()
                else:
                    secret_scopes = dbutils.secrets.listScopes()
                return secret_scopes

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def list_secrets(cls, scope_name: str, dbutils):
        """
        List secrets from a secret scope.

        Args:
            scope_name (str): The name of the secret scope.
            dbutils: The dbutils object for accessing secrets.

        Returns:
            list: A list of secrets from the specified secret scope.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("list_secrets"):
            try:
                running_local = (
                    "dbutils" in locals() or "dbutils" in globals()
                ) is not True

                if running_local is True or dbutils is None:
                    secrets = cls.list_secrets_with_cli(scope_name)
                else:
                    secrets = dbutils.secrets.list(scope=scope_name)()
                return secrets
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def list_secrets_with_cli(cls, scope_name: str):
        """
        Lists the secrets within a specified scope using the Databricks CLI.

        Args:
            scope_name (str): The name of the secret scope.

        Returns:
            list: A list of secrets within the specified scope, or None if an error occurred.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("list_secrets_with_cli"):
            try:
                command = ["databricks", "secrets", "list-secrets", scope_name]
                result = subprocess.run(
                    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                if result.returncode != 0:
                    s_error_message_1 = "Error in executing command:", result.stderr
                    scopes = cls.list_secret_scopes_with_cli()
                    s_error_message_2 = f"Available scopes: {scopes}"
                    error_message = f"{s_error_message_1}\n{s_error_message_2}"
                    raise Exception(error_message)
                json_data = result.stdout
                obj_string = cdc_environment_string.EnvironmentString()
                is_valid_json = obj_string.is_valid_json(json_data)
                if is_valid_json is False:
                    raise Exception("Invalid JSON data returned from command.")
                else:
                    secrets = json.loads(json_data)
                    return secrets

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def list_secret_scopes_with_cli():
        """
        Retrieves a list of secret scopes using the Databricks CLI.

        Returns:
            list: A list of secret scopes.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("list_secret_scopes_with_cli"):
            try:
                command = ["databricks", "secrets", "list-scopes"]
                result = subprocess.run(
                    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                if result.returncode != 0:
                    print("Error in executing command:", result.stderr)
                    return None
                json_data = SecretScope.parse_to_json(result.stdout)
                scopes = json.loads(json_data)
                return scopes

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def parse_to_json(data):
        """
        Parses the given data into a JSON string.

        Args:
            data (str): The data to be parsed.

        Returns:
            str: The JSON string representation of the parsed data.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("parse_to_json"):
            try:
                logger.info(f"data: {data}")
                lines = data.strip().split("\n")
                logger.info(f"lines: {lines}")
                headers = lines[0].split()
                logger.info(f"headers: {headers}")
                scopes = []

                for line in lines[1:]:
                    parts = line.split(maxsplit=1)
                    scope_dict = {
                        headers[0]: parts[0].strip(),
                        headers[1]: parts[1].strip(),
                    }
                    scopes.append(scope_dict)

                return json.dumps(scopes, indent=2)

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def generate_secret_markdown_table(secret_metadata_list):
        """
        Generate a markdown table from a list of secret metadata.

        Args:
            secret_metadata_list (list): A list of secret metadata.

        Returns:
            str: A markdown table representing the secret metadata.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("generate_secret_markdown_table"):
            try:
                # Start with the header
                markdown_table = "| Secret Key |\n| --- |\n"

                # Add each row
                for item in secret_metadata_list:
                    markdown_table += f"| {item.key} |\n"

                return markdown_table

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def generate_secret_scopes_markdown_table(scope_metadata_list):
        """
        Generate a markdown table from a list of secret scope metadata.

        Args:
            scope_metadata_list (list): A list of dictionaries containing secret scope metadata.
                Each dictionary should have 'Scope' and 'Backend' keys.

        Returns:
            str: A markdown table representing the secret scopes, with 'Scope' and 'Backend' columns.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("generate_secret_markdown_table"):
            try:
                # Start with the header
                markdown_table = "| Scope | Backend |\n| --- | --- |\n"

                # Add each row
                for item in scope_metadata_list:
                    markdown_table += f"| {item['Scope']} | {item['Backend']} |\n"

                return markdown_table

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
