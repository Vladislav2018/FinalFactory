from random import *

class Budget(object):

    def calc_salary_by_vacantion(self, current_salary_per_day,
                                 day_in_month, avg_count_of_work_days):
        return current_salary_per_day*randint(avg_count_of_work_days,day_in_month)

