from datawriter import *
from vacantions import *
from typing import *
from city import *
from product import Product
import pandas as pd
from manufacturing import *
import candidates
import datawriter as dw

path_candidates = "data/candidates/candidates.csv"

if __name__ == '__main__':
    candidates_to_write = []
    for i in range(50):
        city_number = np.random.randint(0,49)
        cand = candidates.Candidate(city_from = str(city_number))
        dw.dict_from_class_methods(cand, is_callable=True)
        candidate = dw.dict_from_class_methods(cand, is_callable=False)
        candidates_to_write.append(candidate)
    candidates_df = pd.DataFrame(candidates_to_write)
    candidates_df.to_csv(path_candidates)



