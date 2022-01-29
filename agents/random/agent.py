import random

from ..base_agent import BaseAgent



class Random(BaseAgent):
    def __init__(self, seed=None):
        super().__init__()
        self.rnd = random.Random(seed)


    def init_red(self):
        return self.rnd.sample(range(8), 4)


    def get_action(self, state, legal_act):
        return self.rnd.choice(legal_act)
