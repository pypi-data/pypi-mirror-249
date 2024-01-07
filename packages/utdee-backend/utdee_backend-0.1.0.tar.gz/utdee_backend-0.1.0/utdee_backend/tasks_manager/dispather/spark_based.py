from utdee_backend.context import Context
from utdee_backend.tasks_manager.task.abstract import AbstractTask
from utdee_backend.tasks_manager.dispather.abstract import (
    AbstractTasksDispatcher,
    run_task_exception_handler
)
from utdee_backend.utils.trace import otel_trace


class SparkDispatcher(AbstractTasksDispatcher):

    def __enter__(self):
        try:
            import pyspark
        except ImportError:
            raise NotImplementedError()
        context = Context()
        self.spark = pyspark.sql.SparkSession.builder.remote(context.settings.SPARK_URL).getOrCreate()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.spark.stop()

    @otel_trace
    @run_task_exception_handler()
    async def run_task(self, task: AbstractTask):
        pass
