import json
from typing import Any

from pydantic import BaseModel

from infraflow.runtime.lambdas.events.common import convert_dict_to_python_naming


class SqsLambdaMessageRecord(BaseModel):
    messageId: str
    receiptHandle: str
    body: str
    attributes: dict
    messageAttributes: dict
    md5OfBody: str
    eventSource: str
    eventSourceARN: str
    awsRegion: str

    _data = None

    @property
    def data(self):
        self._data = self._data or json.loads(self.body)
        return self._data


class SqsLambdaEvent(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**convert_dict_to_python_naming(data))

    records: list[SqsLambdaMessageRecord]
