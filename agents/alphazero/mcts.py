import math
import random
import torch
import torch.nn.functional as F
from envs.cgeister import cGeister

class Node:
    def __init__(self, state):
        self.s = state  # Game state
        self.P = None   # Policy
        self.A = None   # Legal actions
        self.N = 0      # Visited number
        self.Wa = {}    # Value of each action
        self.Na = {}    # Visited number of each action
        self.end = None # Node's value as a termination node
        self.next = {}  # Next node of each action


class PV_MCTS:
    def __init__(self, model, evals, c_puct, device):
        self.model = model
        self.evals = evals
        self.c_puct = c_puct
        self.device = device
        self.env = cGeister()


    def get_scores(self, s):
        root = Node(s)
        for _ in range(self.evals):
            self.evaluate(root)
        return [root.Na.get(a, 0) for a in root.A]


    def evaluate(self, node):

        if node.end is None:
            self.env.update(node.s)
            v = 0
            if self.env.done:
                v = 1 if self.env.winner == 0 else -1
            node.end = v

        # Game has ended.
        if node.end != 0:
            return node.end

        # Leaf node
        if node.P is None:
            self.env.update(node.s)
            obsv = self.env._observe()
            act = self.env.get_legal_actions()

            node.P, v = self.predict(obsv, act)
            node.A = act
            node.N += 1 
            return v

        # select next state
        best_score = -float('inf')
        best_act = -1

        t = math.sqrt(node.N)
        for i, a in enumerate(node.A):
            score = node.Wa.get(a, 0) / node.Na.get(a, 1) + \
                    self.c_puct * node.P[i] * t / (1 + node.Na.get(a, 0))
            if score > best_score:
                best_score = score
                best_act = a

        a = best_act
        self.env.update(node.s)
        self.env.step(a)
        next_s = self.env.make_state()

        next_node = Node(next_s)
        node.next[a] = next_node

        v = -self.evaluate(next_node)

        node.Wa[a] = node.Wa.get(a, 0) + v
        node.Na[a] = node.Na.get(a, 0) + 1
        node.N += 1

        return v


    def predict(self, observe, legal_act):
        with torch.no_grad():
            s = torch.tensor(observe, device=self.device).unsqueeze(0)
            a = torch.tensor(legal_act, device=self.device).unsqueeze(0)

            p, v = self.model(s)

            policy = p.gather(1, a).softmax(1).tolist()[0]
            value = v.item()
        return policy, value

