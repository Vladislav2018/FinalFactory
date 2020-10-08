import numpy as np
import pandas as pd

path = "data/factory_info/product1.csv"
PARAMS_RANGES = \
    {
        "p1": np.arange(-1.,1., 0.1),
        "p2": np.arange(1,3,1),
        "p3": (1,2,50,200),
        "p4": np.arange(100,1000,1),
        "p5": (2.3,2.7,3.5)
    }

PARAMS_COST_WEIGHTS = \
    [
        [-i**2 for i in PARAMS_RANGES["p1"]],
        (0.2, 0.45, 0.35),
        (0.1, 0.2, 0.5, 0.2),
        np.arange(1, len(PARAMS_RANGES["p4"])),
        (0.9, 0.01, 0.09)
    ]
COST_MULTIPLIER = 10
STOCHASTIC_WEIGHT = 1

def gen_products():
    list_keys = list(PARAMS_RANGES.keys())
    list_keys.append("costs")
    list_values_raw = list(PARAMS_RANGES.values())
    list_values = []
    values = []
    costs = []
    for i in range(50):
        cost = 0
        for params_list in range(len(PARAMS_RANGES)):
            arr_to_choice = list(list_values_raw[params_list])
            param = np.random.choice(arr_to_choice)
            index_param = arr_to_choice.index(param)
            param = round(param,2)
            weight = PARAMS_COST_WEIGHTS[params_list][index_param]
            weight = round(weight,2)
            cost += COST_MULTIPLIER*weight + np.random.random()
            cost = round(cost,2)
            values.append(param)
        list_values.append(values)
        values = []
        costs.append(cost)
    arr_values = np.array(list_values)
    arr_values = arr_values.transpose()
    costs = np.array(costs)
    arr_values = np.append(arr_values,[costs], axis=0)
    data = {}
    i = 0
    for d in list_keys:
        data.update({d: list(arr_values[i])})
        i+=1
    pd.DataFrame(data=data).to_csv(path)