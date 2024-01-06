from abc import ABC, abstractmethod


class CloudConnector(ABC):
    """
    Abstract base class for cloud connectors.
    """

    @abstractmethod
    def connect(self, service: str):
        """
        Establishes a connection to the specified AWS service.
        """
        pass
