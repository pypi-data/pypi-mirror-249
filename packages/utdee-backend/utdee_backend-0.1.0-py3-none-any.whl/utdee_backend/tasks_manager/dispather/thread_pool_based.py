import asyncio
from concurrent.futures import ThreadPoolExecutor

from utdee_backend.tasks_manager.task.abstract import AbstractTask
from utdee_backend.tasks_manager.dispather.abstract import (
    AbstractTasksDispatcher,
    run_task_exception_handler
)
from utdee_backend.utils.trace import otel_trace


class ThreadPoolTasksDispatcher(AbstractTasksDispatcher):

    def __init__(self, max_workers: int = 5):
        super().__init__()
        self.max_workers = max_workers

    def __enter__(self):
        self.executor = ThreadPoolExecutor(
            max_workers=self.max_workers,
            thread_name_prefix=self.__class__.__name__,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.executor.shutdown()

    @otel_trace
    @run_task_exception_handler()
    async def run_task(self, task: AbstractTask):
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(self.executor, task.run)
        task.result = result
