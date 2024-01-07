from opentelemetry.trace import Tracer

from utdee_backend.utils.singleton import Singleton
from utdee_backend.context.settings import Settings


class Context(metaclass=Singleton):
    settings: Settings
    tracer: Tracer

    def __init__(self):
        self.settings = Settings()
