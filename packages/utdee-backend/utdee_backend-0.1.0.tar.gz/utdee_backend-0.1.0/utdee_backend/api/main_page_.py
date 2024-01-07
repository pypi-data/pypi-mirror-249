from bottle import get

from utdee_backend.utils.trace import otel_trace


@get("/")
@otel_trace
def main_page():
    return "main_page"
