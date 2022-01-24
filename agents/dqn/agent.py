import torch
from ..base_agent import BaseAgent


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


    def get_action(self, observe, legal_act):
        if self.rnd.random() < self.eps:
            return self.rnd.choice(legal_act)

        value = self.get_value(observe)
        legal_v = value[legal_act]
        return legal_act[legal_v.argmax()]


    def get_value(self, observe):
        with torch.no_grad():
            s = torch.Tensor(observe)
            s = s.unsqueeze(0).to(self.device)
            value = self.model.forward(s)
            value = value.cpu().detach().clone().numpy()
        return value
