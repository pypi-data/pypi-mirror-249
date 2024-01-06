import unittest
from decimal import Decimal
from http import HTTPStatus

from pydantic import BaseModel

from capsphere.common import utils
from capsphere.data.api.cloud.aws.lambdas.response import ApiGwResponse


class MockObject(BaseModel):
    key: str
    dec_val: Decimal

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return utils.to_json(self.to_dict())


class TestResponse(unittest.TestCase):
    def test_apigw_response(self):
        mock_object = MockObject(key='some_key', dec_val=Decimal(1000.00))
        mock_object_json = mock_object.to_json()
        apigw_resp = ApiGwResponse(statusCode=HTTPStatus.OK, headers=None,
                                   body=mock_object_json)
        apigw_resp_dict = apigw_resp.to_dict()
        self.assertEqual(str, type(mock_object.key))
        self.assertEqual(Decimal, type(mock_object.dec_val))
        self.assertEqual(dict, type(apigw_resp_dict))
        self.assertEqual(int, type(apigw_resp_dict.get("statusCode")))
        self.assertEqual(200, apigw_resp_dict.get("statusCode"))

