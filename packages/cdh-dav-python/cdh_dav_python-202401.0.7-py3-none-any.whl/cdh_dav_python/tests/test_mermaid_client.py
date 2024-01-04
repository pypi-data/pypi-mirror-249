import subprocess
import unittest
from io import StringIO
from unittest.mock import patch
from cdh_dav_python.mermaid_service.mermaid_client import MermaidClient


class TestMermaidClient(unittest.TestCase):
    """
    Unit test class for testing the MermaidClient class.
    """

    def test_add_mermaid_to_path(self):
        """
        Test case to verify the functionality of adding Mermaid to the path.

        This test case performs the following steps:
        1. Sets up the expected output.
        2. Creates an instance of the MermaidClient class.
        3. Calls the add_mermaid_to_path method.
        4. Asserts that the actual output matches the expected output.

        """

        # Arrange
        expected_output = "current_working_dir:/path/to/current/working/dir\n"
        expected_output += "b'1.1.0\\n': poetry version succeeded"

        # Act
        obj_mermaid_client = MermaidClient()
        actual_output = obj_mermaid_client.add_mermaid_to_path()

        # Assert
        self.assertEqual(actual_output, expected_output)

    def test_install_mermaid(self):
        """
        Test case for the install_mermaid method of the MermaidClient class.

        This test verifies that the install_mermaid method correctly installs Mermaid
        and produces the expected output.

        Steps:
        1. Arrange the expected output.
        2. Create an instance of the MermaidClient class.
        3. Call the install_mermaid method.
        4. Assert that the output matches the expected output.
        """
        # Arrange
        expected_output = "current_working_dir:/path/to/current/working/dir\n"
        expected_output += "b'1.1.0\\n': poetry version succeeded"

        # Act
        obj_mermaid_client = MermaidClient()
        actual_output = obj_mermaid_client.install_mermaid()

        # Assert
        self.assertEqual(actual_output, expected_output)

    def test_show_help(self):
        """
        Test case for the show_help method of the MermaidClient class.

        This test verifies that the show_help method returns the expected output.

        Steps:
        1. Arrange the expected output.
        2. Create an instance of the MermaidClient class.
        3. Call the show_help method.
        4. Assert that the actual output matches the expected output.
        """

        # Arrange
        expected_output = "current_working_dir:/path/to/current/working/dir\n"
        expected_output += "b'1.1.0\\n': poetry version succeeded"

        # Act
        obj_mermaid_client = MermaidClient()
        actual_output = obj_mermaid_client.show_help()

        # Assert
        self.assertEqual(actual_output, expected_output)


if __name__ == "__main__":
    unittest.main()
