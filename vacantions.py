from random import *
from math import *
from datawriter import *
from typing import *
from pandas import read_csv
import pandas as pd
import numpy as np

vacations = read_csv('data/base_vacantions_info.csv')
#it's need to upload the hired employee

class Vacantion(object):

    def __init__(self, period: int):
        self.period = period
        self.data = vacations['vacantion']

    def calc_count_of_submissive_employee(self, min_hiearhy_level: float) -> int:
        #test variant, it must depends from other data
        return round(randrange(0, min_hiearhy_level)**randint(1,10))
    
    def calc_bonus_expected_value(self, min_hiearhy_level: float, vacantion: str) -> int:
        #ToDo: make harder dependency
        if vacantion == "sales_manager":
            return randint(0, 100)/randint(22, 22+ randint(1,9))
        else:
            return randint(0, min_hiearhy_level**randint(1,10))/randint(22, 22 + randint(1, 9))

    def calc_fine_expected_value(self, min_hiearhy_level: float, vacantion: str) -> int:
        if vacantion == "sales_manager":
            return randint(0, 100)/randint(22, 22+ randint(1,9))
        else:
            return randint(0, min_hiearhy_level)/randint(22, 22 + randint(1, 9))

    def calc_current_salary_per_day(self, standart_salary_per_day: int,
                                     count_of_submissive_employee: int, bonus_expected_value: int,
                                     fine_expected_value: int, min_hiearhy_level: float)-> float:
        return (standart_salary_per_day + pow(count_of_submissive_employee,1/2)*0.001 +
                randint(1,10)*0.1 + bonus_expected_value/randint(22,22+min_hiearhy_level) -
                fine_expected_value/randint(22,22+min_hiearhy_level))

    def calc_staff_turnover_per_month(self, min_hiearhy_level: float, current_salary_per_day: int) -> int:
        return round(1/(min_hiearhy_level+1)**2 + 1/current_salary_per_day + randint(1,10)*0.1)

    #Todo: make dependency from the external data
    def calc_count_of_free_positions(self, min_hiearhy_level: float,
                                     current_salary_per_day: float) -> int:
        return round((randint(0,100)**(1/(min_hiearhy_level+1))/current_salary_per_day))

    def calc_count_of_employee(self, vacantion: str, min_hiearhy_level: float) -> int:
        if(vacantion == 'CEO'): return 1
        else:
        #test variant, it must depends from other data
            return round(randint(1, 20)//(min_hiearhy_level+1))

    def calc_competition_per_month(self, min_hiearhy_level: float, standart_salary_per_day: int,
                                   current_salary_per_day: float, staff_turnover_per_month: int) -> int:
        koef = (standart_salary_per_day - current_salary_per_day)*0.1 + \
               min_hiearhy_level + 1/(staff_turnover_per_month+1)
        return round(koef)

    def calc_avg_work_time_in_hours(self, competition_per_month: int, current_salary_per_day: float) -> int:
        return randint(1,10)**2 + competition_per_month + round(current_salary_per_day)

