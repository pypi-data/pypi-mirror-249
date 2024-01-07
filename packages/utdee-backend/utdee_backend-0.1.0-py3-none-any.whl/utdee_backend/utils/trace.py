from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer, set_tracer_provider, Tracer

from utdee_backend.context import Context


def setup_otel_tracer() -> Tracer:
    provider = TracerProvider()
    exporter = OTLPSpanExporter()
    exporter.max_backoff_seconds = 5

    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)
    set_tracer_provider(provider)

    # TODO: unhardcode name
    tracer = get_tracer("utdee_backend")
    return tracer


def otel_trace(func):

    def wrapper(*args, **kwargs):
        with Context().tracer.start_as_current_span(f"running {func.__name__}"):
            result = func(*args, **kwargs)
        return result

    return wrapper
