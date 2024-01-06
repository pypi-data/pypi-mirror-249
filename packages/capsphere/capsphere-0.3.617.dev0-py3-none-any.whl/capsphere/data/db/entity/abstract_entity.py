from abc import ABC

from capsphere.data.db import DbQueryService, DbQueryServiceAsync


class DbEntity(ABC):
    def __init__(self, db_query_service: DbQueryService):
        self.db_query_service = db_query_service

