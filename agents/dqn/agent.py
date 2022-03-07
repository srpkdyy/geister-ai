import torch
import random
from ..base_agent import BaseAgent
from .net import DQN


class Greedy(BaseAgent):
    def __init__(self, weight, eps=0, device=torch.device('cpu'), seed=None):
        super().__init__()

        self.model = DQN()
        self.model.load_state_dict(weight)
        #self.model.share_memory()

        self.eps = eps
        self.device = device
        self.rnd = random.Random(seed)

        self.model.to(self.device)
        self.model.eval()


    def init_red(self):
        return self.rnd.sample(range(8), 4)


    def get_action(self, observe, legal_act):
        if self.rnd.random() < self.eps:
            return self.rnd.choice(legal_act)

        with torch.no_grad():
            s = torch.tensor(observe, device=self.device).unsqueeze(0)
            a = torch.tensor(legal_act, device=self.device)

            v = self.model(s)

            value = v.squeeze(0).gather(0, a)
            act = a[value.argmax()].item()

        return act

