import random
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
from collections import deque
from .dqn import DQN
from .agent import Greedy
from ...envs.cgeister import cGeister
from ...battle import battle



def run(weight=None):
    epochs = 1000000
    batch_size = 128
    
    policy_net = DQN().device('cuda:0')
    target_net = DQN().device('cuda:0')
    target_net.load_state_dict(policy_net.state_dict())
    policy_net.train()
    target_net.eval()

    criterion = nn.SmoothL1Loss().to('cuda:0')
    optimizer = optim.AdamW(policy_net.parameters())
    
    env = cGeister()

    for epoch in tqdm(range(epochs)):
        eps = schedule_eps(epoch, 0.05, 1.0, epochs//2)
        agent = Greedy(target_net, eps=eps)

        history = []
        for _ in range(50):
            history.extend(battle.self_play_history(env, agent, 180))
        Dataset(history)
        DataLoader(Dataset)

        if epoch % 100:
            torch.save(target_net.state_dict(), 'weights/dqn/latest.pth')
        

def schedule_eps(i, e_min, e_max, t):
    return max(e_min, e_max * (1 - i/t))


def train(model, dataloader, creterion, optimizer):


