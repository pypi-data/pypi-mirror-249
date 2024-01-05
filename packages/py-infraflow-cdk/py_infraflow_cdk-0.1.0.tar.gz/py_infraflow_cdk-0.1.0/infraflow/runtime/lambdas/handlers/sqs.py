from typing import TypeVar, Type, Callable, Union, Any

from pydantic import BaseModel

from infraflow.runtime.lambdas.events.sqs import SqsLambdaMessageRecord, SqsLambdaEvent

TSqsMessage = TypeVar('TSqsMessage')


class SqsProcessor:
    def handle_error(self, message: SqsLambdaMessageRecord, error):
        pass

    def after_each(self, message: SqsLambdaMessageRecord, result):
        pass

    def after_all(self, messages: list[SqsLambdaMessageRecord], results):
        pass

    def handler(self, SqsMessageData: Type[TSqsMessage]):
        def typed(func: Callable[
                [TSqsMessage, SqsLambdaMessageRecord],
                Union[dict, BaseModel, list[dict], list[str], list[str], list[BaseModel], list[int], list[float], list[bool]],
            ]):
            def wrapped(event, context):
                e = SqsLambdaEvent(**event)
                results = []
                for m in e.records:
                    try:
                        result = func(SqsMessageData(m.data), m)
                        self.after_each(m, result)
                        results.append(m)
                    except Any as e:
                        self.handle_error(e)

                self.after_all(e.messages, results)
                return results
            return wrapped
        return typed
