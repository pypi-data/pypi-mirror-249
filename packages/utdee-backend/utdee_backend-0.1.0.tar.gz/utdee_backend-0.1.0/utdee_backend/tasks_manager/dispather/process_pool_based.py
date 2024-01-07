from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor

from utdee_backend.tasks_manager.task.abstract import AbstractTask
from utdee_backend.tasks_manager.dispather.abstract import (
    AbstractTasksDispatcher,
    run_task_exception_handler
)
from utdee_backend.utils.trace import otel_trace


class ProcessPoolTasksDispatcher(AbstractTasksDispatcher):

    def __enter__(self):
        self.executor = ProcessPoolExecutor(
            max_workers=10,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.executor.shutdown()

    @otel_trace
    @run_task_exception_handler()
    def run_task(self, task: AbstractTask):
        self.executor.submit(task.run)
