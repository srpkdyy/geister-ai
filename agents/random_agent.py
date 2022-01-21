import random

from .base_agent import BaseAgent



class RandomAgent(BaseAgent):
    def __init__(self):
        super().__init__()


    def init_red(self):
        return random.sample(range(8), 4)


    def get_policy(self, state, legal_act):
        return random.choice(legal_act)

