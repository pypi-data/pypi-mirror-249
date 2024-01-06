# import mysql.connector
# import os
# import logging
# import aiomysql
#
# from capsphere.data.db.exception import DatabaseConnectionError, DatabaseExecutionError
# from capsphere.data.db.interface import BaseDBConnection
# from mysql.connector import Error as MySQLError
#
#
# class Connector(BaseDBConnection):
#     def __init__(self, ssl_cert_path=None):
#         self.logger = logging.getLogger(__name__)
#
#         env_vars = ['MYSQL_DB_HOST', 'MYSQL_DB_NAME', 'MYSQL_DB_USER', 'MYSQL_DB_PASSWORD', 'MYSQL_DB_PORT']
#         for var in env_vars:
#             if os.getenv(var) is None:
#                 message = f"The environment variable {var} is not set. It is required for MySQL database connection."
#                 self.logger.error(message)
#                 raise EnvironmentError(message)
#
#         super().__init__(
#             host=os.getenv('MYSQL_DB_HOST'),
#             database=os.getenv('MYSQL_DB_NAME'),
#             user=os.getenv('MYSQL_DB_USER'),
#             password=os.getenv('MYSQL_DB_PASSWORD'),
#             port=int(os.getenv('MYSQL_DB_PORT', 3306))
#         )
#         self.ssl_cert_path = ssl_cert_path
#
#     def connect(self):
#         if not self.connection:
#             try:
#                 connection_args = {
#                     "host": self.host,
#                     "database": self.database,
#                     "user": self.user,
#                     "password": self.password,
#                     "port": self.port
#                 }
#                 if self.ssl_cert_path:
#                     connection_args['ssl_ca'] = self.ssl_cert_path
#                     connection_args['ssl_verify_cert'] = True
#
#                 self.connection = mysql.connector.connect(**connection_args)
#             except MySQLError as e:
#                 self.logger.error(f"Database connection failed: {e}")
#                 raise DatabaseConnectionError(e)
#         return self.connection
#
#     def disconnect(self):
#         if self.connection:
#             self.connection.close()
#             self.connection = None
#
#     def execute_query(self, query, fetch_results=True):
#         connection = self.connect()
#         cursor = connection.cursor()
#         result = None
#         try:
#             cursor.execute(query)
#             connection.commit()
#             if fetch_results:
#                 result = cursor.fetchall()
#         except MySQLError as e:
#             connection.rollback()
#             self.logger.error(f"Query execution failed: {e}")
#             raise DatabaseExecutionError(e)
#         finally:
#             cursor.close()
#             self.disconnect()
#         return result
#
#     async def connect_async(self):
#         if not self.connection:
#             try:
#                 connection_args = {
#                     "host": self.host,
#                     "user": self.user,
#                     "db": self.database,
#                     "password": self.password,
#                     "port": self.port,
#                 }
#                 if self.ssl_cert_path:
#                     connection_args['ssl'] = {'ca': self.ssl_cert_path}
#                     connection_args['ssl_verify_cert'] = True
#
#                 self.connection = await aiomysql.connect(**connection_args)
#             except aiomysql.Error as e:
#                 self.logger.error(f"Async database connection failed: {e}")
#                 raise DatabaseConnectionError(e)
#
#     async def disconnect_async(self):
#         if self.connection:
#             self.connection.close()
#             await self.connection.wait_closed()
#             self.connection = None
#
#     async def execute_query_async(self, query, fetch_results=True):
#         await self.connect_async()
#         async with self.connection.cursor() as cursor:
#             result = None
#             try:
#                 await cursor.execute(query)
#                 await self.connection.commit()
#                 if fetch_results:
#                     result = await cursor.fetchall()
#             except aiomysql.Error as e:
#                 await self.connection.rollback()
#                 self.logger.error(f"Async query execution failed: {e}")
#                 raise DatabaseExecutionError(e)
#             return result
