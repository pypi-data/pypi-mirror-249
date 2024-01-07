import os


class Settings:
    def __init__(self):
        self.PORT = int(os.getenv("PORT"))

        self.MONGO_URI = os.getenv("MONGO_URI")
        self.MONGO_TEST_DB = os.getenv("MONGO_TEST_DB")
        self.MONGO_TEST_USER = os.getenv("MONGO_TEST_USER")
        self.MONGO_TEST_USER_PASSWORD = os.getenv("MONGO_TEST_USER_PASSWORD")
        self.GUNICORN_CERT = os.getenv("GUNICORN_CERT")
        self.GUNICORN_KEY = os.getenv("GUNICORN_KEY")
        self.SPARK_URL = os.getenv("SPARK_URL")
