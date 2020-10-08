import scipy as sp
import numpy as np
from itertools import chain, repeat
from math import *
import pandas as pd
def gen_factory_risks():
    PATH = "data/factory_info/factory_risks/f_risks.csv"
    POP_MIN_SIZE = 5
    POP_MAX_SIZE = 2*10**3
    POP_STEP = 2
    GDP_MIN= 5
    GDP_MAX = 30
    POPranges = []
    GDPranges = []
    POPparam = POP_MIN_SIZE
    GDPparam = GDP_MIN
    while POPparam < POP_MAX_SIZE:
        POPranges.append(POPparam)
        POPparam*=POP_STEP
    while GDPparam<GDP_MAX:
        GDPranges.append(floor(GDPparam))
        GDPparam+=5
    POPranges.append(POP_MAX_SIZE)
    GDPranges.append( GDP_MAX)
    ecological_priority = []

    for pop in POPranges:
        for gdp in GDPranges:
            ecoef = floor(log2(pop)*(gdp**0.2))
            ecological_priority.append(ecoef)
    POPranges = list(chain.from_iterable(zip(*repeat(POPranges, len(GDPranges)))))
    print(POPranges)
    GDPranges = list(repeat(GDPranges,10))
    GDPranges = list(chain(*GDPranges))
    print(GDPranges)
    data = {"population_under": POPranges, "gdp_under": GDPranges, "ecology_priority": ecological_priority}
    df = pd.DataFrame(data=data)
    df.to_csv(PATH)

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    from scipy.stats import truncnorm
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

