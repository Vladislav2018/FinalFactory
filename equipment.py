from typing import *

avaliable_types = ('Transport machine', 'engine', 'machine')

class Equipment(object):
    def __init__(self, e_type: str, using_period: int, start_price: int,
                 responsible_employee: Dict[Any, Any]):
        self.using_period = using_period
        self.price = start_price
        if e_type in avaliable_types:
            self.e_type: str = e_type
        else:
            raise Exception("Unknown e_type was given")

# depends from employee
    def calc_equipment_deprecation(self, e_type: str, using_period: int) -> float:
        #from 0 to 1
        pass

    def small_repair_cost_range(self, e_type):
        pass

    def critical_repair_cost_range(self, e_type):
        pass

