import unittest
import subprocess
import os
from unittest.mock import patch
from cdh_dav_python.sphinx_service.sphinx_client import SphinxClient

if __name__ == "__main__":
    unittest.main()


class TestSphinxClient(unittest.TestCase):
    def test_build_html(self):
        """
        Test case for the build_html method of the SphinxClient class.

        This method tests the functionality of the build_html method by building
        the HTML documentation using the Sphinx source directory and asserts that
        the return code is 0, indicating a successful build.

        Returns:
            None
        """
        current_path = os.path.dirname(os.path.realpath(__file__))

        # Path to your Sphinx source directory (two directories up)
        sphinx_source_dir = os.path.abspath(
            os.path.join(current_path, "..", "..", "..", "docs")
        )

        obj_sphinx_client = SphinxClient()

        result = obj_sphinx_client.build_html(sphinx_source_dir)

        self.assertEqual(result.returncode, 0, "Sphinx build failed")

    def test_build_pdf(self):
        """
        Test case for the build_html method of the SphinxClient class.

        This method tests the functionality of the build_pdf method by building
        the PDF documentation using the Sphinx source directory and asserts that
        the return code is 0, indicating a successful build.

        Returns:
            None
        """
        current_path = os.path.dirname(os.path.realpath(__file__))

        # Path to your Sphinx source directory (two directories up)
        sphinx_source_dir = os.path.abspath(
            os.path.join(current_path, "..", "..", "..", "docs")
        )

        obj_sphinx_client = SphinxClient()

        result = obj_sphinx_client.build_pdf(sphinx_source_dir)

        self.assertEqual(result.returncode, 0, "Sphinx build failed")


if __name__ == "__main__":
    unittest.main()
