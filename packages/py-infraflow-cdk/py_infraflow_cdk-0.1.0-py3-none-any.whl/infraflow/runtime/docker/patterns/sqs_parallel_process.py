import os
import time
import asyncio
from typing import Any, Callable

import boto3

from infraflow.runtime.docker.contracts.sqs import SqsBotoMessageRecord, SqsBotoResult

MAX_MESSAGES = 50


async def process_messages(processor: callable):
    queue_name = os.environ["SQS_QUEUE"]
    sqs = boto3.resource("sqs")
    queue = sqs.get_queue_by_name(QueueName=queue_name)

    class RunData:
        in_progress_count = 0

    async def process_message(message: SqsBotoMessageRecord):
        try:
            await processor(message=message)
        except Exception as e:
            # TODO: Log
            pass
        finally:
            RunData.in_progress_count -= 1

    while True:
        result: SqsBotoResult = queue.receive_messages(
            MaxNumberOfMessages=MAX_MESSAGES - RunData.in_progress_count,
            WaitTimeSeconds=1
        )
        RunData.in_progress_count += len(result.messages)
        for m in result.messages:
             process_message(m)

        await asyncio.sleep(0.2)

