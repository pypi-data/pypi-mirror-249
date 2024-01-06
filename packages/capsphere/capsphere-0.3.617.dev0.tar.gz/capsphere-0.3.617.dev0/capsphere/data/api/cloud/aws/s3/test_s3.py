import os
import unittest
from unittest.mock import patch, Mock

from dotenv import load_dotenv

from capsphere.data.api.cloud.aws.s3 import S3Client
from capsphere.data.api.exception import AWSConnectionError

load_dotenv()


class TestS3(unittest.TestCase):

    @patch('boto3.client')
    def test_connect_success(self, mock_boto_client):
        # Set up the mock client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client

        # Instantiate and connect the service
        s3_service = S3Client(aws_access_key_id='dummy_key',
                              aws_secret_access_key='dummy_secret',
                              region_name='dummy_region')
        s3_service.connect('s3')

        # Assert that boto3.client was called with the correct arguments
        mock_boto_client.assert_called_with('s3', aws_access_key_id='dummy_key',
                                            aws_secret_access_key='dummy_secret',
                                            region_name='dummy_region')
        # Assert that the client is set
        self.assertIsNotNone(s3_service.client)

    @patch('boto3.client')
    def test_connect_failure(self, mock_boto_client):
        # Set up the mock to raise an exception
        mock_boto_client.side_effect = AWSConnectionError

        s3_service = S3Client(aws_access_key_id='dummy_key',
                              aws_secret_access_key='dummy_secret',
                              region_name='dummy_region')

        # Test that connect raises AWSConnectionError
        with self.assertRaises(AWSConnectionError):
            s3_service.connect()

    @unittest.skip('Skip as not required, integration test')
    def test_count_objects_in_bucket(self):
        s3_service = S3Client(aws_access_key_id=os.getenv('aws_access_key_id'),
                              aws_secret_access_key=os.getenv('aws_secret_access_key'),
                              region_name='ap-southeast-1')

        s3_client = s3_service.connect()
        print(s3_client.get_total_objects('capsphere-candidates'))

    @unittest.skip('Skip as not required, integration test')
    def test_upload_object_into_bucket(self):
        s3_service = S3Client(aws_access_key_id=os.getenv('aws_access_key_id'),
                              aws_secret_access_key=os.getenv('aws_secret_access_key'),
                              region_name='ap-southeast-1')

        s3_client = s3_service.connect()
        s3_client.upload_object('potential', 'capsphere-candidates')

    @unittest.skip('Skip as not required, integration test')
    def test_delete_object_from_bucket(self):
        s3_service = S3Client(aws_access_key_id=os.getenv('aws_access_key_id'),
                              aws_secret_access_key=os.getenv('aws_secret_access_key'),
                              region_name='ap-southeast-1')

        s3_client = s3_service.connect()
        s3_client.delete_object('capsphere_questions.pdf', 'capsphere-candidates')
