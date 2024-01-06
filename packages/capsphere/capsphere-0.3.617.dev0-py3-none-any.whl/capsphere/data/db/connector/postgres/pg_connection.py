import logging
import os
import psycopg

from contextlib import contextmanager, asynccontextmanager
from psycopg import OperationalError
from capsphere.data.db.connector.abstract_connector import AbstractDatabaseConnection, AbstractDatabaseConnectionAsync
from capsphere.data.db.connector.postgres.utils import build_connection_args
from capsphere.data.db.exception import DatabaseConnectionError, DatabaseExecutionError
from capsphere.data.db.helpers.utils import check_env_vars


class PostgresConnector(AbstractDatabaseConnection):
    def __init__(self, ssl_cert_path=None):
        self.logger = logging.getLogger(__name__)

        check_env_vars(['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_PORT'], self.logger)

        super().__init__(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', 5432))
        )
        self.ssl_cert_path = ssl_cert_path

    def connect(self):
        """
        Establishes a connection to the database.
        """
        if not self.connection:
            try:
                connection_args = build_connection_args(self.host, self.database, self.user, self.password, self.port,
                                                        self.ssl_cert_path)
                self.connection = psycopg.connect(**connection_args)
            except OperationalError as e:
                raise DatabaseConnectionError(e)

    def disconnect(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_single_query(self, query, params=None) -> tuple[list, list] | int:
        """
        Executes a single query with parameters.
        """
        if not self.connection:
            raise DatabaseConnectionError("Not connected to the database.")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)

                # Determine the type of query (read or write)
                is_write_operation = any(word in query.upper() for word in ["INSERT", "UPDATE", "DELETE", "DROP"])
                should_fetch = "SELECT" in query.upper() or "RETURNING" in query.upper()

                if should_fetch and cursor.description:
                    # Fetch results for SELECT or RETURNING clause
                    headers = [desc[0] for desc in cursor.description]
                    result = cursor.fetchall()
                    if is_write_operation:
                        self.connection.commit()  # Commit if it's a write operation
                    return result, headers
                elif is_write_operation:
                    # Commit for write operations without RETURNING
                    self.connection.commit()
                    return cursor.rowcount
                else:
                    return list(), list()
        except Exception as e:
            raise DatabaseExecutionError(f"Error executing query: {e}")


class PostgresConnectorAsync(AbstractDatabaseConnectionAsync):
    def __init__(self, ssl_cert_path=None):
        self.logger = logging.getLogger(__name__)

        check_env_vars(['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_PORT'], self.logger)

        super().__init__(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', 5432))
        )
        self.ssl_cert_path = ssl_cert_path

    async def ensure_connection(self):
        """
        Ensure that the database connection is established.
        """
        if not self.connection:
            await self.connect_async()

    async def connect_async(self):
        """
        Establishes an asynchronous connection to the database.
        """
        if not self.connection:
            try:
                connection_args = build_connection_args(self.host, self.database, self.user, self.password, self.port,
                                                        self.ssl_cert_path)
                self.connection = await psycopg.AsyncConnection.connect(**connection_args)
            except OperationalError as e:
                raise DatabaseConnectionError(e)

    async def disconnect_async(self):
        """
        Closes the asynchronous database connection.
        """
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def execute_single_query_async(self, query, params=None):
        """
        Executes a single asynchronous query.
        """
        if not self.connection:
            raise DatabaseConnectionError("Not connected to the database.")

        try:
            async with self.connection.cursor() as cursor:
                await cursor.execute(query, params)

                # Determine the type of query (read or write)
                is_write_operation = any(word in query.upper() for word in ["INSERT", "UPDATE", "DELETE"])
                should_fetch = "SELECT" in query.upper() or "RETURNING" in query.upper()

                if should_fetch and cursor.description:
                    # Fetch results for SELECT or RETURNING clause
                    headers = [desc[0] for desc in cursor.description]
                    result = cursor.fetchall()
                    if is_write_operation:
                        await self.connection.commit()  # Commit if it's a write operation
                    return result, headers
                elif is_write_operation:
                    # Commit for write operations without RETURNING
                    await self.connection.commit()
                    return cursor.rowcount
                else:
                    return list(), list()
        except Exception as e:
            raise DatabaseExecutionError(f"Error executing query: {e}")
