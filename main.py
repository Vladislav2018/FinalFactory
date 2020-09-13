from datawriter import *
from vacantions import *
from typing import *
from city import *
import sqlite3 as sl3
from csv_to_sqlite import *
from manufacturing import *

if __name__ == '__main__':

   db_path = '/home/mv/PycharmProjects/primitive/FinalFactory/db/datamanufacturing.db'
   connection = sl3.connect(db_path)
   create_products_table = """
CREATE TABLE IF NOT EXISTS products (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
                                    name text NOT NULL,
  									mass real NOT NULL,
  									version integer NOT NULL DEFAULT 1,
  									cost real NOT NULL,
  									price real NOT NULL DEFAULT cost,
                                    priority integer NOT NULL,
                                    status_step text
  									NOT NULL CHECK (status_step IN 
										   ('hyp', 'dev', 'prot', 'test',
											'rev', 'prer', 'mass', 'fre',
											'clos')) DEFAULT 'hyp',
  									made integer NOT NULL DEFAULT 0,
  									realised integer NOT NULL DEFAULT 0,
  									defective integer NOT NULL DEFAULT 0,
  									retured integer NOT NULL DEFAULT 0
);
   """
   create_staff_table = """
   CREATE TABLE IF NOT EXISTS staff (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
  									global_place TEXT NOT NULL CHECK (
                                      global_place IN (
                                        'factory', 'store', 'transport', 'office'
                                      )),
  									place_id INTEGER NOT NULL,
                                    salary INTEGER NOT NULL,
  									position TEXT NOT NULL,
  									hired_now INTEGER NOT NULL CHECK(hired_now IN (0,1))
  												DEFAULT 1,
  									common_work_duration INTEGER NOT NULL DEFAULT 0,
  									city_from INTEGER NOT NULL	
);
   """
   create_equipment_table = """
   CREATE TABLE IF NOT EXISTS factory_equipment (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
  									etype TEXT NOT NULL,
                                    current_cost INTEGER NOT NULL,
  									deprecation REAL NOT NULL DEFAULT 0,
  									common_work_duration INTEGER NOT NULL DEFAULT 0,
  									danger_level INTEGER NOT NULL CHECK(danger_level < 4),
  									defect_infuence INTEGER NOT NULL CHECK(defect_infuence IN (0,1))
);
   """
   create_transport_table = """
   CREATE TABLE IF NOT EXISTS transport (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
                                    current_cost INTEGER NOT NULL,
  									capacity INTEGER NOT NULL,
  									deprecation REAL NOT NULL DEFAULT 0,
  									mileage INTEGER NOT NULL DEFAULT 0,
  									fuel_consumption real NOT NULL,
  									fuel_type TEXT NOT NULL CHECK(
                                      fuel_type IN ('p', 'd', 'e', 'g')
                                                                 ),
  									fuel_capacity REAL NOT NULL,
  							broken INTEGER NOT NULL CHECK(broken IN (0,1)) DEFAULT 0
);
   """
   create_product_staff_table = """
CREATE TABLE IF NOT EXISTS products_staff (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
                                    staff_id INTEGER NOT NULL,
  									product_id INTEGER NOT NULL,
  									action_type TEXT NOT NULL CHECK( action_type in
                                      ('invent', 'develop', 'manage', 
                                       'test', 'reviev', 'craft',
                                      'transport', 'sale')
                                    ),
  									action_time INTEGER NOT NULL DEFAULT 0,
  									FOREIGN KEY (staff_id) REFERENCES staff(id),
  									FOREIGN KEY (product_id) REFERENCES products(id)
);
   """
   create_equipment_staff_table = """
   CREATE TABLE IF NOT EXISTS factoryequipment_staff (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
                                    staff_id INTEGER NOT NULL,
  									equipment_id INTEGER NOT NULL,
  									action_type TEXT NOT NULL CHECK( action_type in
                                      ('buy', 'check', 'manage', 'work')
                                    ),
  									action_time INTEGER NOT NULL DEFAULT 0,
  									FOREIGN KEY (staff_id) REFERENCES staff(id),
  									FOREIGN KEY (equipment_id) REFERENCES factory_equipment(id)
);
   """
   create_transport_table
   connection.executescript()
   connection.close()

'''
 cities = []
 for i in range(50):
     city = City(60)
     cities.append(city)
 cities_writer(cities)
'''




