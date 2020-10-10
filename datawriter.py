import pandas as pd
from typing import *
import os
import warnings
import numpy as np
import itertools as it

DAYS_IN_MONTH: Tuple[int, ...] = (31, 28, 31, 30, 31, 30, 31, 31, 30, 30, 31, 30, 31)
func_prefixes: Tuple[str, ...] = ('calc_', 'gen', 'write')
CSV_FORMAT: Final[str] = '.csv'
TXT_FORMAT: Final[str] = '.txt'
etypes_path = "data/equipment/etypes.csv"

def dict_from_csv(path:str, param1:str, param2:str):
    table = pd.read_csv(path)
    keys = list(table[param1].array)
    values = list(table[param2].array)
    out = dict(zip(keys,values))
    return out

def dicts_to_scv(path: str, dicts):
    pass

def dict_from_class_methods(object: object, is_callable: bool, *args, **kwargs):
    data_dict = {}
    if is_callable == True:
        all_attrs = dir(object)
        all_methods = [func for func in all_attrs
                       if callable(getattr(object, func))]
        method_list = [func for func in all_methods
                       if func.startswith("calc")]

        for method in method_list:
            retunings = getattr(object, method)(*args, **kwargs)
            d = {method: retunings}
            data_dict.update(d)
    else:
        attrs_list = [func for func in dir(object)
                        if not callable(getattr(object, func))
                        and not func.startswith("__")]

        for attr in attrs_list:
            retunings = getattr(object, attr)
            d = {attr: retunings}
            data_dict.update(d)
        return data_dict

def get_csv_essence(path: str, essence_name: str, essence_id: str , format: str = '.csv'):
    try:
        data = pd.read_csv(path + essence_name + '_' + essence_id + format)
        return data
    except FileNotFoundError:
        all_essences = os.listdir(path)
        if (data in all_essences):
            essence = np.random.choice(all_essences)
            essence_data = pd.read_csv(path + essence)
            return essence_data
        else:
            raise ('The folder has not essences')

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

def genFilename_from_class(obj: object, format = CSV_FORMAT):
    return obj.__class__.__name__ + '_' + str(id(obj)) + format


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


def cities_writer(cities, path = 'data/cities/before/'):
    city_number: int = 0
    for city in cities:
        filename = 'City_' + str(city_number) + CSV_FORMAT
        period: int = city.__getattribute__('period')
        dist: int = city.__getattribute__('dist_to_the_nearest_factory')
        start_population = None
        start_gdp = None
        start_competition = None
        start_places = None
        product = None
        col_names = ['population', 'gdp_per_capita', 'competition', 'possible_places']
        col_vals = []
        while period > 0:
            population = get_value_from_obj('population', city,
                                            start_population)
            start_population = population
            gdp_per_capita = get_value_from_obj('gdp_per_capita', city,
                                                population, start_gdp)
            start_gdp = gdp_per_capita
            competition = get_value_from_obj('competition', city,
                                             population, gdp_per_capita, start_competition, product)
            start_competition = competition
            places = get_value_from_obj('possible_places', city,
                                             population, gdp_per_capita, start_places, competition,)
            if (product is None) or (type(product) is not tuple):
                col_vals.append([population, gdp_per_capita, competition, places])
            elif type(product) is tuple:
                for prod in product:
                    col_names.append(prod)
                    col_vals.append([competition])
            period -= 1
            city.__setattr__('period', period)
        city_df = pd.DataFrame(col_vals)
        city_df.to_csv(path + filename, header= col_names)
        city_number += 1
        const_prefs = {'dist_to_the_nearest_factory: ': str(dist)}

        with open(path + 'const_info' + filename, 'a',) as const_info:
            const_info.write(str(const_prefs))

def gen_equipment_tables(etypes_path = etypes_path):
    abs_root_path = r'D:\FinalFactory\data\equipment'
    etypes_data = pd.read_csv(r'D:\FinalFactory\data\equipment\etypes.csv')
    etypes = list(etypes_data["etype"])
    esubtypes = list(etypes_data["esubtype"])
    for i in range(len(etypes)):
        path = abs_root_path +"\_"+ etypes[i] +"\_"+ esubtypes[i]
        os.makedirs(path)
        for param in ["common", "danger", "events", "other", "models"]:
            path = abs_root_path +"\_"+ etypes[i] +r"\_"+ esubtypes[i] +"\_"+ param
            os.makedirs(path)

def check_isntance_name(instance: str, path: str):
    all_instances = os.listdir(path)
    for elem in all_instances:
        if instance not in elem:
            continue
        else:
            return len(all_instances)
    return 0
def gen_next_name_table(instance: str, path: str):
    number = it.count(1)
    check = check_isntance_name(instance,path)
    if check > 0:
        number = it.count(check)
    number = number.__next__()
    return path+instance+"_"+str(number)+CSV_FORMAT