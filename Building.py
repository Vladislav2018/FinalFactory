import pandas as pd
import os
import numpy as np

CITY_PATH = 'data/cities/'
OBJECT = 'City_'
FORMAT = '.csv'

#Todo: chunk loading and handilng
class Building():
    def __init__(self, area: int, high: int, city_id: str = ''):
        try:
            self.city_data = pd.read_csv(CITY_PATH + 'City_' + city_id + '.csv')
            '''
            ToDo: to give a choice to user: if free places is absent there, you can build
            store near the city. It will take more resources and probably less sales but would
            be profitable in some cases
            '''
        except FileNotFoundError:
            all_cities = os.listdir(CITY_PATH)
            if('City' in all_cities):
                city = np.random.choice(all_cities)
                self.city_data = pd.read_csv(CITY_PATH + city)
            else:
                raise ('The folder has not cities')
            self.area = area
            self.high = high