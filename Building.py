import pandas as pd
import os
import numpy as np

CITY_PATH = 'data/cities/'
OBJECT = 'City_'
FORMAT = '.csv'

#Todo: chunk loading and handilng
class Building():
    def __init__(self, city_id: str = ''):
        try:
            self.city_data = pd.read_csv(CITY_PATH + 'City_' + city_id + '.csv')
        except FileNotFoundError:
            all_cities = os.listdir(CITY_PATH)
            if('City' in all_cities):
                city = np.random.choice(all_cities)
                self.city_data = pd.read_csv(CITY_PATH + city)
            else:
                raise ('The folder has not cities')