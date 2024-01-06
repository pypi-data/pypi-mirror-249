class AWSConnectionError(Exception):
    """Exception raised when the AWS connection fails."""
    pass


class AWSExecutionError(Exception):
    """Exception raised for errors during query execution of AWS functions."""
    pass


class PayexConnectionError(Exception):
    """Exception raised when the Payex connection fails."""
    pass


class PayexExecutionError(Exception):
    """Exception raised for errors during query execution of Payex functions."""
    pass
