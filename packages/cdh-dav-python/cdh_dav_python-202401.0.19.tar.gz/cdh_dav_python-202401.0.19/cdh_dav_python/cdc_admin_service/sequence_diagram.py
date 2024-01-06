import pandas as pd
import os
import sys
import re
import math
import datetime
from datetime import datetime, timedelta, time

from cdh_dav_python.cdc_admin_service import (
    environment_tracing as cdc_env_tracing,
    environment_logging as cdc_env_logging
)

from cdh_dav_python.cdc_tech_environment_service import (
    environment_file as cdc_env_file,
    environment_http as cdc_env_http
)

# Default request time out
REQUEST_TIMEOUT = 180
# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)
# Default limit item number of items to retrieve
LIMIT = 500


class SequenceDiagram:

    @staticmethod
    def format_log_entry(log_entry):
        # Convert timestamp to American date-time format
        timestamp = datetime.fromtimestamp(
            log_entry["Local time"] / 1000).strftime('%Y-%m-%d %I:%M:%S %p')

        # Create the formatted string based on the type of log entry
        if log_entry["type"] == "event":
            return f"{log_entry['ename']}, Duration: {log_entry['duration']} s, Timestamp: {timestamp}"
        else:
            return f"Severity level: {log_entry['severity']}, Message: {log_entry['message']}, Timestamp: {timestamp}"

    @staticmethod
    def extract_name(detail):
        match = re.search(r'Name: (\w+),', detail)
        return match.group(1) if match else ''

    @staticmethod
    def extract_severity_and_message_and_duration(detail):
        severity_match = re.search(r'Severity level: (\w+)', detail)
        message_match = re.search(r'Message: (.+)', detail)
        duration_match = re.search(r'Duration: (.+)', detail)

        severity = severity_match.group(1) if severity_match else ''
        message = message_match.group(1) if message_match else ''
        duration = duration_match.group(1) if duration_match else ''

        return severity, message, duration

    @staticmethod
    def calculate_duration(current_time, previous_time):

        # Handle None inputs
        if current_time is None or previous_time is None:
            return 0.0

        # Convert datetime.time to total seconds since midnight
        current_seconds = (current_time.hour * 3600 +
                           current_time.minute * 60 +
                           current_time.second +
                           current_time.microsecond / 1e6)

        prev_seconds = (previous_time.hour * 3600 +
                        previous_time.minute * 60 +
                        previous_time.second +
                        previous_time.microsecond / 1e6)

        duration = current_seconds - prev_seconds
        return round(duration, 1)

    @staticmethod
    def convert_time(time_str):
        # Handle float or integer inputs
        if isinstance(time_str, (float, int)):
            total_seconds = float(time_str)
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            seconds, microseconds = divmod(seconds, 1)
            microseconds *= 1e6  # Convert fractional seconds to microseconds
            return time(int(hours), int(minutes), int(seconds), int(microseconds))

        # Handle the "0" string case

        if isinstance(time_str, time):
            return time_str
        elif time_str == "0":
            return time(0, 0, 0)
        elif isinstance(time_str, str):
            return datetime.strptime(time_str, "%M:%S.%f").time()
        else:
            raise ValueError(f"Unsupported type {type(time_str)} for time_str")

    @classmethod
    def read_log_trace(cls, log_path=None, environment="dev", file_name="download_manifest_excel.xlsx"):
        """
        Reads a log trace from an Excel file, processes the data, and returns a DataFrame with log traces.

        Args:
            log_path (str, optional): The path to the directory where the Excel log file is located. If not provided, 
                                    a default path based on the executing script's directory and the environment 
                                    parameter will be constructed.
            environment (str, optional): Specifies the environment under which the log trace file is located. 
                                        Default is "dev".
            file_name (str, optional): Name of the Excel file containing the log traces. 
                                    Default is "download_manifest_excel.xlsx".

        Returns:
            pd.DataFrame: A DataFrame containing the processed log traces, sorted by 'Local time' and with a 
                        computed 'Duration' column in seconds.

        Raises:
            Exception: If an error occurs during the reading or processing of the Excel file.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("read_log_trace"):
            try:

                if log_path is None:
                    # Get the directory of the currently executing script (i.e., the 'tests' folder)
                    tests_directory = os.path.dirname(
                        os.path.abspath(__file__))
                    # Get the parent directory (i.e., the project root)
                    log_path = os.path.dirname(tests_directory)
                    log_path = (
                        log_path + "/" + environment + "_log_trace_sequence/"
                    )

                obj_file = cdc_env_file.EnvironmentFile()

                right_most_150_chars = file_name[-80:]
                file_name = right_most_150_chars

                log_path = obj_file.convert_to_current_os_dir(
                    log_path)

                logger.info("variable: " + log_path)

                log_excel_file = log_path + file_name
                logger.info("log_excel_file: " + log_excel_file)

                # Read the Excel file into a DataFrame from the first sheet
                df_log_trace = pd.read_excel(log_excel_file, sheet_name=0)

                # Apply the function to the 'Local time' column
                df_log_trace['Local time'] = df_log_trace['Local time'].apply(
                    cls.convert_time)

                # Sort by 'Local time'
                df_log_trace = df_log_trace.sort_values(by='Local time')

                # Extract name from details
                df_log_trace['Name'] = df_log_trace['Details'].apply(
                    cls.extract_name)

                # Extract severity and messages from details
                df_log_trace['Severity'], df_log_trace['Message'], df_log_trace['Duration'] = zip(
                    *df_log_trace['Details'].apply(cls.extract_severity_and_message_and_duration))

                # Drop the 'Type' column
                df_log_trace.drop(columns=['Type'], inplace=True)

                return df_log_trace

            except Exception as ex:
                # Corrected error message formatting
                error_msg = f"Excel Error: {str(ex)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def generate_timeline(cls, log_path=None, environment="dev", file_name="download_manifest_excel.xlsx"):
        """
        Generates a timeline string based on log trace data from an Excel file.

        This method reads log trace data from an Excel file, sorts it based on the 'Local time' field, and then 
        formats each log entry to generate a detailed timeline of events.

        Args:
            log_path (str, optional): The path to the directory where the Excel log file is located. If not provided, 
                                    a default path based on the executing script's directory and the environment 
                                    parameter will be constructed.
            environment (str, optional): Specifies the environment under which the log trace file is located. 
                                        Default is "dev".
            file_name (str, optional): Name of the Excel file containing the log traces. 
                                    Default is "download_manifest_excel.xlsx".

        Returns:
            str: A detailed timeline of events based on the log trace data.

        Raises:
            Exception: If an error occurs during the reading or processing of the Excel file or the generation 
                    of the timeline.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("generate_timeline"):
            try:

                # Variables to control the call stack level and indentation
                stack = []
                indentation = "  "
                previous_name = None

                # List to store the lines of the timeline
                timeline = []

                df_timeline = cls.read_log_trace(
                    log_path, environment, file_name)

                # Filter out empty names
                df_timeline = df_timeline[df_timeline['Name'].str.strip().ne(
                    '')]

                # Filter out __init__ names
                df_timeline = df_timeline[df_timeline['Name'] != '__init__']

                # Filter out get names and redundant functions
                df_timeline = df_timeline[df_timeline['Name'] != 'get']
                df_timeline = df_timeline[df_timeline['Name']
                                          != 'get_api_token']
                df_timeline = df_timeline[df_timeline['Name']
                                          != 'validate_api_token']
                df_timeline = df_timeline[df_timeline['Name']
                                          != 'get_api_token_from_config']
                df_timeline = df_timeline[df_timeline['Name']
                                          != 'convert_to_windows_dir']
                df_timeline = df_timeline[df_timeline['Name']
                                          != 'convert_to_current_os_dir']
                df_timeline = df_timeline[df_timeline['Name']
                                          != 'convert_to_unix_dir']
                for _, row in df_timeline.iterrows():
                    name = row['Name']
                    duration = row['Duration']
                    severity = row['Severity']
                    message = row['Message']

                    # Update stack based on call name
                    if name == '__init__':
                        stack.append(name)
                    elif previous_name == '__init__':
                        stack[-1] = name
                    elif name in stack:
                        # If the name is already in the stack, pop names until we find it
                        while stack and stack[-1] != name:
                            stack.pop()
                    else:
                        # If the name is not in the stack, simply add it
                        stack.append(name)

                    # Create the timeline entry
                    indents = len(stack) - 1

                    line = f"{indentation * indents}{name} [{duration}]"
                    if severity and message:
                        line += f" | {severity}: {message}"
                    timeline.append(line)

                    # Update previous name for the next iteration
                    previous_name = name

                content = "\n".join(timeline)

                new_file_name = file_name.rsplit('.', 1)[0] + ".txt"
                full_path = os.path.join(log_path, new_file_name)

                # Open the file at full_path in write mode with utf-8 encoding
                with open(full_path, 'w', encoding='utf-8') as file:
                    file.write(content)

                return content

            except Exception as ex:
                # Corrected error message formatting
                error_msg = f"Excel Error: {str(ex)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def generate_diagram(cls, log_path=None, environment="dev", file_name="download_manifest_excel.xlsx"):
        """
        Generates a sequence diagram in Mermaid notation based on log trace data from an Excel file.

        Args:
            log_path (str, optional): The path to the directory where the Excel log file is located. If not provided, 
                                    a default path based on the executing script's directory and the environment 
                                    parameter will be constructed.
            environment (str, optional): Specifies the environment under which the log trace file is located. 
                                        Default is "dev".
            file_name (str, optional): Name of the Excel file containing the log traces. 
                                    Default is "download_manifest_excel.xlsx".

        Returns:
            str: A sequence diagram in Mermaid notation based on the log trace data.

        Raises:
            Exception: If an error occurs during the reading or processing of the Excel file or the generation 
                    of the diagram.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("generate_diagram"):
            try:

                df = cls.read_log_trace(log_path, environment, file_name)

                # Process the data to generate Mermaid notation
                participants = df['Name'].unique()
                mermaid_code = "sequenceDiagram\n"
                for participant in participants:
                    mermaid_code += f"participant {participant}\n"

                previous_name = None
                for index, row in df.iterrows():
                    if previous_name:
                        mermaid_code += f"{previous_name}-->>{row['Name']}: {row['Details'].split(',')[0]}\n"
                        mermaid_code += f"Note right of {row['Name']}: Duration: {row['Duration']} s\n"
                    previous_name = row['Name']

                return mermaid_code

            except Exception as ex:
                # Corrected error message formatting
                error_msg = f"Excel Error: {str(ex)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

# Usage:
# file_path = 'path_to_your_excel_file.xlsx'
# diagram = SequenceDiagram.generate_diagram(file_path)
# print(diagram)
