from typing import Any, Union
from typing import TypeVar, Generic

from infraflow.util import caps_camel

T = TypeVar('T')

from aws_cdk import aws_sqs as sqs
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subscriptions
from aws_cdk import aws_events as events
from aws_cdk import aws_lambda as lambdas
from aws_cdk import aws_events_targets as targets

from infraflow.cdk.lambdas import QueueFunctionConstruct
from infraflow.cdk.core.service_stage import ServiceStageStack


class Event:
    def __init__(self, stage: ServiceStageStack, bus_id: str, event_key: str):
        self.stage = stage
        self.event_key = event_key
        self.priority = None
        self.filters: list[dict] = []
        self.bus_id = bus_id

    def express_only(self):
        self.add_filter({
            "express": True
        })
        self.priority = "express"
        return self

    def non_express(self):
        self.add_filter({
            "express": False
        })
        self.priority = "default"
        return self

    def with_priority(self, priority: int):
        self.add_filter({
            "priority": priority
        })
        self.priority = f"priority_{priority}"
        return self

    def with_priorities(self, start: int, stop: int):
        self.add_filter({
            "priority": [start, stop]
        })
        self.priority = f"priority_{start}_{stop}"
        return self

    def with_prop(self, key: str):
        self.add_filter({
            key: True
        })
        return self

    def with_true_prop(self, key: str):
        self.add_filter({
            key: True
        })
        return self

    def with_prop_equal(self, key: str, value: Any):
        self.add_filter({
            key: value
        })
        return self

    def add_filter(self, filter: dict):
        self.filters.append(filter)

    @property
    def suffix(self):
        return self.priority

    def subscribe(self, *processors: Union[lambdas.Function, QueueFunctionConstruct, sqs.Queue]):
        subs = []
        for processor in processors:
            if isinstance(processor, QueueFunctionConstruct):
                queue, lam, sub = processor.queue, processor.function, processor.queue
            elif isinstance(processor, sqs.Queue):
                queue, lam, sub = processor, None, processor
            elif isinstance(processor, lambdas.Function):
                queue, lam, sub = None, processor, processor
            else:
                raise TypeError()
            subs.append(sub)
        self._subscribe(*subs)

    @property
    def id(self):
        def filter_name(f: dict):
            def prop_name(k, v):
                return f"{caps_camel(k)}{caps_camel(v)}"

            return "".join(prop_name(k, v) for k, v in f.items())

        filters_string = ''.join([filter_name(f) for f in self.filters])
        return f"{caps_camel(self.bus_id)}{caps_camel(self.event_key)}{filters_string}"

    def _subscribe(self, *subscribers: Union[sqs.Queue, lambdas.Function]):
        pass


class SnsEvent(Event):
    def __init__(self, stage: ServiceStageStack, bus_id: str, event_key: str, bus: sns.ITopic):
        super().__init__(stage, bus_id, event_key)
        self.bus = bus
        self.filters = []

    def _subscribe(self, *subscribers: Union[sqs.Queue, lambdas.Function]):
        for queue in subscribers:
            self.bus.add_subscription(self.get_sns_sqs_subscription(queue))

    def get_sns_sqs_subscription(self, subscriber: Union[sqs.Queue, lambdas.Function]):
        if isinstance(subscriber, sqs.Queue):
            return subscriptions.SqsSubscription(subscriber, filter_policy=self.filter_policy)
        elif isinstance(subscriber, lambdas.Function):
            return subscriptions.LambdaSubscription(subscriber, filter_policy=self.filter_policy)
        else:
            raise TypeError()

    @property
    def filter_policy(self):
        return


class EventBridgeEvent(Event):
    def __init__(self, stage: ServiceStageStack, bus_id: str, event_key: str, bus: events.IEventBus):
        super().__init__(stage, bus_id, event_key)
        self.bus = bus
        self.filters = []

    def _subscribe(self, *subscribers: Union[sqs.Queue, lambdas.Function]):
        targets_ = [get_eb_target(subscriber) for subscriber in subscribers]
        return events.Rule(self.stage, self.id, event_bus=self.bus, targets=targets_, event_pattern={
            "detail": {

            }
        })


def get_eb_target(subscriber: Union[sqs.Queue, lambdas.Function]):
    if isinstance(subscriber, sqs.Queue):
        target = targets.SqsQueue(subscriber)
    elif isinstance(subscriber, lambdas.Function):
        target = targets.LambdaFunction(subscriber)
    else:
        raise TypeError()
    return target


class InfraflowEventBus(Generic[T]):
    def __init__(self, stage: ServiceStageStack, bus_id, bus: T):
        self.bus = bus
        self.bus_id = bus_id
        self.stage = stage

    def event(self, event_key: str) -> Event:
        pass


class EventBridgeEventBus(InfraflowEventBus[events.IEventBus]):
    def __init__(self, stage: ServiceStageStack, bus_id, bus: events.IEventBus):
        super().__init__(stage, bus_id, bus)

    def event(self, event_key: str) -> Event:
        return EventBridgeEvent(self.stage, self.bus_id, event_key, self.bus)


class SnsEventBus(InfraflowEventBus[sns.ITopic]):
    def __init__(self, stage: ServiceStageStack, bus_id, bus: sns.ITopic):
        super().__init__(stage, bus_id, bus)

    def event(self, event_key: str) -> Event:
        return SnsEvent(self.stage, self.bus_id, event_key, self.bus)

# selection_bus = EventBus()
#
# selection_bus.event('ready').with_true_prop('amplify').express_only().subscribe(
#     context=LambdaContext(...),
#     handler=handle_amplify_selection,
#     suffix='express',
#     queued=True
# )
