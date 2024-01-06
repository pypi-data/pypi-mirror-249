import json
import re
import itertools
from dataclasses import fields

from decimal import Decimal
from typing import AnyStr


def read_file(filepath: str) -> AnyStr:
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"File not found from filepath: {filepath}"
    except Exception as e:
        return f"An error occurred while reading filepath: {filepath}: {e}"


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def from_json(data: str, cls):
    def convert_field(obj, field):
        field_type = field.type
        if field_type == Decimal:
            return Decimal(obj[field.name])
        return obj[field.name]

    data_dict = json.loads(data)
    kwargs = {field.name: convert_field(data_dict, field) for field in fields(cls)}
    return cls(**kwargs)


def to_json(obj):
    return json.dumps(obj, cls=DecimalEncoder)


def get_file_format(filename: str) -> str:
    parts = filename.split(".")
    if len(parts) == 2:
        return parts[1]
    else:
        raise ValueError(f"Unrecognised filename format '{filename}': Unable to split strings")


def read_list_from_file(filename: str) -> list:
    with open(filename, 'r') as file:
        my_list = json.load(file)

    for item in my_list:
        converted_item = {int(key): value for key, value in item.items()}
        item.clear()
        item.update(converted_item)

    return my_list


def process_text(text_list: list[str]):
    """
    This is where we standardise headers or text. Leading and trailing spaces in strings should be eliminated,
    periods at the start and end of strings should be eliminated too. Any periods or spaces in between strings
    must be converted to underscores.
    """
    processed_text = []
    for text in text_list:
        # remove leading and trailing spaces, periods, slashes and parenthesis
        text = text.strip(". /()")

        # replace spaces, periods, slashes and brackets in between text with underscores
        text = re.sub(r'[\s./]+', '_', text)

        # replace strings within brackets with underscores followed by the strings
        text = re.sub(r'\[([^]]+)\]', r'_\1', text)

        # remove any remaining underscores at the beginning or end
        text = text.strip('_')
        processed_text.append(text)
    return processed_text


def flatten_list(data: list[list]):
    return list(itertools
                .chain
                .from_iterable(data))
