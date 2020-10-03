import uuid
import pandas as pd
import datawriter as dw
import math as m
import numpy as np
from usersfunc import *
Vacansies_PATH = "data/base_vacantions_info.csv"
cities_path = "data/cities/before/"

vacansies = pd.read_csv(Vacansies_PATH)

class Candidate():

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if hasattr(self, 'pretend_position') is True:
            if self.pretend_position not in list(vacansies['vacantion'].array):
                raise ("Unknown position")
        else:
            self.calc1_pretend_position()
        if hasattr(self, "city_from") == False:
            raise Exception("Unknown city")
        city_data = dw.get_csv_essence(cities_path, 'City', self.city_from)
        self.uuid = uuid.uuid1()
        gbd_per_capita_all = city_data["gdp_per_capita"]
        gbd_per_capita = gbd_per_capita_all.mean()
        population = city_data["population"].mean()
        self.gbd_per_capita_coef = round(gbd_per_capita / 10 ** 4, 2)
        self.population_coef = round(2 * 10 ** 7 / population,2)

    def calc1_pretend_position(self):
        if hasattr(self, 'pretend_position') is False:
            vac_salaries = dw.dict_from_csv(Vacansies_PATH, "vacantion", "standart_salary_per_day")
            salaries = list(vac_salaries.values())
            weights = []
            for salary in salaries:
                weight = 1/salary**2
                weights.append(weight)
            standart_weights = [float(i) / sum(weights) for i in weights]
            vacansies = list(vac_salaries.keys())
            self.pretend_position = np.random.choice(a=vacansies, p= standart_weights)
        return self.pretend_position

    def calc2_is_male(self)->int:
        vacantions_gender: dict = dw.dict_from_csv(Vacansies_PATH, "vacantion", "male_sex_prob_coef")
        prob = vacantions_gender[self.pretend_position]
        prob = prob/100
        is_male = np.random.choice(a= [0,1], p = [1- prob, prob])
        self.is_male = is_male
        return is_male

    def calc3_get_age(self) -> int:
        vacantions_ages: dict = dw.dict_from_csv(Vacansies_PATH, "vacantion", "median_age")
        age_coef: int = vacantions_ages[self.pretend_position]
        poss_ages = np.arange(18, 65)
        weights = []
        for age in poss_ages:
            weight = 1/abs(age_coef - age**2)
            weights.append(weight)
        standart_weights = [float(i)/sum(weights) for i in weights]
        candidate_age = np.random.choice(a = poss_ages, p = standart_weights)
        candidate_age = int(candidate_age)
        self.age = candidate_age

        return candidate_age

    def calc4_smocking(self)->int:
        if self.is_male == 1:
            self.smocker =  np.random.choice(a = [1, 0], p = [0.7, 0.3])
        else:
            self.smocker = np.random.choice(a=[1, 0], p=[0.5, 0.5])
        return self.smocker

    def calc5_expierence_prpos(self):
        exp_table = dw.dict_from_csv(Vacansies_PATH, "vacantion", "min_req_exp")
        exp_coef = exp_table[self.pretend_position]
        if(self.is_male == True):
           exp = m.floor(self.population_coef*self.age*exp_coef*np.random.random()/10000)
        else:
            age_infl = 0.015*self.age
            exp = m.floor(self.population_coef*self.age*exp_coef*np.random.random()/10000) - 36*np.random.choice(a = [0,1], p=(1 - age_infl, age_infl))
        self.expierence = abs(exp)
        return self.expierence

    def calc6_get_softskills(self):
        meansoft = m.floor((self.age+self.expierence)*np.random.random())
        distr = get_truncated_normal(mean= meansoft, sd = 30, low=1, upp= 100)
        self.softskills = m.floor(distr.rvs())
        return self.softskills

    def calc7_get_hardskills(self):
        meam_coef = self.population_coef*self.gbd_per_capita_coef*self.age+(self.expierence/12)
        coef = len(str(m.floor(meam_coef))) - len(str(100)) + 1
        meam_coef = meam_coef*(0.1**coef)
        distr = get_truncated_normal(mean= meam_coef, sd = meam_coef/3, low=1, upp= 100)
        self.hardskills = m.floor(distr.rvs())
        return self.hardskills

    def calc8_pretend_salary(self):
        salaries = dw.dict_from_csv(Vacansies_PATH, "vacantion", "standart_salary_per_day")
        salary = salaries[self.pretend_position]
        exp_table = dw.dict_from_csv(Vacansies_PATH, "vacantion", "min_req_exp")
        req_exp = exp_table[self.pretend_position]
        delta_exp = self.expierence-req_exp

        weights = np.array([0.95])
        other_weights = np.random.random(5)
        weights = np.concatenate([other_weights, weights])
        weights = list(weights)
        params = [salary, self.hardskills, self.population_coef*self.gbd_per_capita_coef,
                  delta_exp, self.softskills,  self.age]
        final_arr = map(lambda x, y: x * y, params, weights)
        final_arr = [el * 0.4 for el in final_arr]
        pretend_salary = m.floor(sum(final_arr))

        self.pretend_salary = pretend_salary
        return pretend_salary