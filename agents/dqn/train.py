import os
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
from .self_play import self_play_history
from battle import play


def run(epochs, weight, plays, datas, trains, updates, views, saves):
    os.makedirs('./weights/dqn', exist_ok=True)
    
    if saves is None:
        saves = epochs // 100

    kwargs = {
        'batch_size': 128,
        'shuffle': True,
        'num_workers': 4,
        'pin_memory': True,
    }
    
    device = torch.device('cuda')
    torch.backends.cudnn.benchmark = True

    policy_net = DQN().to(device)
    target_net = DQN().to(device)

    if weight is not None:
        policy_net.load_state_dict(torch.load(weight))

    weight = policy_net.state_dict()
    target_net.load_state_dict(weight)

    policy_net.train()
    target_net.eval()

    criterion = nn.SmoothL1Loss().to(device)
    optimizer = optim.AdamW(policy_net.parameters())
    
    env = cGeister
    adevice = torch.device('cuda:0' if torch.cuda.device_count() == 1 else 'cuda:1')
    agent = Greedy(weight, device=adevice)
    rndm = Random()

    dataset = deque([], maxlen=datas)

    for epoch in tqdm(range(1, epochs + 1)):

        history = []
        for i in range(plays):
            agent.eps = 0.4 ** (1 + (i*7 / (plays-1)))
            history.extend(self_play_history(env, agent, 200))

        with torch.no_grad():
            mask = torch.empty(144, dtype=torch.int64)
            for h in history:
                legal_i = h[-1]
                mask.fill_(legal_i[0])
                mask[:len(legal_i)] = torch.tensor(legal_i)
                h[-1] = mask.clone()

        dataset.extend(history)
        dataloader = DataLoader(dataset, **kwargs)

        for _ in range(trains):
            train(policy_net, target_net, dataloader, criterion, optimizer, device)

        weight = policy_net.state_dict()
        agent.model.load_state_dict(weight)
        if epoch % updates == 0:
            target_net.load_state_dict(weight)

        if epoch % views == 0:
            agent.eps = 0
            r = [play(env, agent, rndm, 150) for _ in range(100)]
            s = [0, 0, 0]
            for rr in r:
                s[rr] += 1
            print('vs random, draw:{} win:{} lose:{}'.format(*s))
            score = 'd{}w{}l{}'.format(*s)

        if epoch % saves == 0:
            torch.save(weight, 'weights/dqn/{}-{}.pth'.format(epoch, score))


def schedule_eps(e, e_min, e_max, t):
    return max(e_min, e_max * (1 - e/t))


def train(pnet, tnet, dataloader, creterion, optimizer, device):
    for state, action, reward, next_state, next_legal_actions in dataloader:
        state = state.to(device)
        action = action.to(device).reshape(-1, 1)
        reward = reward.to(device)
        next_state = next_state.to(device)
        next_legal_actions = next_legal_actions.to(device)

        output = pnet(state).gather(1, action)
        target = -tnet(next_state).gather(1, next_legal_actions).max(1)[0].detach()

        not_final = reward == 0
        target = target * not_final + reward

        loss = creterion(output, target.unsqueeze(1))

        optimizer.zero_grad()
        loss.backward()
        for param in pnet.parameters():
            param.grad.data.clamp_(-1, 1)
        optimizer.step()

