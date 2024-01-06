import unittest
from unittest.mock import MagicMock
from cdh_dav_python.az_key_vault_service.az_key_vault import AzureKeyVault


class TestAzureKeyVault(unittest.TestCase):
    def setUp(self):
        self.vault_url = "https://example-vault.vault.azure.net"
        self.tenant_id = "tenant-id"
        self.client_id = "client-id"
        self.running_interactive = True

        self.key_vault = AzureKeyVault(
            self.vault_url, self.tenant_id, self.client_id, self.running_interactive
        )

    def test_get_secret_interactive(self):
        """
        Test case for the get_secret_interactive method.

        This test mocks the necessary dependencies and verifies that the get_secret method
        correctly retrieves the secret value from the key vault.

        It asserts that the retrieved secret value matches the expected secret value,
        and that the necessary methods for retrieving the secret are called with the correct arguments.
        """
        # Mock the necessary dependencies
        self.key_vault.get_credential_device = MagicMock(
            return_value="device_credential"
        )
        self.key_vault.get_secret_client = MagicMock(return_value="device_client")
        self.key_vault.retrieve_secret = MagicMock(return_value="secret_value")

        secret_name = "my_secret"
        secret_value = self.key_vault.get_secret(secret_name)

        self.assertEqual(secret_value, "secret_value")
        self.key_vault.get_credential_device.assert_called_once()
        self.key_vault.get_secret_client.assert_called_once_with("device_credential")
        self.key_vault.retrieve_secret.assert_called_once_with(
            "device_client", secret_name
        )

    def test_get_secret_non_interactive(self):
        """
        Test case for the 'get_secret' method when running in non-interactive mode.

        This test mocks the necessary dependencies and sets the 'running_interactive' flag to False.
        It then calls the 'get_secret' method with a secret name and asserts that the returned secret value matches the expected value.
        Additionally, it verifies that the 'get_credential', 'get_secret_client', and 'retrieve_secret' methods are called with the expected arguments.

        """
        # Mock the necessary dependencies
        self.key_vault.get_credential = MagicMock(return_value="client_credential")
        self.key_vault.get_secret_client = MagicMock(return_value="client")
        self.key_vault.retrieve_secret = MagicMock(return_value="secret_value")

        # Set running_interactive to False
        self.key_vault.running_interactive = False

        secret_name = "my_secret"
        secret_value = self.key_vault.get_secret(secret_name)

        self.assertEqual(secret_value, "secret_value")
        self.key_vault.get_credential.assert_called_once()
        self.key_vault.get_secret_client.assert_called_once_with("client_credential")
        self.key_vault.retrieve_secret.assert_called_once_with("client", secret_name)


if __name__ == "__main__":
    unittest.main()
