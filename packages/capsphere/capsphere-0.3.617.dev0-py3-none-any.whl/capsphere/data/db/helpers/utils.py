import os
from dataclasses import is_dataclass, fields
from datetime import date, datetime

from pydantic import BaseModel


def check_env_vars(env_vars, logger):
    """Checks if the required environment variables are set."""
    for var in env_vars:
        if os.getenv(var) is None:
            message = f"The environment variable {var} is not set. It is required for the database connection."
            logger.error(message)
            raise EnvironmentError(message)


def map_row_to_dataclass(model_type: type, row: tuple, headers: list[str]):
    if not issubclass(model_type, BaseModel):
        raise ValueError(f"{model_type.__name__} is not a Pydantic model")

    # Zip headers and row values and create a dict
    row_dict = dict(zip(headers, row))

    # Convert datetime and date to ISO 8601 format string
    for key, value in row_dict.items():
        if isinstance(value, (datetime, date)):
            row_dict[key] = value.isoformat()

    # Instantiate the Pydantic model
    return model_type(**row_dict)

    # if not is_dataclass(dataclass_type):
    #     raise ValueError(f"{dataclass_type.__name__} is not a dataclass")
    #
    # dataclass_fields = {f.name: f.type for f in fields(dataclass_type)}
    # mapped_data = {}
    # for header, value in zip(headers, row):
    #     if header in dataclass_fields:
    #         if isinstance(value, datetime):
    #             # Convert datetime to ISO 8601 format string
    #             mapped_data[header] = value.isoformat()
    #         elif isinstance(value, date):
    #             # Convert date to ISO 8601 format string
    #             mapped_data[header] = value.isoformat()
    #         else:
    #             mapped_data[header] = value
    #
    # return dataclass_type(**mapped_data)


def get_model_list_from_query(query_result: tuple, class_type: type) -> list[any]:
    data = query_result[0]
    headers = query_result[1]

    data_list = []

    for row in data:
        loan = map_row_to_dataclass(class_type, row, headers)
        data_list.append(loan)

    return data_list
