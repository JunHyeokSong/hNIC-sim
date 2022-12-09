'''
Simulator is responsible to control one experiment for given parameters
Specifically,
- Generates requests,
- Control Cache,
- Collect metrics
'''

from cache import Cache
from content import *
from content_table import ContentTable

class Simulator:
    def __init__(self, scenario, parameters, n_contents: int) -> None:
        self.scenario = scenario
        self.parameters = parameters
        self.n_contents = n_contents

        contentTable = ContentTable()
        for i in range(n_contents):
            contentTable.add(Content(i, contentSizePolicy(i)), 0.0, 0.0, 0, 0)
        self.cache = Cache(contentTable, parameters)
        pass

    def execute(self):
        for r, t in self.scenario:
            self.cache.query(r, t)

    def score(self):
        h = self.cache.metric["hit"]
        m = self.cache.metric["miss"]
        return h / (h+m)