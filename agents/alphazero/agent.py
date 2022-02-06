import random
import torch
import numpy as np
from ..base_agent import BaseAgent
from .net import DualDQN
from .mcts import PV_MCTS
from .utils import boltzman


class AlphaZero(BaseAgent):
    def __init__(self, weight, evals=150, device=torch.device('cpu'), seed=None):
        super().__init__()

        self.model = DualDQN()
        self.model.load_state_dict(weight)

        
        self.device = device
        self.rnd = random.Random(seed)

        self.model.to(device)
        self.model.eval()

        self.pv_mcts = PV_MCTS(self.model, evals, 1.0, device)


    def init_red(self, evaluate=False):
        return self.rnd.sample(range(8), 4)


    def get_action(self, state, legal_act, gamma=0):
        policy = self.get_policy(state, gamma)
        action = self.rnd.choices(legal_act, policy)[0]
        return action

    
    def get_policy(self, state, gamma):
        scores = self.pv_mcts.get_scores(state)

        if gamma == 0:
            policy = [0] * len(scores)
            policy[scores.index(max(scores))] = 1.0
        else:
            policy = boltzman(scores, gamma)

        return policy

