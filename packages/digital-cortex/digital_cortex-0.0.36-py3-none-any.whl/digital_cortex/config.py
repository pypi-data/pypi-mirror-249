import os


class Config:
    HOST_URL = os.getenv("HOST_URL", 'http://localhost:9999')


config = Config()
