from __future__ import annotations

import asyncio
from typing import List

from utdee_backend.tasks_manager.task.abstract import AbstractTask
from utdee_backend.tasks_manager.factory.abstract import AbstractTasksFactory
from utdee_backend.utils.async_generator_descryptor import AsyncGeneratorDescriptor


class ListOfTasksFactory(AbstractTasksFactory):
    list_of_tasks = AsyncGeneratorDescriptor()

    def __init__(self, list_of_tasks: List[AbstractTask]):
        self.list_of_tasks = list_of_tasks

    async def _start(self):
        async with asyncio.TaskGroup() as tg:
            async for task in self.list_of_tasks:
                tg.create_task(self.dispatcher.run_task(task=task))
