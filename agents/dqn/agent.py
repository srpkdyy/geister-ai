import torch
import random
from ..base_agent import BaseAgent
from .net import DQN


class Greedy(BaseAgent):
    def __init__(self, model, eps=0, use_cuda=True, seed=None):
        super().__init__()

        if isinstance(model, DQN):
            self.model = model
            self.device = torch.device('cuda' if next(model.parameters()).is_cuda else 'cpu')
        else:
            self.model = DQN()
            self.model.load_state_dict(torch.load('./weights/dqn/' + model))
            self.device = torch.device('cuda' if use_cuda and torch.cuda.is_available() else 'cpu')
            self.model.to(self.device)

        self.eps = eps
        self.rnd = random.Random(seed)
        self.model.eval()


    def init_red(self):
        return self.rnd.sample(range(8), 4)


    def get_action(self, observe, legal_act):
        if self.rnd.random() < self.eps:
            return self.rnd.choice(legal_act)

        with torch.no_grad():
            s = torch.Tensor(observe).pin_memory()
            s = s.to(self.device, non_blocking=True).unsqueeze(0)

            value = self.model.forward(s)

            value = value.detach().clone().squeeze(0)
            lv = value[legal_act]
            return legal_act[lv.argmax()]

