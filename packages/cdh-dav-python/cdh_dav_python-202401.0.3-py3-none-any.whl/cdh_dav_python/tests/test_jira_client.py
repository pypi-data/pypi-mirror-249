from dotenv import load_dotenv
import os
import sys
import requests
from unittest import mock
import pytest

import cdh_dav_python.jira_service.jira_client as jira_client
import cdh_dav_python.cdc_metadata_service.environment_metadata as cdc_env_metadata

from cdh_dav_python.cdc_admin_service import (
    environment_logging as cdc_env_logging,
)

from pathlib import Path

sys.path.append("..")


NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


def get_config(parameters):
    environment_metadata = cdc_env_metadata.EnvironmentMetaData()

    config = environment_metadata.get_configuration_common(parameters, None)

    return config


def test_get_tasks():
    logger_singleton = cdc_env_logging.LoggerSingleton.instance(
        NAMESPACE_NAME, SERVICE_NAME
    )
    logger = logger_singleton.get_logger()

    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    logger.info(f"dotenv_path:{dotenv_path}")
    load_dotenv(dotenv_path)

    # Get the absolute path of the current script
    current_script_path = os.path.abspath(__file__)

    # Get the project root directory by going up one or more levels
    project_root = os.path.dirname(os.path.dirname(current_script_path))

    # Change the current working directory to the project root directory
    os.chdir(project_root)

    repository_path_default = str(Path(os.getcwd()))
    parameters = {
        "data_product_id": "wonder_metadata_dev",
        "data_product_id_root": "ocio",
        "data_product_id_individual": "CDH",
        "environment": "dev",
        "repository_path": repository_path_default,
    }

    config = get_config(parameters)

    jira_client_secret_key = config.get("jira_client_secret_key")
    az_kv_jira_env_var = jira_client_secret_key.replace("-", "_")
    logger.info(f"az_kv_jira_env_var:{az_kv_jira_env_var}")
    jira_client_secret = os.getenv(az_kv_jira_env_var)
    logger.info(f"jira_client_secret:{jira_client_secret}")
    if jira_client_secret is None:
        raise Exception(
            f"Unable to get Jira client secret from environment variable {az_kv_jira_env_var}"
        )

    # Set your default project value here
    jira_project = "DTEDS"

    jira_base_url = config.get("jira_base_url")

    jira_headers = {
        "Authorization": f"Bearer {jira_client_secret}",
        "Content-Type": "application/json",
    }
    logger.info(f"headers_length:{str(len(jira_headers))}")

    jira_client_instance = jira_client.JiraClient()
    jira_tasks = jira_client_instance.get_tasks(
        jira_project, jira_headers, jira_base_url
    )
    logger.info(jira_tasks)
    return "Success"
