from datawriter import *
from vacantions import *
from typing import *
from city import *
from product import *
import pandas as pd
import candidates
import datawriter as dw
from usersfunc import *
path_candidates = "data/candidates/candidates.csv"
from data import products_raw_data as PWD

if __name__ == '__main__':
    i = 0
    while i < 2:
        gen_products(PWD.PARAMS_RANGES[i], PWD.PARAMS_COST_WEIGHTS[i], PWD.COST_MULTIPLIERS[i], PWD.STOCHASTIC_WEIGHTS[i])
        i+=1


"""
    candidates_to_write = []
    for i in range(50):
        city_number = np.random.randint(0,49)
        cand = candidates.Candidate(city_from = str(city_number))
        dw.dict_from_class_methods(cand, is_callable=True)
        candidate = dw.dict_from_class_methods(cand, is_callable=False)
        candidates_to_write.append(candidate)
    candidates_df = pd.DataFrame(candidates_to_write)
    candidates_df.to_csv(path_candidates)
    """




