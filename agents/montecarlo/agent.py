from .mcts import MCTS
from ..base_agent import BaseAgent


class P_MCTS(BaseAgent):
    def __init__(self, calc_ms=1000):
        super().__init__()
        self.mcts = MCTS(calc_ms)

    def init_red(self):
        return [3, 4, 5, 6]
#        return [0, 1, 2, 7]
        return [0, 2, 5, 7]
        return [0, 3, 4, 7]
        return [1, 2, 5, 6]

    def get_action(self, state, legal_act):
        scores = self.mcts.evaluate(state, legal_act)
        idx = scores.index(max(scores))
        return legal_act[idx]

