from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from capsphere.data.db.entity.abstract_entity import DbEntity
from capsphere.data.model.data_record import DataRecord
from typing import Optional

T = TypeVar('T', bound=DataRecord | DbEntity)
K = TypeVar('K', bound=list[DataRecord] | list[DbEntity])


class DataProcessor(ABC, Generic[T, K]):

    def __init__(self, data: dict, **tables: T):
        self.data = data
        self.tables = tables

    @abstractmethod
    def process(self) -> Optional[K]:
        raise NotImplementedError("process method not implemented")
