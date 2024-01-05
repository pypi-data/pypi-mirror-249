import json
from typing import Any

from pydantic import BaseModel

from infraflow.runtime.docker.contracts.common import convert_dict_to_python_naming


class SqsBotoMessageRecord(BaseModel):
    messageId: str
    receiptHandle: str
    body: str
    attributes: dict
    messageAttributes: dict
    md5OfBody: str

    _data = None

    @property
    def data(self):
        self._data = self._data or json.loads(self.body)
        return self._data


class SqsBotoResult(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**convert_dict_to_python_naming(data))

    messages: list[SqsBotoMessageRecord]
