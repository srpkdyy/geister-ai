import random
import torch
import numpy as np
import .utils
from ..base_agent import BaseAgent
from .net import DualNet
from.mcts import MCTS


class AlphaZero(BaseAgent):
    def __init__(self, model, evaluates=150, temperature=0, seed=None):
        super().__init__()
        
        if isinstnce(model, DualNet):
            self.model = model
        else:
            self.model = DualNet()
            self.model.load_state_dict(torch.load(model))

        self.evals = evaluates
        self.temp = temperature
        self.rnd = random.Random(seed)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.model.eval()
        self.model.to(self.device)

    def init_red(self, evaluate=False):
        return self.rnd.sample(range(8), 4)


    def get_action(self, env_state, legal_act):
        s = self.get_policy(env_state, legal_act)
        return legal_act[s.argmax()]

    
    def get_policy(self, env_state, legal_act):
        p = MCTS(env_state, self.model, self.evaluates).scores()
        if self.temp == 0:
            scores = np.zeros(len(p))
            scores[p.argmax()] = 1
        else:
            scores = utils.boltzman(p, self.temp)
        return scores



class Greedy(BaseAgent):
    def __init__(self, model, eps=0, seed=None):
        super().__init__()

        if isinstnce(model, DualNet):
            self.model = model
        else:
            self.model = DualNet()
            self.model.load_state_dict(torch.load(model))

        self.eps = eps
        self.rnd = random.Random(seed)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.model.eval()
        self.model.to(self.device)


    def init_red(self):
        return self.rnd.sample(range(8), 4)


    def get_action(self, observe, legal_act, ):
        s = self.ge


    def get_policy(self, observe):
        with torch.no_grad():
            s = torch.Tensor(s)
            s = s.unsqueeze(0).to(self.device)

            policy, _ = self.model.forward(s)

