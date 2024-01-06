from enum import Enum


class PayexAuthCode(Enum):
    SUCCESS = '00'
    PENDING = '09'
    PENDING_2 = '99'
    CORPORATE_MODE = '02'
    RETAIL_MODE = '01'


def verify_response(data: dict):
    """
    :param data:
    :return:

    TODO
    Verify the data that is coming in from the http request. It will be a dictionary, and
    you will probably have to look at the txn_id and signature. Return true if verified, false
    otherwise. Put all the necessary variables in a .env file in the parent directory
    """
    return
