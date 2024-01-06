from abc import ABC, abstractmethod
from contextlib import contextmanager, asynccontextmanager


class AbstractDatabaseConnection(ABC):
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    @abstractmethod
    def connect(self):
        """Establishes a connection to the database."""
        pass

    @abstractmethod
    def disconnect(self):
        """Closes the database connection."""
        pass

    @abstractmethod
    def execute_single_query(self, query, params=None):
        """Executes a single query."""
        pass

    @contextmanager
    def get_connection(self):
        self.connect()
        try:
            yield self
        finally:
            self.disconnect()


class AbstractDatabaseConnectionAsync(ABC):
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    @abstractmethod
    def connect_async(self):
        pass

    @abstractmethod
    def disconnect_async(self):
        """Closes the database connection."""
        pass

    @abstractmethod
    def execute_single_query_async(self, query, params=None):
        """Executes a single asynchronous query."""
        pass

    @asynccontextmanager
    async def get_connection_async(self):
        await self.connect_async()
        try:
            yield self
        finally:
            await self.disconnect_async()
