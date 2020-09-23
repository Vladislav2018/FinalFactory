import uuid
import pandas as pd

class Candidate():
    def __init__(self, **kwards):
        self.uuid = uuid.uuid1()
        params = kwards.keys()
