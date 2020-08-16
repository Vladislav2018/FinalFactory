import pandas as pd
from typing import *
import csv

DAYS_IN_MONTH: Tuple[int, ...] = (31, 28, 31, 30, 31, 30, 31, 31, 30, 30, 31, 30, 31)
func_prefixes: Tuple[str, ...] = ('calc_', 'gen', 'write')
CSV_FORMAT: Final[str] = '.csv'

def genFilename_from_method(func_name: str, curr_month: int) -> str:
    """
    This function generate name for file,
    that based on name of the given function
    without prefix in global tuple of the possible prefixes.
    :param func_name: str
    :param curr_month: int
    :return: str
    """
    filename= ''
    for prefix in func_prefixes:
        if prefix in func_name:
            filename = func_name[len(prefix):]
    return filename + str(curr_month)+ CSV_FORMAT

def genFilename_from_class(obj: object):
    return obj.__class__.__name__ + '_' + str(id(obj)) + CSV_FORMAT


def call_counter(func):
    """
    Decorator that counts number of function calls
    :param func: callable
    :return: callable
    """
    #that method uses like an object
    def helper(*args, **kwargs):
        helper.calls += 1
        return func(*args, **kwargs)
    helper.calls = 0
    helper.__name__= func.__name__

    return helper

#todo: think about usage with another type of the data (probably, it needs to reset count of callls)
@call_counter
def get_month(call_count: int, list_len: int) -> int:
    """
    This function depends on the decorator,
    that counts numbers of calls of this function.
    The second argument is the length of the job list,
    or an another data, that must be initialised for each month not separately.
    :param call_count: int (gets from call_counter)
    :param list_len: int
    :return: int ("current" month)
    """
    month = (call_count // list_len) + 1
    return month

#Todo: write naming rules in the documentation
def get_value_from_obj(key_name : str, obj: object, *args, method_prefix: str = 'calc_') -> Any:
    """
    This function calls method by name (from given string).
    According to the recommendations, method has name the same
     key_name, with any prefix (default =  'calc_')
    :param key_name: str
    :param obj: custom class object
    :param args: method input arguments
    :param method_prefix: str
    :return: Any
    """
    if hasattr(obj, method_prefix + key_name) == True:
        return getattr(obj, method_prefix + key_name)(*args)
    else:
        raise Exception('Attribute is undefined')

def cities_writer(cities):
    for city in cities:
        filename: str = genFilename_from_class(city)
        period: int = city.__getattribute__('period')
        dist: int = city.__getattribute__('dist_to_the_nearest_factory')
        with open('data/'+filename, 'a', newline='') as csvfile:
                fieldnames = [
                    'month_ago', 'dist_to_the_nearest_factory',
                    'population', 'gdp_per_capita', 'competition'
                              ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                start_population = None
                start_gdp = None
                start_competition = None
                while period > 0:
                    population = get_value_from_obj('population', city, start_population)
                    start_population = population
                    gdp_per_capita = get_value_from_obj('gdp_per_capita', city, population, start_gdp)
                    start_gdp = gdp_per_capita
                    competition = get_value_from_obj('competition', city, population, gdp_per_capita, start_competition)
                    start_competition = competition

                    row = {'month_ago': period, 'dist_to_the_nearest_factory': dist,
                           'population':population, 'gdp_per_capita': gdp_per_capita,
                           'competition': competition}
                    writer.writerow(row)
                    period -= 1
                    city.__setattr__('period', period)


