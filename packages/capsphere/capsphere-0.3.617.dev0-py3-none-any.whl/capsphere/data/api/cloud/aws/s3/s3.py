import logging

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from capsphere.data.api.cloud.abstract_storage import CloudStorage
from capsphere.data.api.exception import AWSConnectionError, AWSExecutionError

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)
logging.getLogger(__name__).setLevel(logging.DEBUG)


class S3Client(CloudStorage):
    """
    AWS S3 Connector using boto3.
    """

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.client = None

    def connect(self, service='s3'):
        """
        Establishes a client connection to AWS S3
        """
        if not self.client:
            try:
                self.client = boto3.client(
                    service,
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key,
                    region_name=self.region_name
                )
            except (BotoCoreError, ClientError) as e:
                raise AWSConnectionError(f"Error connecting to AWS s3 client via boto3 library: {e}")
        return self

    def upload_object(self, object_path: str, bucket_name: str):
        self._ensure_connected()
        try:
            with open(object_path, 'rb') as data:
                self.client.upload_fileobj(data, bucket_name, object_path)
        except (BotoCoreError, ClientError) as e:
            raise AWSExecutionError(f"Error uploading object from '{object_path}' to S3 bucket '{bucket_name}': {e}")

    def delete_object(self, object_name: str, bucket_name: str):
        self._ensure_connected()
        try:
            self.client.delete_object(Bucket=bucket_name, Key=object_name)
        except (BotoCoreError, ClientError) as e:
            raise AWSExecutionError(f"Error deleting object '{object_name}' from S3 bucket '{bucket_name}': {e}")

    def get_object(self, object_name: str, bucket_name: str, file_path: str):
        self._ensure_connected()
        try:
            with open(file_path, 'wb') as data:
                self.client.download_fileobj(bucket_name, object_name, data)
        except (BotoCoreError, ClientError) as e:
            raise AWSExecutionError(
                f"Error downloading object '{object_name}' from S3 bucket '{bucket_name}' to '{file_path}': {e}")

    def get_total_objects(self, bucket_name: str) -> int:
        self._ensure_connected()
        try:
            total_objects = 0
            paginator = self.client.get_paginator('list_objects_v2')

            for page in paginator.paginate(Bucket=bucket_name):
                total_objects += len(page.get('Contents', []))

            return total_objects
        except (BotoCoreError, ClientError) as e:
            raise AWSExecutionError(f"Error getting total objects from S3 bucket '{bucket_name}': {e}")

    def list_all_objects(self, bucket_name: str) -> list:
        self._ensure_connected()
        all_objects = []

        try:
            response = self.client.list_objects_v2(Bucket=bucket_name)

            while True:
                if 'Contents' in response:
                    for obj in response['Contents']:
                        all_objects.append(obj['Key'])

                # Check if there are more objects and if so, continue listing
                if response.get('IsTruncated'):
                    response = self.client.list_objects_v2(Bucket=bucket_name,
                                                           ContinuationToken=response.get('NextContinuationToken'))
                else:
                    break

            return all_objects
        except (BotoCoreError, ClientError) as e:
            raise AWSExecutionError(f"Error listing objects in S3 bucket '{bucket_name}': {e}")

    def _ensure_connected(self):
        if self.client is None:
            raise AWSConnectionError("AWS Connector is not connected to S3.")


class S3Resource:
    pass


class S3Session:
    pass
