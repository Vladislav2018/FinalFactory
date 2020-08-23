import numpy as np
from typing import *
import math

# Todo: save in variables all magic numbers
class City(object):
    # ToDo: make possibility to choose the function of changing param
    def __init__(self, period: int = 1, min_dist: int = 1, max_dist: int = 10**4):
        if period < 1 or max_dist < 1 or max_dist < 1:
            raise Exception('All the arguments must be > 1')
        self.period = period
        self.dist_to_the_nearest_factory = round(np.random.randint(min_dist, max_dist)*np.random.random(), 2)
        self.MIN_DIST = 1
        self.MAX_DIST = 10**4
        self.MIN_POP = 1
        self.MAX_POP = 2*10**3
        self.SCALE = 10**4
        self.POP_DISTR_BASE = 0.6
        self.GDB_DIVIDE_KOEF = 100

    def calc_population(self, first_val: Union[None, int] = None, min_pop: int = 1,
                        max_pop: int = 2*10**3, scale: int = 10**4) -> int:
        if first_val is None:
            population = math.floor((np.random.pareto(self.POP_DISTR_BASE)+1)*min_pop*scale)
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
            gdp = round(np.random.normal(first_val, first_val/self.GDB_DIVIDE_KOEF))
            gdp = abs(gdp)
        self.gdp = gdp
        return gdp

    def calc_competition(self, population: int, gdp_per_capita: int,
                         first_val: Union[None, int] = None,
                         product_id: Union[None, int] = None) -> int:
        if product_id is None:
            from warnings import warn
            warn('The product is None, method will return 0')
            return 0

        pop_len = len(str(population))
        realistic_koef = (population)*2*(10**(-7))
        if first_val is None:
            count: int = round(math.log(population*gdp_per_capita**pop_len)*realistic_koef)
        else:
            if first_val > 0:
                difference_part: float = first_val/2
                differences = np.arange(-round(first_val/difference_part)+1, round(first_val/difference_part)+1)
                probabilities_raw: List[float, ...] = [float(first_val)/(i**2 + 0.1) for i in differences]
                probabilities = [float(i)/sum(probabilities_raw) for i in probabilities_raw]
                bound: int = np.random.choice(differences, p= probabilities)
                count: int = first_val + bound
                count = abs(count)
            else:
                count = np.random.choice([0,1], p= [0.99, 0.01])
        self.count = count
        return count

    def calc_possible_places(self,
                             population: int, gdp_per_capita: int,
                             competition: Union[int, None],
                             first_val: Union[int, None] = None):

        additional: int = round(math.pow(population * gdp_per_capita,1/1.7)/self.SCALE)

        if competition is None:
            competition = 0
        first_val: int = competition + additional
        additional = round(math.sqrt(additional/20))
        if gdp_per_capita < 10**4:
            differences = np.arange(- additional, additional)
        else:
            differences = np.arange(- additional + 1, additional + 1)
        if len(differences) < 3:
            differences = [-1, 0, 1]
        probabilities_raw: List[float, ...] = [float(first_val)/(i**4 + 0.1) for i in differences]
        try:
            probabilities = [float(i) / sum(probabilities_raw) for i in probabilities_raw]
        except ZeroDivisionError:
            from sklearn import preprocessing
            scaler = preprocessing.MinMaxScaler()
            probabilities = scaler.fit_transform(probabilities_raw)
        bound = np.random.choice(differences, p= probabilities)
        count = first_val + bound
        if count < 0:
            count = 0
        self.all_places = count
        return count






