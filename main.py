from datawriter import *
from vacantions import *
from typing import *
from city import *
import sqlite3 as sl3
from db.dbmanager import DataBase
from product import Product

from manufacturing import *

if __name__ == '__main__':


   db_path = 'db/data.db'
   logs_path = 'db/logs.db'

   create_products_table = """
CREATE TABLE IF NOT EXISTS products (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
                                    name text NOT NULL,
  									mass real NOT NULL,
  									volume real NOT NULL,
  									type TEXT NOT NULL,
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
                                    uuid TEXT NOT NULL,
  									place_id INTEGER NOT NULL,
                                    salary INTEGER NOT NULL,
  									position TEXT NOT NULL,
  									hired_now INTEGER NOT NULL CHECK(hired_now IN (0,1))
  												DEFAULT 1,
  									common_work_duration INTEGER NOT NULL DEFAULT 0,
  									city_from INTEGER NOT NULL,	
  									sex TEXT NOT NULL CHECK (sex IN ('M', 'N'))
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
     									ttype TEXT NOT NULL,
     									fuel_type TEXT NOT NULL 
     									check (fuel_type in 
     									("petrol", "gas", "diesel", "electricity")
     									),
     									model TEXT NOT NULL,
     									firm TEXT NOT NULL,
     									capacity REAL NOT NULL,
     									max_mass INTEGER NOT NULL,
     									max_speed INTEGER NOT NULL,
     									fuel_capacity INTEGER NOT NULL,
     									fuel_consumption REAL NOT NULL,
                                       current_cost INTEGER NOT NULL,
     									deprecation REAL NOT NULL DEFAULT 0,
     									common_work_duration INTEGER NOT NULL DEFAULT 0,
     									repairs INTEGER NOT NULL DEFAULT 0,
     									avg_fepairs_price INTEGER NOT NULL DEFAULT 0,
     									mileage REAL NOT NULL DEFAULT 0
   );
      """
   create_products_staff_table = """
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
   create_transport_staff_table = """
   CREATE TABLE IF NOT EXISTS transport_staff (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
                                    staff_id INTEGER NOT NULL,
  									transport_id INTEGER NOT NULL,
  									action_type TEXT NOT NULL CHECK( action_type in
                                      ('buy', 'check', 'manage', 'drive')
                                    ),
  									action_time INTEGER NOT NULL DEFAULT 0,
  									FOREIGN KEY (staff_id) REFERENCES staff(id),
  									FOREIGN KEY (transport_id) REFERENCES transport(id)
)
   """
   create_candidates_table = """
      CREATE TABLE IF NOT EXISTS candidates (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
                                    pretend_salary INTEGER NOT NULL,
                                    uuid TEXT NOT NULL,
  									pretend_position TEXT NOT NULL,
									expierence_prpos INTEGER NOT NULL, 
  									city_from INTEGER NOT NULL,
  									smoking INTEGER NOT NULL CHECK (smoking IN (0,1)),
  									hadrskills_test INTEGER,
  									softskills INTEGER,
  									sex TEXT NOT NULL CHECK (sex IN ("M", "N"))
);
   """
   create_factories_table = """
   CREATE TABLE IF NOT EXISTS factories (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
     								count_of_equipment INTEGER NOT NULL DEFAULT 0,
     								count_of_employee INTEGER NOT NULL DEFAULT 0,
                                    products_made INTEGER NOT NULL DEFAULT 0,
                                    products_realised INTEGER NOT NULL DEFAULT 0,
                                    products_returned INTEGER NOT NULL DEFAULT 0,
                                    defective INTEGER NOT NULL DEFAULT 0,
                                    cost_in_a_day INTEGER NOT NULL DEFAULT 0,
                                    opening_cost INTEGER NOT NULL DEFAULT 0,
                                    profit INTEGER NOT NULL DEFAULT 0
   );
   """
   create_stores_table = """
   CREATE TABLE IF NOT EXISTS stores (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
     								count_of_employee INTEGER NOT NULL DEFAULT 0,
                                    products_realised INTEGER NOT NULL DEFAULT 0,
                                    products_returned INTEGER NOT NULL DEFAULT 0,
                                    cost_in_a_day INTEGER NOT NULL DEFAULT 0,
                                    opening_cost INTEGER NOT NULL DEFAULT 0,
                                    all_visits INTEGER NOT NULL DEFAULT 0,
                                    unique_visits INTEGER NOT NULL DEFAULT 0,
                                    work_hours INTEGER NOT NULL DEFAULT 0,
                                    profit INTEGER NOT NULL DEFAULT 0
   );
   """
   create_stores_products = """
   CREATE TABLE IF NOT EXISTS stores_products (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
                                    product_id INTEGER NOT NULL,
                                    store_id INTEGER NOT NULL,
                                    products_count INTEGER NOT NULL,
  									FOREIGN KEY (product_id) REFERENCES products(id),
  									FOREIGN KEY (store_id) REFERENCES stores(id)
);
   """
   create_factories_products = """
      CREATE TABLE IF NOT EXISTS factories_products (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
                                    product_id INTEGER NOT NULL,
                                    factory_id INTEGER NOT NULL,
  									FOREIGN KEY (product_id) REFERENCES products(id),
  									FOREIGN KEY (factory_id) REFERENCES factories(id)
);
   """
   create_staff_factories = """
      CREATE TABLE IF NOT EXISTS staff_factories (
                                    id integer PRIMARY KEY UNIQUE NOT NULL,
  									employee_id INTEGER NOT NULL,
                                    factory_id INTEGER NOT NULL,
                                    action_type TEXT NOT NULL CHECK (action_type IN ("work", "manage", "check")),
  									FOREIGN KEY (employee_id) REFERENCES staff(id),
  									FOREIGN KEY (factory_id) REFERENCES factories(id)
);
   """
   create_staff_stores = """
         CREATE TABLE IF NOT EXISTS staff_stores (
                                        id integer PRIMARY KEY UNIQUE NOT NULL,
     									employee_id INTEGER NOT NULL,
                                        store_id INTEGER NOT NULL,
                                        action_type TEXT NOT NULL CHECK (action_type IN ("work", "manage", "check")),
     									FOREIGN KEY (employee_id) REFERENCES staff(id),
     									FOREIGN KEY (store_id) REFERENCES stores(id)
   );
      """
   modify_staff_table = """
   ALTER TABLE staff
   ADD COLUMN ownership REAL DEFAULT 0
   """
   logger_table = """
      CREATE TABLE IF NOT EXISTS logs (
                                       id integer PRIMARY KEY UNIQUE NOT NULL,
                                       table_name TEXT NOT NULL,
     									way_action TEXT NOT NULL check (way_action in ('insertion', 'deleting', 'changing')),
     									last_val TEXT,
     									new_val TEXT
     									);
      """

   print()

   logger = DataBase(logs_path)
   pr1 = Product()
   #logger.db_connection.executescript()

'''
 cities = []
 for i in range(50):
     city = City(60)
     cities.append(city)
 cities_writer(cities)
'''




