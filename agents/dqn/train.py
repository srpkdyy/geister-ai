import random
from tqdm import tqdm
from collections import deque
from .agent import Greedy
from ...envs.cgeister import cGeister
from ...battle import battle


class Memory():
    def __init__(self, size):
        self.buffer = dqeue(maxlen=size)


    def add(self, experience):
        self.buffer.append(experience)


    def sample(self, batchsize):
        idx = random.sample(range(len(self.buffer)), batchsize)
        return [self.buffer[i] for i in idx]


    def __len__(self):
        return len(self.buffer)


def train(episodes):
    env = cGeister()

    for _ in tqdm(range(episodes)):
        main = Greedy('weights/?.pth', eps=eps)
        target = Greedy('weights/?.pth', eps=eps)

        history = battle_history(env, main, target, 150)
        


def _train(eps):

    r = 


