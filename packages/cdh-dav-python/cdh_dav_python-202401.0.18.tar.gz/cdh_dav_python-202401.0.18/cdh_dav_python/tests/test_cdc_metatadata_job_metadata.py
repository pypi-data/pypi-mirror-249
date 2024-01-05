import pytest
import sys
import os

sys.path.append("..")

import cdh_dav_python.cdc_metadata_service.job_metadata as cdc_job_metadata
import cdh_dav_python.cdc_metadata_service.environment_metadata as cdc_environment_metadata

from unittest.mock import MagicMock
from unittest.mock import patch
from pathlib import Path
from databricks.connect import DatabricksSession
from databricks.sdk.core import Config

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


ENVIRONMENT = "dev"

# Get the absolute path of the current script
current_script_path = os.path.abspath(__file__)

# Get the project root directory by going up one or more levels
project_root = os.path.dirname(os.path.dirname(current_script_path))

# Change the current working directory to the project root directory
os.chdir(project_root)

REPOSITORY_PATH_DEFAULT = str(Path(os.getcwd()))


def get_config(parameters):
    """
    Retrieves the configuration based on the given parameters.

    Args:
        parameters (dict): A dictionary containing the parameters.

    Returns:
        dict: The configuration retrieved based on the parameters.
    """
    obj_environment_metadata = cdc_environment_metadata.EnvironmentMetaData()
    config = obj_environment_metadata.get_configuration_common(parameters, None)
    return config


def test_run_analytics_processing():
    """
    Test case for the run_analytics_processing function.

    This test case creates mock objects and calls the run_analytics_processing function with the mock objects and
    other required parameters. It then asserts the result of the function call.

    Returns:
        None
    """
    # Create mock objects
    obj_env_metadata = cdc_environment_metadata.EnvironmentMetaData()

    REPOSITORY_PATH_DEFAULT = str(Path(os.getcwd()))

    parameters = {
        "data_product_id": "wonder_metadata",
        "data_product_id_root": "wonder",
        "data_product_id_individual": "metadata",
        "environment": "dev",
        "repository_path": REPOSITORY_PATH_DEFAULT,
    }

    config = get_config(parameters)

    # Set USER_ID for Spark
    user_name = os.environ.get("USER") or os.environ.get("USERNAME")
    os.environ["USER_ID"] = user_name
    dbx_config = Config(profile="WONDER_METADATA_DEV")
    spark = DatabricksSession.builder.sdkConfig(dbx_config).getOrCreate()
    dbutils = None
    export_schema = ""
    filter_column_name = ""
    filter_value = ""

    # Call the function under test
    obj_job_metadata = cdc_job_metadata.JobMetaData()

    result = obj_job_metadata.run_analytics_processing(
        obj_env_metadata,
        config,
        spark,
        dbutils,
        export_schema,
        filter_column_name,
        filter_value,
    )

    # Assert the result
    assert isinstance(result, str)
    # Add more specific assertions based on the expected behavior of the function

    # Add more test cases as needed


if __name__ == "__main__":
    pytest.main()
