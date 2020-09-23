import sqlite3
import logging as log
from typing import *
import inspect

class MetaDataBase(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DataBase(metaclass=MetaDataBase):
    def __init__(self, path: str):
        log.basicConfig(level=log.DEBUG)
        self.db_connection = sqlite3.connect(path)
        self.connection_path = path
        log.info("Connected to db in: " + path + " from " + str(inspect.stack(context=1)))

    def __del__(self):
        log.info("Connection to " + self.connection_path + " was closed")
        self.db_connection.close()