import os
import sys
from unittest.mock import patch

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

import pytest

if sys.platform == "win32":
    from cdh_dav_python.windows_service.windows_credential import WindowsCredential
    import win32cred

sys.path.append("..")


@pytest.fixture
def mocker():
    with patch.object(win32cred, "CredEnumerate") as mock_CredEnumerate:
        yield mock_CredEnumerate


def test_list_credentials():
    if sys.platform != "win32":
        return

    # Call the function under test
    credentials = WindowsCredential.list_credentials()

    # Assert the returned credentials match the expected value
    # assert credentials == expected_credentials

    print(credentials)


def test_get_credential_by_address(mocker):
    if sys.platform != "win32":
        return

    # Define the expected credential
    expected_credential = {
        "TargetName": "git:https://github.com",
        "UserName": "username",
        "CredentialBlob": "password",
    }
    mocker.return_value = [expected_credential]

    # Call the function under test
    credential = WindowsCredential.get_credential_by_address(
        "LegacyGeneric:target=GitHub - https://api.github.com/jcbowyer"
    )

    # Assert that the mocked function was called correctly
    # mocker.assert_called_once_with(None, win32cred.CRED_TYPE_GENERIC)

    # Assert the returned credential matches the expected value
    # assert credential == expected_credential

    print(credential)


def test_file_trace_exporter_to_readable_dict():
    # Create an instance of FileTraceExporter
    exporter = FileTraceExporter()

    # Create a span object for testing
    span = Span()

    # Set span attributes
    span.set_span_context(SpanContext(trace_id=123, span_id=456))
    span.parent = Span()
    span.name = "Test Span"
    span.status = Status(status_code=StatusCode.OK)
    span.kind = SpanKind.INTERNAL
    span.start_time = datetime.now()
    span.end_time = datetime.now()
    span.attributes = {"key": "value"}

    # Call the to_readable_dict method
    result = exporter.to_readable_dict(span)

    # Assert the returned value matches the expected value
    expected_result = {
        "trace_id": "123",
        "span_id": "456",
        "parent_id": "None",
        "name": "Test Span",
        "status": "OK",
        "kind": "INTERNAL",
        "start_time": str(span.start_time),
        "end_time": str(span.end_time),
        "attributes": {"key": "value"},
    }
    assert result == expected_result


def test_file_trace_exporter_export():
    # Create an instance of FileTraceExporter
    exporter = FileTraceExporter()

    # Create a list of spans for testing
    spans = [Span(), Span()]

    # Call the export method
    result = exporter.export(spans)

    # Assert the returned value matches the expected value
    assert result == SpanExportResult.SUCCESS


def test_file_trace_exporter_delete_old_files():
    # Create an instance of FileTraceExporter
    exporter = FileTraceExporter()

    # Create a temporary folder for testing
    folder_path = "/tmp/test_folder"
    os.makedirs(folder_path, exist_ok=True)

    # Create a temporary file within the folder
    file_path = os.path.join(folder_path, "test_file.txt")
    with open(file_path, "w") as file:
        file.write("Test")

    # Call the delete_old_files method
    exporter.delete_old_files()

    # Assert that the file has been deleted
    assert not os.path.exists(file_path)

    # Cleanup the temporary folder
    os.rmdir(folder_path)


if __name__ == "__main__":
    pytest.main()
