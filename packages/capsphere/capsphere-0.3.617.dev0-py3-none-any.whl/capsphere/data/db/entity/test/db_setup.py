import re

from capsphere.data.db.connector.postgres import PostgresConnector
from capsphere.data.db.db_service import DbQueryService


def run_sql_script(file_name: str) -> None:
    db_query_service = DbQueryService(PostgresConnector())
    with open(file_name, 'r') as file:
        sql_script = file.read()
        db_query_service.execute(sql_script)


def drop_table(table_name: str) -> None:
    if not _is_safe_table_name(table_name):
        raise ValueError(f"Unsafe table name: {table_name}")
    db_query_service = DbQueryService(PostgresConnector())
    query = f"DROP TABLE IF EXISTS {table_name}"
    db_query_service.execute(query)


def _is_safe_table_name(table_name: str):
    """
    Check if the table name is safe to be included in a SQL query.
    This is a basic check. You might want to extend this depending on your requirements.
    """
    return re.match("^[A-Za-z0-9_]+$", table_name) is not None
