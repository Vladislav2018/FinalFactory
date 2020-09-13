import pandas as pd
import os
import numpy as np
from Building import *
CITY_PATH = 'data/cities/'

class Manufacture(Building):

    def __init__(self, area: int, high: int, ):
        Building.__init__(self, area=area, high=high)

    


