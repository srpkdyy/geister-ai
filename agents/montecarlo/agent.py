from .mcts import MCTS
from ..base_agent import BaseAgent


class P_MCTS(BaseAgent):
    def __init__(self):
        super().__init__()
        self.mcts = MCTS()

    def init_red(self):
        return [0, 1, 2, 3]

    def get_action(self, state, legal_act):
        scores = self.mcts.evaluate(state)
        idx = scores.index(max(scores))
        return legal_act[idx]

