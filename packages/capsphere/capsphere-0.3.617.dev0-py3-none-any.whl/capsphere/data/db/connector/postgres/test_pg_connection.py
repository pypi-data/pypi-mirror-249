import unittest
import asyncio
import os

from unittest.mock import patch

from dotenv import load_dotenv

from capsphere.data.db.connector.postgres import PostgresConnector

load_dotenv()


#
# if os.name == 'nt':
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#
#
class TestConnection(unittest.TestCase):

    def test_connector(self):
        """Test the Connector class."""
        # Set up environment variables here if not already set
        connector = PostgresConnector()
        try:
            connector.connect()
            # Optionally, you can perform additional checks here
        finally:
            connector.disconnect()

#     def test_connector_context(self):
#         connector = Connector()
#         with connector.get_connection():
#             data = connector.execute_query("SELECT * FROM loan_amortizations")
#             print(data)
# #
#
# @unittest.skip
# class TestConnectorAsync(unittest.IsolatedAsyncioTestCase):
#     async def test_connector_async(self):
#         """Test the ConnectorAsync class."""
#         # Set up environment variables here if not already set
#         connector = ConnectorAsync()
#         try:
#             await connector.connect_async()
#             # Optionally, you can perform additional checks here
#         finally:
#             await connector.disconnect_async()
#
#     # @patch('capsphere.data.db.postgres.connection.os.getenv')
#     # def test_missing_environment_variables(self, mock_getenv):
#     #     mock_getenv.return_value = None
#     #
#     #     # Attempt to instantiate the connection, which should raise EnvironmentError
#     #     with self.assertRaises(EnvironmentError) as context:
#     #         connection = Connector(ssl_cert_path='/path/to/cert')
#     #
#     #     # Check if the error message is correct
#     #     self.assertIn("The environment variable DB_HOST is not set", str(context.exception))
#
#     # def test_postgres(self):
#     #     # pg_db = PostgreSQLConnection(ssl_cert_path=self.pem_path)
#     #     pg_db = PostgreSQLConnection()
#     #     try:
#     #         connection = pg_db.connect()
#     #         print("Connection successful.")
#     #     except Exception as e:
#     #         print(f"Connection failed: {e}")
#     #     finally:
#     #         if pg_db.connection:
#     #             pg_db.disconnect()
