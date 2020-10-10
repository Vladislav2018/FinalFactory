import numpy as np
import pandas as pd
import datawriter as DW
import uuid
import math as m

path = "data/factory_info/"
# I should divide responsibility of this method
def gen_products(params, weights, cost_multiplier, stochastic_weight):
    list_keys = list(params.keys())
    list_values_raw = list(params.values())
    list_values = []
    values = []
    costs = []
    prices = []
    ids = []
    creating_speed = []
    for i in range(50):
        cost = 0
        for params_list in range(len(list_keys)):
            arr_to_choice = list(list_values_raw[params_list])
            param = np.random.choice(arr_to_choice)
            index_param = arr_to_choice.index(param)
            tp = str(param.dtype)
            if tp == "float64":
                param = round(param,2)
            weight = weights[params_list][index_param]
            weight = round(weight,2)
            cost += cost_multiplier*weight + np.random.random()*stochastic_weight
            cost = round(cost,2)
            values.append(param)
        ids.append(uuid.uuid1().__str__())
        speed = round(abs(m.tan(cost))*10)+np.random.choice(a=[100,200])
        creating_speed.append(speed)
        list_values.append(values)
        values = []
        price = round(cost*1.5 + abs(m.sin(m.sqrt(cost)))*np.random.randint(1,3), 2)
        prices.append(price)
        costs.append(cost)
    arr_values = np.array(list_values)
    arr_values = arr_values.transpose()
    costs = np.array(costs)
    arr_values = np.append(arr_values,[costs], axis=0)
    arr_values = np.append(arr_values, [prices], axis=0)
    arr_values = np.append(arr_values, [creating_speed], axis=0)
    arr_values = np.append(arr_values, [ids], axis=0)
    data = {}
    list_keys.append("costs")
    list_keys.append("prices")
    list_keys.append("creating_speed_in_secs")
    list_keys.append("uuid")
    i = 0
    for d in list_keys:
        data.update({d: list(arr_values[i])})
        i+=1
    tb = pd.DataFrame(data=data)
    tb.drop_duplicates()
    tb.to_csv(DW.gen_next_name_table("product", path))