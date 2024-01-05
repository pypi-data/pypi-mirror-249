""" Module for environment_metadata for the developer service with
metadata config file dependencies. """


# core
import sys  # don't remove required for error handling
import os
from pathlib import Path

# text
import json
from html.parser import HTMLParser  # web scraping html

import logging.config

# data
import logging
import uuid
from datetime import datetime

# Import from sibling directory ..\cdc_tech_environment_service
OS_NAME = os.name
sys.path.append("..")

if OS_NAME.lower() == "nt":
    print("environment_logging: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("environment_logging: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))

# cdh
from cdh_dav_python.cdc_security_service import (
    security_core as cdh_sec_core,
)

from cdh_dav_python.cdc_tech_environment_service import (
    environment_file as cdc_environment_file,
)


from cdh_dav_python.az_storage_service import (
    az_storage_file as az_file,
)


from cdh_dav_python.cdc_metadata_service import (
    logging_metadata as cdh_log_metadata,
)

from cdh_dav_python.cdc_admin_service import (
    environment_tracing as cdc_env_tracing,
    environment_logging as cdc_env_logging,
)

from dotenv import load_dotenv, find_dotenv, set_key

# spark
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, concat_ws, lit, udf, trim
from pyspark.sql.types import StringType, StructType

# http
import requests

# Import from sibling directory ..\databricks_service
OS_NAME = os.name

