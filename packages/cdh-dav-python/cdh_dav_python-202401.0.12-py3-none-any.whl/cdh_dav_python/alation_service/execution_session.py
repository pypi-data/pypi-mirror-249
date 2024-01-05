import os
import sys
import json
import requests

from cdh_dav_python.cdc_admin_service import (
    environment_tracing as cdc_env_tracing,
    environment_logging as cdc_env_logging
)

from cdh_dav_python.cdc_tech_environment_service import (
    environment_http as cdc_env_http
)


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

TIMEOUT_5_SEC = 5
TIMEOUT_ONE_MIN = 60
# Get the currently running file name


class ExecutionSession:

    def get_execution_sessions(self, edc_alation_base_url):

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_execution_sessions"):

            logger.info("##### Get all execution sessions #####")
            api_url = "/integration/v1/query/execution_session/"
            session_list_url = edc_alation_base_url + api_url
            response = requests.get(session_list_url,
                                    headers=headers,
                                    timeout=TIMEOUT_ONE_MIN)
            sessions = json.loads(response.text)
            for session in sessions:
                session_id = session["id"]
                client_session_id = session["client_session_id"]
                msg = f"ID: {session_id}, Client-session-ID: {client_session_id}"
                logger.info(msg)

            query_id = "249"
