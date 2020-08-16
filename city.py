import numpy as np
from typing import *
import math

class City(object):
    # ToDo: make possibility to choose the function of changing param
    def __init__(self, period: int, min_dist: int = 1, max_dist: int = 10**4):
        if period < 1 or max_dist < 1 or max_dist < 1:
            raise Exception('All the arguments must be > 1')
        self.period = period
        self.dist_to_the_nearest_factory = round(np.random.randint(min_dist, max_dist)*np.random.random(), 2)

    def calc_population(self, first_val: Union[None, int] = None, min_pop: int = 1,
                        max_pop: int = 2*10**3, scale: int = 10**4) -> int:
        if first_val is None:
            population = math.floor((np.random.pareto(0.6)+1)*min_pop*scale)
            while population > max_pop*scale:
                population -= (min_pop*scale)
        else:
            left_bound = -first_val / (min_pop * scale)

            population = first_val + np.random.randint(
                math.floor(left_bound), math.floor(abs(left_bound))
            )
        self.population = population
        return population

    def calc_gdp_per_capita(self,  population: int, first_val: Union[None, int] = None, avg_gdp_per_capita_in_country: int = 10**4,
                            avg_citizens: int= 5*10**4, population_infuence_coeff: int = 4) -> int:
        if first_val is None:
            coeff: float = math.pow(population/avg_citizens, 1/population_infuence_coeff)
            gdp: int = math.floor(np.random.normal(avg_gdp_per_capita_in_country,
                                              avg_gdp_per_capita_in_country/population_infuence_coeff)*coeff)
        else:
            gdp = round(np.random.normal(first_val, first_val/100))
            gdp = abs(gdp)
        self.gdp = gdp
        return gdp

    def calc_competition(self, population: int, gdp_per_capita: int,
                         first_val: Union[None, int] = None,) -> int:
        count: int = 0
        if first_val is None:
            count: int = math.floor(
                math.log10((population*gdp_per_capita))*np.random.random()
            )
        else:
            bound: int = np.random.laplace(0, round(first_val/10 + 0.6))
            bound = round(bound)
            count: int = first_val + bound
            count = abs(count)
        self.count = count
        return count

