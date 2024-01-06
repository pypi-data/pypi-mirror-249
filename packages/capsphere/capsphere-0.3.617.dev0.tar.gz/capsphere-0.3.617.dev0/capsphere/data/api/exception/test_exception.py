import unittest

from capsphere.data.api.exception import AWSExecutionError


class TestException(unittest.TestCase):
    def test_exception(self):
        aws_exec_error = AWSExecutionError()
