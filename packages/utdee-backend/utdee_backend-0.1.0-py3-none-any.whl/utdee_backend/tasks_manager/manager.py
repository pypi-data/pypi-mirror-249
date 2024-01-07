from abc import ABC, abstractmethod

from utdee_backend.tasks_manager.factory.abstract import AbstractTasksFactory
from utdee_backend.tasks_manager.dispather.abstract import AbstractTasksDispatcher


class AbstractTasksManager(ABC):

    def __init__(
            self,
            factory: AbstractTasksFactory,
            dispatcher: AbstractTasksDispatcher
    ):
        self.factory = factory
        self.dispatcher = dispatcher

        self.factory.dispatcher = dispatcher
        self.dispatcher.tasks_factory = factory

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TasksManager(AbstractTasksManager):

    def run(self):
        self.factory.start()

    def __enter__(self):
        self.factory.__enter__()
        self.dispatcher.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.factory.__exit__(exc_type, exc_val, exc_tb)
        self.dispatcher.__exit__(exc_type, exc_val, exc_tb)
