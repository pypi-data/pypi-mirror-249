import json
from typing import TypeVar, ParamSpec, Generic, Any

from pydantic import BaseModel

from infraflow.runtime.lambdas.events.common import convert_dict_to_python_naming, dict_to_camel_shallow


class HttpLambdaRequestContext(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**convert_dict_to_python_naming(data, shallow=True))
    resource_path: str
    http_method: str
    path: str


class HttpLambdaEventBase(BaseModel):
    resource: str
    path: str
    headers: dict[str, str]
    multi_value_headers: dict[str, list[str]]
    stage_variables: dict[str, str]
    path_parameters: dict[str, str]

    http_method: str
    request_context: HttpLambdaRequestContext
    query_string_parameters: dict[str, str]
    multi_value_query_string_parameters: dict[str, list[str]]
    path_parameters: dict[str, str]
    stage_variables: dict[str, str]
    body: str
    is_base_64_encoded: bool


TQueryParams = TypeVar('TQueryParams')
TBody = TypeVar('TBody', dict, BaseModel, list, int, float, bool, str)
TPathParams = TypeVar('TPathParams')
P = ParamSpec("P")


class LambdaHttpRequest(HttpLambdaEventBase, Generic[TQueryParams, TBody]):
    query: TQueryParams
    data: TBody


class LambdaHttpAwsEvent(HttpLambdaEventBase):
    def __init__(self, **data: Any):
        super().__init__(**convert_dict_to_python_naming(data, shallow=True))

    @property
    def body_json(self):
        return json.loads(self.body)

    def request(self, TQueryParams: type, TBody: type):
        return LambdaHttpRequest(
            query=TQueryParams(self.query_string_parameters),
            data=TBody(self.body_json),
            **self.model_dump()
        )


class LambdaAwsHttpResult(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**dict_to_camel_shallow(data))
    status_code: int
    headers: dict[str, list[str]]
    is_base_64_encoded: bool
    multi_value_headers: dict[str, list[str]]
    body: str


class LambdaHttpResponse(BaseModel, Generic[TBody]):
    status_code: int
    headers: dict[str, list[str]]
    is_base_64_encoded: bool
    multi_value_headers: dict[str, list[str]]
    data: TBody

    def to_aws(self):
        dump = self.model_dump()
        body = json.dumps(dump.pop('data'))
        return LambdaAwsHttpResult(**dump, body=body)

