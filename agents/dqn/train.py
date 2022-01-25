import random
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
from collections import deque
from .net import DQN
from .agent import Greedy
from ..random.agent import Random
from envs.cgeister import cGeister
from battle import play, self_play_history



def run(epochs=10000, weight=None, save_interval=100):

    kwargs = {
        'batch_size': 128,
        'shuffle': True,
        'num_workers': 4,
        'pin_memory': True,
    }
    
    pdevice = torch.device('cuda:0')
    tdevice = torch.device('cuda:0')

    policy_net = DQN().to(pdevice)
    target_net = DQN().to(tdevice)
    target_net.load_state_dict(policy_net.state_dict())
    policy_net.train()
    target_net.eval()

    criterion = nn.SmoothL1Loss().to(pdevice)
    optimizer = optim.AdamW(policy_net.parameters())
    
    env = cGeister()
    rndm = Random()

    for epoch in tqdm(range(epochs)):
        eps = schedule_eps(epoch, 0.1, 0.9, epochs//2)

        agent = Greedy(target_net, eps=eps)

        history = []
        for _ in range(50):
            history.extend(self_play_history(env, agent, 180))

        dataloader = DataLoader(history, **kwargs)

        train(policy_net, target_net, dataloader, criterion, optimizer, pdevice)

        target_net.load_state_dict(policy_net.state_dict())

        if epoch % save_interval == 0:
            r = [play(env, agent, rndm, 150) for _ in range(100)]
            print('vs random, r:{}'.format(sum(r)))
            torch.save(target_net.state_dict(), 'weights/dqn/{}.pth'.format(epoch))

    r = [play(env, agent, rndm, 150) for _ in range(100)]
    print('last vs random, r:{}'.format(sum(r)))
    torch.save(target_net.state_dict(), 'weights/dqn/last.pth')
        

def schedule_eps(i, e_min, e_max, t):
    return max(e_min, e_max * (1 - i/t))


def train(pnet, tnet, dataloader, creterion, optimizer, device):
    for state, action, reward, next_state in dataloader:
        state = state.to(device)
        action = action.to(device).reshape(-1, 1)
        reward = reward.to(device).to(torch.float)
        next_state = next_state.to(device)

        output = pnet(state).gather(1, action)
        target = -tnet(next_state).max(1)[0].detach()

        is_final = reward != 0
        target[is_final] = reward[is_final]

        loss = creterion(output, target.unsqueeze(1))

        optimizer.zero_grad()
        loss.backward()
        for param in pnet.parameters():
            param.grad.data.clamp_(-1, 1)
        optimizer.step()

