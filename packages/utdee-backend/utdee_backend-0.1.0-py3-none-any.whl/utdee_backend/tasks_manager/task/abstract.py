from __future__ import annotations

from abc import ABC, abstractmethod


def run_exception_handler(*pargs, **pkwargs):
    def wrapper(run):
        def run_wrapper(task: AbstractTask, *args, **kwargs):
            try:
                return run(task, *args, **kwargs)
            except Exception as e:
                task.error = e
                raise e
        return run_wrapper
    return wrapper


class AbstractTask(ABC):

    def __init__(self, *args, **kwargs):
        self.result = None
        self.error = None

    @abstractmethod
    @run_exception_handler()
    def run(self):
        pass
