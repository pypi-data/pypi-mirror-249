from typing import TypeVar, ParamSpec, Callable, Concatenate, Union

from pydantic import BaseModel

from infraflow.runtime.lambdas.events.http import LambdaHttpRequest, LambdaHttpResponse, LambdaHttpAwsEvent

TQueryParams = TypeVar('TQueryParams')
TBody = TypeVar('TBody')
TPathParams = TypeVar('TPathParams')
P = ParamSpec("P")


def http_handler(func: Callable[
    Concatenate[LambdaHttpRequest[TBody, TQueryParams], LambdaHttpResponse, P],
    Union[dict, BaseModel, list[dict], list[str], list[str], list[BaseModel], list[int], list[float], list[bool]],
]):
    def wrapped(event, context):
        e = LambdaHttpAwsEvent(**event)
        return func(e.request(TBody, TQueryParams), LambdaHttpResponse(), **e.path_parameters)
    return wrapped
