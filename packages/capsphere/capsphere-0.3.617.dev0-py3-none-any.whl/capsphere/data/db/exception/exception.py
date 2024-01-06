class DatabaseConnectionError(Exception):
    """Exception raised when the database connection fails."""
    pass


class DatabaseExecutionError(Exception):
    """Exception raised for errors during query execution."""
    pass
