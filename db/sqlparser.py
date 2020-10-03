import sqlite3 as sq
from db.dbmanager import DataBase

def write_log(row_data, path_to_db: str = "db/logs.db"):
    log_con = DataBase(path_to_db)
    pass

def pasreSQL(query: str):
    pass