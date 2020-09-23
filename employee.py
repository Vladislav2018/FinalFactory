import pandas as pd
from warnings import *
from typing import *
vacations = pd.read_csv('data/base_vacantions_info.csv')

class Employee():
    def __init__(self,  position: str, ownership: float = 0,
                 when_hired: int = 0, in_subordination: Any = None,
                 candidate: object = None):
        if position not in vacations['vacantion']:
            raise ('Unknown position: ' + position)
        if ownership < 0 or ownership > 1 or when_hired < 0:
            raise ('"Ownership" must be in range(0,1), "when_hired" must be only positive')
        if vacations['min_hierarhy_level'] >= 4 and in_subordination is not None:
            raise ('Nobody can rule this Employee: ' + str(id(self)))
        elif vacations['min_hierarhy_level'] < 4 and in_subordination is None:
            raise ('Employee: ' + str(id(self)) + ' must be subordinate')
        if vacations['min_hierarhy_level'] >= 4 and ownership < 0.25:
            warn('Employee: ' + str(id(self)) + ' should have a large share of the ownership')

        self.position = position
        self.ownership = ownership
        self.when_hired = when_hired
        self.in_submission = in_subordination

