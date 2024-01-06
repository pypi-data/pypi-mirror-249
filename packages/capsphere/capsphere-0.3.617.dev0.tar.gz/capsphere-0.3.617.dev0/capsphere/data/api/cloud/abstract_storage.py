from abc import ABC, abstractmethod

from capsphere.data.api.cloud.abstract_connector import CloudConnector


class CloudStorage(CloudConnector, ABC):

    @abstractmethod
    def upload_object(self, object_path: str, bucket: str) -> None:
        pass

    @abstractmethod
    def delete_object(self, object_name: str, bucket: str) -> None:
        pass

    @abstractmethod
    def get_object(self, object_name: str, bucket: str, file_path: str) -> None:
        pass

    @abstractmethod
    def get_total_objects(self, bucket: str) -> int:
        pass

    @abstractmethod
    def list_all_objects(self, bucket: str) -> list:
        pass
