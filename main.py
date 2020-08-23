from datawriter import *
from vacantions import *
from typing import *
from city import *
import sqlite3 as sl3
from csv_to_sqlite import *

if __name__ == '__main__':
    db_path = ''
    connection = sl3.connect(db_path)

    connection.close()
    cities = []
    for i in range(50):
        city = City(60)
        cities.append(city)
    cities_writer(cities)

