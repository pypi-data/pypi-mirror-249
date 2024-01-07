import requests
from requests.models import Response

from utdee_backend.tasks_manager.task.abstract import AbstractTask, run_exception_handler


class GetCallTask(AbstractTask):
    result: Response = None

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    @run_exception_handler()
    def run(self):
        import sys
        from threading import current_thread
        from time import sleep
        sleep(1)
        print(self.url, current_thread().ident, sys.thread_info)
        response = requests.get(self.url, timeout=5)
        response.raise_for_status()
        return response
