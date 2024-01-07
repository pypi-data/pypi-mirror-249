from typing import List

from utdee_backend import otel_trace
from utdee_backend.tasks_manager.task import GetCallTask
from utdee_backend.tasks_manager.manager import TasksManager
from utdee_backend.tasks_manager.factory import ListOfTasksFactory
from utdee_backend.tasks_manager.dispather import (
    ThreadPoolTasksDispatcher, ProcessPoolTasksDispatcher, SparkDispatcher,
)


@otel_trace
def thread_pool_list_of_get_call_tasks(list_of_tasks: List[GetCallTask]):
    factory = ListOfTasksFactory(list_of_tasks=list_of_tasks)
    dispatcher = ThreadPoolTasksDispatcher()
    with TasksManager(
        factory=factory,
        dispatcher=dispatcher,
    ) as manager:
        manager.run()

        # TODO: check runtime exceptions there


@otel_trace
def process_pool_list_of_get_call_tasks(list_of_tasks: List[GetCallTask]):
    factory = ListOfTasksFactory(list_of_tasks=list_of_tasks)
    dispatcher = ProcessPoolTasksDispatcher()
    with TasksManager(
        factory=factory,
        dispatcher=dispatcher,
    ) as manager:
        manager.run()


@otel_trace
def spark_list_of_get_call_tasks(list_of_tasks: List[GetCallTask]):
    factory = ListOfTasksFactory(list_of_tasks=list_of_tasks)
    dispatcher = SparkDispatcher()
    with TasksManager(
        factory=factory,
        dispatcher=dispatcher,
    ) as manager:
        manager.run()
