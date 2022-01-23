import random

from ..base_agent import BaseAgent



class Random(BaseAgent):
    def __init__(self, seed=None):
        super().__init__()


    def init_red(self):
        return random.sample(range(8), 4)


    def get_action(self, state, legal_act):
        return random.choice(legal_act)

