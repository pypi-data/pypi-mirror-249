from datetime import timedelta

from redis import StrictRedis


class TaskTracker:
    def __init__(self, redis: StrictRedis):
        self.redis = redis

    def batch(self, task_batch_key: str):
        return TaskBatch(task_batch_key, self.redis)


class TaskBatch:
    def __init__(self, task_batch_key: str, redis: StrictRedis):
        self.redis = redis
        self.task_batch_key = f"tasks_{task_batch_key}"

    def start_batch(self, task_count: int, timeout: timedelta = timedelta(days=1)):
        self.redis.set(self.task_batch_key, task_count, ex=timeout)

    def finish_task(self):
        return self.redis.decr(self.task_batch_key) == 0
