import pathlib
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


import pytest
import cdh_dav_python.cdc_metadata_service.environment_metadata as cdc_env_metadata
import cdh_dav_python.databricks_service.notebook as cdc_dbx_notebook
import cdh_dav_python.cdc_tech_environment_service.environment_file as cdc_env_file

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


def get_config(parameters):
    """
    Retrieves the configuration based on the given parameters.

    Args:
        parameters (dict): A dictionary containing the parameters.

    Returns:
        dict: The configuration retrieved based on the parameters.
    """

    environment_metadata = cdc_env_metadata.EnvironmentMetaData()

    config = environment_metadata.get_configuration_common(parameters, None)

    return config


def test_run_notebook():
    """
    Test case for the run_notebook function.

    This function tests the functionality of the run_notebook function by calling it with mock variables
    and asserting that the response is equal to {"result": "success"}.

    Parameters:
    None

    Returns:
    None
    """

    repository_path_default = str(Path(os.getcwd()))

    parameters = {
        "data_product_id": "wonder_metadata_dev",
        "data_product_id_root": "wonder",
        "data_product_id_individual": "metadata",
        "environment": "dev",
        "running_local": True,
        "repository_path": repository_path_default,
    }

    config = get_config(parameters)

    # Mock variables
    token = "my_token"
    databricks_instance_id = config["databricks_instance_id"]
    cluster_id = "my_cluster_id"
    notebook_path = "my_notebook_path"
    parameters = {"param1": "value1", "param2": "value2"}

    # Call the function under test
    obj_notebook = cdc_dbx_notebook.Notebook(config)
    response = obj_notebook.run_notebook(
        token, databricks_instance_id, cluster_id, notebook_path, parameters
    )

    # Assert the response
    assert response == {"result": "success"}
