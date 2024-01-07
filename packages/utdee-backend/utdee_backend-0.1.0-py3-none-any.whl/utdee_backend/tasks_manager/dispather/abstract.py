from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

# TODO: circular import
# from utdee_backend.tasks_manager.factory import AbstractTasksFactory
from utdee_backend.tasks_manager.task.abstract import AbstractTask
from utdee_backend.utils.context_manager import ContextManager


def run_task_exception_handler(*pargs, **pkwargs):
    def wrapper(run_task):
        async def run_task_wrapper(
                task_dispather: AbstractTasksDispatcher,
                task: AbstractTask, *args, **kwargs
        ):
            run_result = TaskDispatcherRunResult(task)
            task_dispather.run_result.append(run_result)
            try:
                return await run_task(task_dispather, task, *args, **kwargs)
            except Exception as e:
                run_result.exception = e
        return run_task_wrapper
    return wrapper


class TaskDispatcherRunResult:

    def __init__(self, task):
        self.task = task
        self.exception = None


class AbstractTasksDispatcher(ABC, ContextManager):
    tasks_factory: "AbstractTasksFactory"

    def __init__(self):
        self.run_result: List[TaskDispatcherRunResult] = []

    @abstractmethod
    # @run_task_exception_handler()  # TODO: cause exception: "coroutines cannot be used with run_in_executor"
    async def run_task(self, task: AbstractTask):
        pass
