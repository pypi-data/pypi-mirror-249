from dataclasses import dataclass, asdict
from typing import Optional

from pydantic import BaseModel

from capsphere.common import utils


class ApiGwResponse(BaseModel):
    statusCode: int
    headers: Optional[dict]
    body: Optional[str]

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return utils.to_json(self.to_dict())