uuid_udf = udf(lambda: str(uuid.uuid4()), StringType())

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class EnvironmentMetaData:
    """This is a conceptual class representation of an Environment
    It is a static class libary
    Todo
    Note which variables require manual updates from the centers and which
    can be prepopulated
    Note which variables are EDAV or Peraton specific
    Separate out config.devops.dev, config.cdh.dev and config.core.dev
    """

    @classmethod
    def check_configuration_files(cls, config: dict, dbutils: object) -> dict:
        """Takes in config dictionary and dbutils objects, returns populated
            check_files dictionary with check results

        Args:
            config (dict): global config dictionary
            dbutils (object): databricks dbutils object

        Returns:
            dict: check_files dictionary with results of file configuration
                    checks
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()

        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("check_configuration_files"):
            try:
                running_local = config["running_local"]
                # confirm ingress_folder
                ingress_folder = config["cdh_folder_ingress"]
                ingress_folder_files_exists = str(
                    cls.file_exists(running_local, ingress_folder, dbutils)
                )

                # confirm cdh_folder_config
                cdh_folder_config = config["cdh_folder_config"]
                cdh_folder_config_files_exists = str(
                    cls.file_exists(running_local, cdh_folder_config, dbutils)
                )

                # confirm database path
                cdh_folder_database = config.get("cdh_folder_database")
                files_exists = cls.file_exists(
                    running_local, cdh_folder_database, dbutils
                )
                cdh_folder_database_files_exists = str(files_exists)

                s_text = f"ingress_folder_files_exists exists test result:\
                    {ingress_folder_files_exists}"
                s_text_1 = f"cdh_folder_database_files_exists exists test result:\
                    {cdh_folder_database_files_exists}"
                s_text_2 = f"{config.get('cdh_database_name')} at cdh_folder_database:\
                    {cdh_folder_database}"
                ingress_folder_files_exists_test = s_text
                cdh_folder_config_files_exists_test = f"cdh_folder_config_files_exists exists\
                    test result: {cdh_folder_config_files_exists}"
                check_files = {
                    "cdh_folder_ingress": f"{ingress_folder}",
                    "ingress_folder_files_exists_test": ingress_folder_files_exists_test,
                    "cdh_folder_config": f"{cdh_folder_config}",
                    "cdh_folder_config_files_exists_test": cdh_folder_config_files_exists_test,
                    "cdh_folder_database": f"{cdh_folder_database}",
                    "cdh_folder_database_files_exists test": s_text_1,
                    "creating new cdh_database_name": s_text_2,
                }

                return check_files

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def get_job_list(
        cls, job_name: str, config: dict, spark: SparkSession
    ) -> DataFrame:
        """Get list of jobs actions for a selected job

        Args:
            job_name (str): Selected Job name
            config (dict): Configuration dictionary
            spark (SparkSession): Spark object

        Returns:
            DataFrame: Dataframe with list of job actions
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()

        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_job_list"):
            try:
                obj_env_log = cdh_log_metadata.LoggingMetaData()

                ingress_folder_sps = config["ingress_folder_sps"]
                ingress_folder_sps = ingress_folder_sps.rstrip("/")
                config_jobs_path = f"{ingress_folder_sps}/bronze_sps_config_jobs.csv"

                data_product_id = config["data_product_id"]
                info_msg = f"config_jobs_path:{config_jobs_path}"
                obj_env_log.log_info(config, info_msg)

                first_row_is_header = "true"
                delimiter = ","
                df_jobs = (
                    spark.read.format("csv")
                    .option("header", first_row_is_header)
                    .option("sep", delimiter)
                    .option("multiline", True)
                    .option("inferSchema", True)
                    .load(config_jobs_path, forceLowercaseNames=True, inferLong=True)
                )
                df_jobs = df_jobs.withColumn("job_name", trim("job"))
                df_jobs = df_jobs.filter(df_jobs.job_name == job_name)
                df_jobs.show(truncate=False)

                return df_jobs

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def get_column_list(
        cls, config: dict, spark: SparkSession, dbutils: object
    ) -> DataFrame:
        """Takes in dataset config dictionary, spark object, dbutils object\
        and returns dataframe
        with list of columns for dataset

        Args:
            config (dict): dataset config dictionary
            spark (SparkSession): spark session
            dbutils (object): databricks dbutils object

        Returns:
            DataFrame: dataframe popluated with list of columns for dataset
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()

        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_column_list"):
            try:
                first_row_is_header = "true"
                delimiter = ","

                dataset_name = config["dataset_name"]
                running_local = config["running_local"]
                ingress_folder_sps = config["ingress_folder_sps"]
                data_product_id = config["data_product_id"]
                ingesttimestamp = datetime.now()

                file_path = f"{ingress_folder_sps}bronze_sps_config_columns.csv"
                # check if size of file is 0
                client_id = config["az_sub_client_id"]
                tenant_id = config["az_sub_tenant_id"]
                client_secret = config["client_secret"]
                file_size = cls.get_file_size(
                    running_local,
                    file_path,
                    dbutils,
                    spark,
                    client_id,
                    client_secret,
                    tenant_id,
                )

                logger.info(f"file_size: {str(file_size)}")

                # default to empty DataFrame
                df_results = spark.createDataFrame([], StructType([]))

                if file_size > 0:
                    df_results = (
                        spark.read.format("csv")
                        .option("header", first_row_is_header)
                        .option("sep", delimiter)
                        .option("inferSchema", True)
                        .option("inferLong", True)
                        .option("multiline", True)
                        .option("inferDecimal", True)
                        .option("inferInteger", True)
                        .option("forceLowercaseNames", True)
                        .load(file_path)
                        .withColumn("meta_ingesttimestamp", lit(ingesttimestamp))
                        .withColumn(
                            "row_id",
                            concat_ws(
                                "-",
                                col("data_product_id"),
                                col("dataset_name"),
                                col("column_name"),
                            ),
                        )
                    )

                    # bronze_sps_config_columns_df.select(col("column_batch_group").cast("int").as("column_batch_group"))
                    if df_results.count() == 0:
                        logger.info("File hase 0 rows")
                    else:
                        if dataset_name == "sps":
                            project_filter = f"(data_product_id == '{data_product_id}')"
                            df_results = df_results.filter(project_filter)
                else:
                    logger.error(
                        f"{ingress_folder_sps}bronze_sps_config_columns.csv file_size indicates is empty"
                    )

                return df_results

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_file_size(
        running_local: bool,
        file_path: str,
        dbutils,
        spark,
        client_id: str = None,
        client_secret: str = None,
        tenant_id: str = None,
    ) -> int:
        """Gets the file size in bytes for the specified file path.

        Args:
            running_local (bool): Indicates whether the code is running locally or in a distributed environment.
            file_path (str): The path of the file for which to retrieve the size.
            dbutils: The dbutils object for interacting with Databricks utilities.
            spark: The SparkSession object for running Spark jobs.
            client_id (str, optional): The client ID for authentication (if applicable). Defaults to None.
            client_secret (str, optional): The client secret for authentication (if applicable). Defaults to None.
            tenant_id (str, optional): The tenant ID for authentication (if applicable). Defaults to None.

        Returns:
            int: The size of the file in bytes.
        """

        obj_env_file = cdc_environment_file.EnvironmentFile()
        file_size = obj_env_file.get_file_size(
            running_local,
            file_path,
            dbutils,
            spark,
            client_id,
            client_secret,
            tenant_id,
        )
        return file_size

    @staticmethod
    def file_exists(running_local: bool, path: str, dbutils) -> bool:
        """Takes in path, dbutils object, returns whether file exists at provided path

        Args:
            running_local: bool
            path (str): path to file
            dbutils (object): databricks dbutils

        Returns:
            bool: True/False indication if file exists
        """

        obj_env_file = az_file.AzStorageFile()
        file_exists = obj_env_file.file_exists(running_local, path, dbutils)
        return file_exists

    @staticmethod
    def convert_to_windows_dir(path: str) -> str:
        """Takes in path and returns path with backslashes converted to forward slashes

        Args:
            path (str): path to be converted

        Returns:
            str: converted path
        """
        obj_env_file = cdc_environment_file.EnvironmentFile()
        converted_path = obj_env_file.convert_to_windows_dir(path)
        return converted_path

    @staticmethod
    def convert_to_current_os_dir(path: str) -> str:
        """Takes in path and returns path with backslashes converted to forward slashes

        Args:
            path (str): path to be converted

        Returns:
            str: converted path
        """
        obj_env_file = cdc_environment_file.EnvironmentFile()
        converted_path = obj_env_file.convert_to_current_os_dir(path)
        return converted_path

    @staticmethod
    def load_environment(
        running_local: bool,
        sp_tenant_id: str,
        subscription_id: str,
        sp_client_id: str,
        environment: str,
        data_product_id: str,
        dbutils,
        application_insights_connection_string: str,
        az_sub_oauth_token_endpoint: str,
    ):
        """
        Loads the environment file to configure the environment for the application.

        Args:
            running_local (bool): A flag indicating whether the application is running locally or deployed.
            sp_tenant_id (str): The Azure Active Directory tenant (directory) ID.
            subscription_id (str): The ID of the Azure subscription.
            sp_client_id (str): The Azure service principal's client (application) ID.
            environment (str): The deployment environment (e.g., 'dev', 'test', 'prod').
            data_product_id (str): The project ID to which the application belongs.
            dbutils: Databricks utilities object, which provides access to the Databricks filesystem and secrets, etc.
            application_insights_connection_string (str): The connection string for Azure Application Insights for application monitoring.
        """

        logger = logging.getLogger(data_product_id)
        logger.setLevel(logging.DEBUG)

        path = sys.executable + "\\.."
        sys.path.append(os.path.dirname(os.path.abspath(path)))
        env_path = os.path.dirname(os.path.abspath(path))

        if dbutils is None:
            running_local = True
        if running_local is True:
            logger.info(f"running_local: {running_local}")
            if OS_NAME.lower() == "nt":
                logger.info("windows")
                env_share_path = env_path + "\\share"
                folder_exists = os.path.exists(env_share_path)
                if not folder_exists:
                    # Create a new directory because it does not exist
                    os.makedirs(env_share_path)
                env_share_path_2 = sys.executable + "\\..\\share"
                sys.path.append(os.path.dirname(os.path.abspath(env_share_path_2)))
                env_file_path = env_share_path + "\\.env"
                logger.info(f"env_file_path: {env_file_path}")
                # don't delete line below - it creates the file
            else:
                logger.info("non windows")
                # env_share_path = env_path + "/share"
                env_share_path = os.path.expanduser("~") + "/share"
                folder_exists = os.path.exists(env_share_path)
                if not folder_exists:
                    # Create a new directory because it does not exist
                    os.makedirs(env_share_path)
                env_share_path_2 = sys.executable + "/../share"
                sys.path.append(os.path.dirname(os.path.abspath(env_share_path_2)))
                env_file_path = env_share_path + "/.env"
                logger.info(f"env_file_path: {env_file_path}")
                # don't delete line below - it creates the file

            open(env_file_path, "w+", encoding="utf-8")
            dotenv_file = find_dotenv(env_file_path)
            logger.info(f"dotenv_file: {dotenv_file}")
            set_key(dotenv_file, "AZURE_TENANT_ID", sp_tenant_id)
            set_key(dotenv_file, "AZURE_SUBSCRIPTION_ID", subscription_id)
            set_key(dotenv_file, "az_sub_client_id", sp_client_id)
        else:
            logger.info(f"running_local: {running_local}")
            env_share_path = os.path.expanduser("~") + "/share"
            folder_exists = os.path.exists(env_share_path)
            if not folder_exists:
                # Create a new directory because it does not exist
                os.makedirs(env_share_path)
            env_share_path_2 = sys.executable + "/../share"
            sys.path.append(os.path.dirname(os.path.abspath(env_share_path_2)))
            env_file_path = env_share_path + "/.env"
            env_file = open(env_file_path, "w+", encoding="utf-8")
            logger.info(f"env_file_path: {env_file_path}")
            dotenv_file = find_dotenv(env_file_path)

            # env_file_path = f"/mnt/{environment}/{data_product_id}"
            # print(f"env_file_path: {env_file_path}")
            # env_file_path = env_file_path + "/config/config_{environment}.txt"
            # dbutils.fs.put(
            #     env_file_path,
            #     f"""AZURE_TENANT_ID {sp_tenant_id}
        # AZURE_SUBSCRIPTION_ID {subscription_id}
        # az_sub_client_id {sp_client_id}
        #  """,
        #     True,
        # )

        # Define the desired connection string
        # DEV
        environment = environment.strip().lower()
        if environment == "dev":
            default_connection_string = "InstrumentationKey=8f02ef9a-cd94-48cf-895a-367f102e8a24;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/"
        # PROD
        else:
            default_connection_string = "InstrumentationKey=d091b27b-14e0-437f-ae3c-90f3f04ef3dc;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/"

        message = f"default_connection_string: {default_connection_string}"
        logger.info(message)
        print(message)

        # Check if the variable is blank (not set or empty)
        if not application_insights_connection_string:
            application_insights_connection_string = default_connection_string

        message = f"application_insights_connection_string: {application_insights_connection_string}"
        logger.info(message)
        print(message)

        set_key(
            dotenv_file,
            "APPLICATIONINSIGHTS_CONNECTION_STRING",
            application_insights_connection_string,
        )

        set_key(dotenv_file, "AZURE_AUTHORITY_HOST ", az_sub_oauth_token_endpoint)
        set_key(dotenv_file, "PYARROW_IGNORE_TIMEZONE", "1")

        message = f"dotenv_file: {dotenv_file}"
        logger.info(message)
        print(message)

        load_dotenv(dotenv_file)

        return env_file_path

    @classmethod
    def get_configuration_common(cls, parameters: dict, dbutils) -> dict:
        """Takes in parameters dictionary and returns config dictionary

        Args:
            parameters (dict): global parameters dictionary

        Returns:
            dict: update global configuration dictionary
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_configuration_common"):
            try:
                logger.info(f"parameters: {parameters}")
                parameters.setdefault("running_local", False)
                parameters.setdefault("dataset_name", "na")
                parameters.setdefault("cicd_action", "na")

                if isinstance(parameters["running_local"], (bool)) is False:
                    running_local = parameters["running_local"].lower() in [
                        "true",
                        "1",
                        "t",
                        "y",
                        "yes",
                    ]
                else:
                    running_local = parameters["running_local"]

                if dbutils is None:
                    running_local = True

                data_product_id = parameters["data_product_id"]
                logger.info(f"running_local: {running_local}")
                environment = parameters["environment"]
                data_product_id_root = parameters["data_product_id_root"]
                # Get the current year
                current_year = str(datetime.now().year)
                # Retrieve the parameter 'yyyy', and if it's not present, default to the current year
                yyyy_param = parameters.get("yyyy", current_year)
                # Get the current month
                current_month = datetime.now().strftime("%m")
                # Retrieve the parameter 'mm', and if it's not present, default to the current month
                mm_param = parameters.get("mm", current_month)
                # Get the current day
                current_day = datetime.now().strftime("%d")
                # Retrieve the parameter 'dd', and if it's not present, default to the current day
                dd_param = parameters.get("dd", current_day)

                dataset_name = parameters["dataset_name"]
                cicd_action = parameters["cicd_action"]
                repository_path = parameters["repository_path"]

                # create logger
                logger = logging.getLogger(data_product_id)
                logger.setLevel(logging.DEBUG)

                config_string = "config"
                cicd_action_string = "cicd"

                logger.info(f"repository_path:{repository_path}")
                repository_path = cls.convert_to_current_os_dir(repository_path)

                obj_repository_path = Path(repository_path)

                # Convert the path to a string and check if it contains 'cdh_dav_python'
                if "cdh_dav_python" in str(repository_path):
                    logger.info(
                        f"repository_path contains cdh_dav_python - extract up until token:{repository_path}"
                    )
                    # Split the path into parts
                    path_parts = obj_repository_path.parts

                    # Find the index of 'cdh_dav_python' in the path
                    cdh_dav_python_index = path_parts.index("cdh_dav_python")

                    # Extract the path up to and including 'cdh_dav_python'
                    repository_path = str(Path(*path_parts[: cdh_dav_python_index + 1]))

                    logger.info(f"extracted repository_path:{repository_path}")
                else:
                    logger.info("The path does not contain 'cdh_dav_python'")

                logger.info(f"data_product_id_root:{data_product_id_root}")
                logger.info(f"data_product_id:{data_product_id}")
                env_folder_path = f"{repository_path.rstrip('/')}/{data_product_id_root}/{data_product_id}/"
                logger.info(f"env_folder_path:{env_folder_path}")
                env_folder_path = cls.convert_to_current_os_dir(env_folder_path)
                if os.path.exists(env_folder_path) and os.path.isdir(env_folder_path):
                    logger.info(
                        f"The env_folder_path directory {env_folder_path} exists."
                    )
                else:
                    logger.info(
                        f"The env_folder_path directory {env_folder_path} does not exist."
                    )
                    two_levels_up = (
                        os.path.dirname(os.path.dirname(env_folder_path)) + "/"
                    )
                    two_levels_up = cls.convert_to_current_os_dir(two_levels_up)
                    env_folder_path = two_levels_up
                    if os.path.exists(env_folder_path) and os.path.isdir(
                        env_folder_path
                    ):
                        logger.info(
                            f"The env_folder_path directory {env_folder_path} exists."
                        )
                    else:
                        raise ValueError(
                            f"The env_folder_path directory {env_folder_path} does not exist."
                        )

                cdh_folder_config_path = f"{env_folder_path}{config_string}/"
                logger.info(f"cdh_folder_config_path:{cdh_folder_config_path}")
                cdh_folder_config_path = cls.convert_to_current_os_dir(
                    cdh_folder_config_path
                )
                environment_json_path = (
                    f"{cdh_folder_config_path}{config_string}.{environment}.json"
                )
                environment_json_path_default = (
                    f"{cdh_folder_config_path}{config_string}.{environment}.json"
                )

                # Check if environment_json_path exists
                environment_json_path = cls.convert_to_current_os_dir(
                    environment_json_path
                )
                logger.info(f"environment_json_path check 1: {environment_json_path}")
                if not cls.file_exists(running_local, environment_json_path, None):
                    logger.info(f"config does not exist: {environment_json_path}")
                    repository_path_temp = os.getcwd()
                    repository_path_temp = str(Path(repository_path_temp))
                    repository_path_temp = f"{repository_path_temp}{data_product_id_root}/{data_product_id}/{config_string}/"
                    repository_path_temp = cls.convert_to_current_os_dir(
                        repository_path_temp
                    )
                    environment_json_path = (
                        f"{repository_path_temp}{config_string}.{environment}.json"
                    )
                    logger.info(
                        f"environment_json_path check 2: {environment_json_path}"
                    )
                    if not cls.file_exists(running_local, environment_json_path, None):
                        logger.info(f"config does not exist: {environment_json_path}")
                        repository_path_temp = os.getcwd()
                        repository_path_temp = str(Path(repository_path_temp).parent)
                        repository_path_temp = f"{repository_path_temp}{data_product_id_root}/{data_product_id}/{config_string}/"
                        repository_path_temp = cls.convert_to_current_os_dir(
                            repository_path_temp
                        )
                        environment_json_path = (
                            f"{repository_path_temp}{config_string}.{environment}.json"
                        )
                        logger.info(
                            f"environment_json_path check 3: {environment_json_path}"
                        )
                        if not cls.file_exists(
                            running_local, environment_json_path, None
                        ):
                            logger.info(
                                f"config does not exist: {environment_json_path}"
                            )
                            # Try two levels up from the current folder
                            repository_path_temp = os.getcwd()
                            repository_path_temp = str(
                                Path(repository_path_temp).parent.parent
                            )
                            repository_path_temp = f"{repository_path_temp}{data_product_id_root}/{data_product_id}/{config_string}/"
                            repository_path_temp = cls.convert_to_current_os_dir(
                                repository_path_temp
                            )
                            environment_json_path = f"{repository_path_temp}{config_string}.{environment}.json"
                            logger.info(
                                f"environment_json_path check 4: {environment_json_path}"
                            )
                            if not cls.file_exists(
                                running_local, environment_json_path, None
                            ):
                                logger.info(
                                    f"config does not exist: {environment_json_path}"
                                )
                                repository_path_temp = os.getcwd()
                                repository_path_temp = str(
                                    Path(repository_path_temp).parent.parent.parent
                                )
                                repository_path_temp = cls.convert_to_current_os_dir(
                                    repository_path_temp
                                )
                                repository_path_temp = f"{repository_path_temp}{data_product_id_root}/{data_product_id}/{config_string}/"
                                repository_path_temp = cls.convert_to_current_os_dir(
                                    repository_path_temp
                                )
                                environment_json_path = f"{repository_path_temp}{config_string}.{environment}.json"
                                logger.info(
                                    f"environment_json_path check 5: {environment_json_path}"
                                )

                                if not cls.file_exists(
                                    running_local, environment_json_path, None
                                ):
                                    logger.info(
                                        f"config does not exist: {environment_json_path}"
                                    )
                                    environment_json_path = (
                                        environment_json_path_default
                                    )
                                else:
                                    logger.info(
                                        f"config exists: {environment_json_path}"
                                    )
                            else:
                                logger.info(f"config exists: {environment_json_path}")
                else:
                    logger.info(f"config exists: {environment_json_path}")

                cicd_folder = f"{repository_path}{data_product_id_root}/{data_product_id}/{cicd_action_string}/"
                cicd_folder = cls.convert_to_current_os_dir(cicd_folder)
                cicd_action_path = (
                    f"{cicd_folder}" + f"{cicd_action}" + f".{environment}.json"
                )

                logger.info("---- WORKING REPOSITORY FILE REFERENCE -------")
                logger.info(f"environment_json_path: {environment_json_path}")
                logger.info(data_product_id)
                logger.info("----------------------------------------------")

                # Assuming `parameters` and `environment_json_path` are defined somewhere above this code.

                with open(
                    environment_json_path, mode="r", encoding="utf-8"
                ) as json_file:
                    config = json.load(json_file)

                config["running_local"] = running_local
                config["yyyy"] = yyyy_param
                config["mm"] = mm_param
                config["dd"] = dd_param
                config["dataset_name"] = dataset_name
                config["dataset_type"] = "TABLE"
                config["repository_path"] = repository_path
                config["environment_json_path"] = environment_json_path
                config["cicd_action_path"] = cicd_action_path
                config["ingress_folder_sps"] = "".join(
                    [config["cdh_folder_config"], "cdh/"]
                )
                config["data_product_id"] = config["cdh_data_product_id"]
                config["data_product_id_root"] = config["cdh_data_product_id_root"]
                config["data_product_id_individual"] = config[
                    "cdh_data_product_id_individual"
                ]
                data_product_id_individual = config["data_product_id_individual"]
                config["databricks_instance_id"] = config.get(
                    "cdh_databricks_instance_id"
                )
                config["environment"] = config["cdh_environment"]
                config["override_save_flag"] = "override_with_save"
                config["is_using_dataset_folder_path_override"] = False
                config["is_using_standard_column_names"] = "force_lowercase"
                config["is_export_schema_required_override"] = True
                config[
                    "ingress_mount"
                ] = f"/mnt/{environment}/{data_product_id_individual}/ingress"
                if config["az_sub_client_secret_key"] is None:
                    config["az_sub_client_secret_key"] = str(az_sub_client_secret_key)
                data_product_id = config["data_product_id"]
                cdh_folder_database = config.get("cdh_folder_database")
                if not cdh_folder_database:
                    schema_dataset_file_path = ""
                else:
                    schema_dataset_file_path = (
                        cdh_folder_database.rstrip("/") + "/bronze_clc_schema"
                    )
                config["schema_dataset_file_path"] = schema_dataset_file_path

                if config:
                    print(
                        f"Configuration found environment_json_path: {environment_json_path}"
                    )
                else:
                    error_message = "Error: no configurations were found."
                    error_message = (
                        error_message
                        + f"Check your settings file: {environment_json_path}."
                    )
                    print(error_message)

                scope = config.get("cdh_databricks_kv_scope")
                kv_client_id_key = config.get("cdh_oauth_sp_kv_client_secret_key")
                kv_client_secret_key = config.get("cdh_oauth_sp_kv_client_secret_key")
                if kv_client_id_key is not None:
                    if kv_client_id_key.strip() == "":
                        kv_client_id_key = None

                if kv_client_secret_key is not None:
                    if kv_client_secret_key.strip() == "":
                        kv_client_secret_key = None

                sp_redirect_url = config.get("cdh_oauth_sp_redirect_url")
                az_sub_oauth_token_endpoint = config.get("az_sub_oauth_token_endpoint")
                sp_tenant_id = config["az_sub_tenant_id"]
                subscription_id = config["az_sub_subscription_id"]
                sp_client_id = config["az_sub_client_id"]
                sp_azure_databricks_resource_id = config.get(
                    "cdh_oauth_databricks_resource_id"
                )

                az_apin_ingestion_endpoint = config.get("az_apin_ingestion_endpoint")
                az_apin_instrumentation_key = config.get("az_apin_instrumentation_key")
                application_insights_connection_string = f"InstrumentationKey={az_apin_instrumentation_key};IngestionEndpoint={az_apin_ingestion_endpoint}"
                az_sub_oauth_token_endpoint = config.get("az_sub_oauth_token_endpoint")

                # Write changes to .env file - create .env file if it does not exist
                env_file_path = cls.load_environment(
                    running_local,
                    sp_tenant_id,
                    subscription_id,
                    sp_client_id,
                    environment,
                    data_product_id,
                    dbutils,
                    application_insights_connection_string,
                    az_sub_oauth_token_endpoint,
                )

                config["env_file_path"] = env_file_path
                az_sub_client_secret_key = config["az_sub_client_secret_key"]
                if running_local is True:
                    logger.info(f"az_sub_client_secret_key:{az_sub_client_secret_key}")
                    sp_client_secret = os.getenv(az_sub_client_secret_key)
                else:
                    message = (
                        f"Retrieving Databricks secret for {az_sub_client_secret_key}."
                    )
                    logger.info(message)
                    logger.info(message)
                    sp_client_secret = dbutils.secrets.get(
                        scope=scope, key=az_sub_client_secret_key
                    )

                config["az_sub_client_id"] = sp_client_id
                config["client_secret"] = sp_client_secret
                config["tenant_id"] = sp_tenant_id

                sp_authority_host_url = "https://login.microsoftonline.com"

                if sp_client_secret is None:
                    config["error_message"] = "azure_client_secret_value_not_set_error"
                else:
                    obj_security_core = cdh_sec_core.SecurityCore()

                    config_user = (
                        obj_security_core.acquire_access_token_with_client_credentials(
                            sp_client_id,
                            sp_client_secret,
                            sp_tenant_id,
                            sp_redirect_url,
                            sp_authority_host_url,
                            sp_azure_databricks_resource_id,
                            data_product_id,
                        )
                    )
                    config["redirect_uri"] = config_user["redirect_uri"]
                    config["authority_host_url"] = config_user["authority_host_url"]
                    config["azure_databricks_resource_id"] = config_user[
                        "azure_databricks_resource_id"
                    ]
                    config["az_sub_oauth_token_endpoint"] = config_user[
                        "az_sub_oauth_token_endpoint"
                    ]
                    config["access_token"] = config_user["access_token"]

                return config

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_dataset_list(config: dict, spark: SparkSession) -> DataFrame:
        """Takes in config dictionary, spark object, returns list of datasets in project

        Args:
            config (dict): global config dictionary
            spark (SparkSession): spark session

        Returns:
            DataFrame: dataframe with list of datasets in project
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_configuration_common"):
            try:
                obj_env_log = cdh_log_metadata.LoggingMetaData()

                first_row_is_header = "true"
                delimiter = ","

                csv_file_path = config["ingress_folder_sps"]
                csv_file_path = csv_file_path + "\\"
                csv_file_path = csv_file_path + "bronze_sps_config_datasets.csv"
                data_product_id = config["data_product_id"]
                ingesttimestamp = datetime.now()

                df_results = (
                    spark.read.format("csv")
                    .option("header", first_row_is_header)
                    .option("sep", delimiter)
                    .option("multiline", True)
                    .option("inferSchema", True)
                    .load(csv_file_path, forceLowercaseNames=True, inferLong=True)
                    .withColumn("meta_ingesttimestamp", lit(ingesttimestamp))
                    .withColumn(
                        "row_id",
                        concat_ws("-", col("data_product_id"), col("dataset_name")),
                    )
                )

                # sort
                if df_results.count() > 0:
                    # df_results.show()
                    df_results = df_results.sort("pipeline_batch_group")
                else:
                    err_message = (
                        f"No datasets found for data_product_id:{data_product_id}"
                    )
                    obj_env_log.log_error(data_product_id, err_message)
                    print(err_message)

                return df_results

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_pipeline_list(config: dict, spark: SparkSession) -> DataFrame:
        """Takes in config dictionary, spark session object, returns dataframe with list of pipelines in project

        Args:
            config (dict): global config dictionary
            spark (SparkSession): spark session

        Returns:
            DataFrame: dataframe with list of pipelines in project
        """

        first_row_is_header = "true"
        delimiter = ","

        ingress_folder_sps = config["ingress_folder_sps"]
        ingesttimestamp = datetime.now()
        data_product_id = config["data_product_id"]

        bronze_sps_config_pipelines_df = (
            spark.read.format("csv")
            .option("header", first_row_is_header)
            .option("sep", delimiter)
            .option("multiline", True)
            .option("inferSchema", True)
            .load(
                f"{ingress_folder_sps}bronze_sps_config_pipelines.csv",
                forceLowercaseNames=True,
                inferLong=True,
            )
            .withColumn("meta_ingesttimestamp", lit(ingesttimestamp))
            .withColumn(
                "row_id",
                concat_ws("-", col("data_product_id"), col("view_name")),
            )
        )

        bronze_sps_config_pipelines_df = bronze_sps_config_pipelines_df.filter(
            "data_product_id == '" + data_product_id + "' "
        )

        # sort by load group to ensure dependencies are run in order
        bronze_sps_config_pipelines_df = bronze_sps_config_pipelines_df.sort(
            "pipeline_batch_group"
        )

        return bronze_sps_config_pipelines_df

    @classmethod
    def list_files(cls, config: dict, token: str, base_path: str) -> list:
        """Takes in a config dictionary, token and base_path, returns
        populated list of files

        Args:
            config (dict): global config dictionary
            token (str): token
            base_path (str): path to list files

        Returns:
            list: list of files at the path location
        """

        obj_env_log = cdh_log_metadata.LoggingMetaData()

        databricks_instance_id = config["databricks_instance_id"]
        json_text = {"path": base_path}
        headers = {"Authentication": f"Bearer {token}"}
        url = f"https://{databricks_instance_id}/api/2.0/workspace/list"
        data_product_id = config["data_product_id"]
        obj_env_log.log_info(config, f"------- Fetch {base_path}  -------")
        obj_env_log.log_info(config, f"url:{str(url)}")
        headers_redacted = str(headers).replace(token, "[bearer REDACTED]")
        obj_env_log.log_info(config, f"headers:{headers_redacted}")

        response = requests.get(url=url, headers=headers, json=json_text, timeout=120)
        data = None
        results = []

        try:
            response_text = str(response.text)
            data = json.loads(response_text)
            msg = f"Received list_files with length : {len(str(response_text))} when posting to : "
            msg = msg + f"{url} to list files for : {base_path}"
            response_text_fetch = msg
            print("- response : success  -")
            print(f"{response_text_fetch}")
            lst = data["objects"]

            for i in lst:
                if i["object_type"] == "DIRECTORY" or i["object_type"] == "REPO":
                    path = i["path"]
                    results.extend(cls.list_files(config, token, path))
                else:
                    path = i["path"]
                    results.append(path)
        except Exception as exception_object:
            f_filter = HTMLFilter()
            f_filter.feed(response.text)
            response_text = f_filter.text
            print(f"- response : error - {exception_object}")
            print(f"Error converting response text:{response_text} to json")

        return results

    @staticmethod
    def setup_spark_configuration(spark: SparkSession, config: dict) -> SparkSession:
        """Takes spark session, global config dictionary
        and return configured Spark session

        Args:
            spark (SparkSession): spark session
            config (dict): global config dictionary

        Returns:
            SparkSession: configured spark session
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("setup_spark_configuration"):
            try:
                c_ep = config["az_sub_oauth_token_endpoint"]
                c_id = config["az_sub_client_id"]
                c_secret = config["client_secret"]
                sp_tenant_id = config["az_sub_tenant_id"]
                running_local = config["running_local"]

                client_secret_exists = True
                if c_id is None or c_secret is None:
                    client_secret_exists = False
                storage_account = config["cdh_azure_storage_account"]

                client_token_provider = (
                    "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider"
                )
                provider_type = "OAuth"

                # stack overflow example
                fs_prefix_e1 = "fs.azure.account.auth."
                fso_prefix_e1 = "fs.azure.account.oauth"
                fso2_prefix_e1 = "fs.azure.account.oauth2"
                fso3_prefix_e1 = "fs.azure.account.oauth2.client.secret"  # spark.hadoop
                fs_suffix_e1 = f".{storage_account}.dfs.core.windows.net"
                fso3_prefix_e1 = fso3_prefix_e1 + fs_suffix_e1

                if client_secret_exists is None:
                    client_secret_exists = False

                logger.info(f"client_secret_exists:{str(client_secret_exists)}")
                logger.info(f"endpoint:{str(c_ep)}")

                # config["run_as"] = "service_principal"
                config["run_as"] = "remote_user"
                run_as = config["run_as"]
                logger.info(f"running databricks access using run_as:{run_as}")

                if (
                    client_secret_exists is True
                    and run_as == "service_principal"
                    and running_local is True
                ):
                    spark.conf.set(f"{fs_prefix_e1}type{fs_suffix_e1}", provider_type)
                    spark.conf.set(
                        f"{fso_prefix_e1}.provider.type{fs_suffix_e1}",
                        client_token_provider,
                    )
                    spark.conf.set(f"{fso2_prefix_e1}.client.id{fs_suffix_e1}", c_id)
                    spark.conf.set(
                        f"{fso2_prefix_e1}.client.secret{fs_suffix_e1}", c_secret
                    )
                    client_endpoint_e1 = (
                        f"https://login.microsoftonline.com/{sp_tenant_id}/oauth2/token"
                    )
                    spark.conf.set(
                        f"{fso2_prefix_e1}.client.endpoint{fs_suffix_e1}",
                        client_endpoint_e1,
                    )

                    logger.log_info(
                        config,
                        f'spark.conf.set "({fs_prefix_e1}type{fs_suffix_e1}", "{provider_type}")',
                    )
                    logger.log_info(
                        config,
                        f'spark.conf.set "({fso_prefix_e1}.provider.type{fs_suffix_e1}", \
                        "{client_token_provider}")',
                    )
                    logger.log_info(
                        config,
                        f'spark.conf.set "({fso2_prefix_e1}.client.id{fs_suffix_e1}", "{c_id}")',
                    )
                    logger.log_info(
                        config,
                        f'spark.conf.set "{fso2_prefix_e1}.client.endpoint{fs_suffix_e1}" \
                        = "{client_endpoint_e1}"',
                    )

                spark.conf.set("spark.databricks.io.cache.enabled", "true")
                # Enable Arrow-based columnar data transfers
                spark.conf.set("spark.sql.execution.arrow.enabled", "true")
                # sometimes azure storage has a delta table not found bug - in that scenario try filemount above
                spark.conf.set("spark.sql.execution.arrow.fallback.enabled", "true")
                spark.conf.set("spark.databricks.pyspark.enablePy4JSecurity", "false")
                # Enable Delta Preview
                spark.conf.set("spark.databricks.delta.preview.enabled ", "true")

                if running_local is False:
                    os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"
                    spark.sql(
                        "SET spark.databricks.delta.schema.autoMerge.enabled = true"
                    )
                    cdh_folder_checkpoint = config["cdh_folder_checkpoint"]
                    logger.info(f"cdh_folder_checkpoint: {cdh_folder_checkpoint}")
                    spark.sparkContext.setCheckpointDir(cdh_folder_checkpoint)

                # Checkpoint
                return spark

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise


class HTMLFilter(HTMLParser):
    """Parses HTMLData

    Args:
        HTMLParser (_type_): _description_
    """

    text = ""

    def handle_data(self, data):
        """Parses HTMLData

        Args:
            data (_type_): _description_
        """
        self.text += data
