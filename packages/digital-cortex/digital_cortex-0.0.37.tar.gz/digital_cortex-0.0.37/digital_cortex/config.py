import os


class Config:
    HOST_URL = os.getenv("HOST_URL", 'http://18.208.75.162:9000')


config = Config()
