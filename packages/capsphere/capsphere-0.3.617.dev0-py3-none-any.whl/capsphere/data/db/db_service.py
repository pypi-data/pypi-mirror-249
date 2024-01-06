from capsphere.data.db.connector.abstract_connector import AbstractDatabaseConnection, AbstractDatabaseConnectionAsync


class DbQueryService:
    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection = db_connection

    def execute(self, query, params=None):
        with self.db_connection.get_connection():
            return self.db_connection.execute_single_query(query, params)


class DbQueryServiceAsync:
    def __init__(self, db_connection: AbstractDatabaseConnectionAsync):
        self.db_connection = db_connection

    async def execute_async(self, query, params=None):
        async with self.db_connection.get_connection_async():
            return await self.db_connection.execute_single_query_async(query, params)
