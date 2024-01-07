from bottle import get

from utdee_backend.tasks_manager import thread_pool_list_of_get_call_tasks, GetCallTask
from utdee_backend.utils.trace import otel_trace


urls = (
    "https://www.yr.no/api/v0/locations/2-7531926/forecast",
    "https://www.yr.no/api/v0/locations/2-7531926/celestialeventsmultipledays",
    "https://www.yr.no/api/v0/locations/2-7531926/forecast/currenthour",
)


@get("/thread_task")
@otel_trace
def thread_task():
    list_of_tasks = [GetCallTask(u) for u in urls] * 10
    thread_pool_list_of_get_call_tasks(list_of_tasks=list_of_tasks)
    result = ("\n"*3).join(
        f"{t.url}\n{t.result.text}" for t in list_of_tasks
    )
    return f"<html><pre>{result}</pre></html>"
