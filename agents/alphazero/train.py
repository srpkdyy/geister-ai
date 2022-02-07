import os
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
from collections import deque
from torch.utils.data import DataLoader
from .net import DualDQN
from envs.cgeister import cGeister
from .agent import AlphaZero
from ..random.agent import Random
from .self_play import self_play_history
from .utils import eval_network, play


def run(epochs=1000,
        weight=None,
        plays=150,
        trains=20,
        ds_size=500000):
    os.makedirs('./weights/alphazero/', exist_ok=True)

    kwargs = {
        'batch_size': 128,
        'shuffle': True,
        'num_workers': 4,
        'pin_memory': True
    }

    device = torch.device('cuda')
    torch.backends.cudnn.benchmark = True

    train_net = DualDQN().to(device)
    best_net = DualDQN().to(device)

    if weight is not None:
        train_net.load_state_dict(weight)

    weight = train_net.state_dict()
    best_net.load_state_dict(weight)

    train_net.train()
    best_net.eval()

    loss_p = nn.CrossEntropyLoss().to(device)
    loss_v = nn.MSELoss().to(device)
    optimizer = optim.AdamW(train_net.parameters())

    env = cGeister
    adevice = torch.device('cuda:0' if torch.cuda.device_count() == 1 else 'cuda:1')
    train_agent = AlphaZero(weight, evals=50, device=adevice)
    best_agent = AlphaZero(weight, evals=50, device=adevice)
    rndm = Random()

    dataset = deque(maxlen=ds_size)

    for epoch in range(1, epochs + 1):
        print('=================== Epoch: {} ======================'.format(epoch))
        weight = best_net.state_dict()
        best_agent.model.load_state_dict(weight)
        train_net.load_state_dict(weight)

        print('Self play:')
        gamma = 3
        for _ in tqdm(range(plays)):
            dataset.extend(self_play_history(env, best_agent, 180))
            dataset.extend(self_play_history(env, best_agent, 180, all_purple=True))
            gamma = max(1, gamma - 10/plays)

        dataloader = DataLoader(dataset, **kwargs)

        print('Train:')
        train(trains, train_net, dataloader, loss_p, loss_v, optimizer, device)

        print('Eval: ')
        train_agent.model.load_state_dict(train_net.state_dict())
        r = eval_network(10, env, train_agent, best_agent, verbose=True)

        if r >= 0:
            print('Update & save model: r={}'.format(r))
            best_net.load_state_dict(train_net.state_dict())
            torch.save(best_net.state_dict(), 'weights/alphazero/head.pth')

            rs = [utils.play(env, train_agent, rndm, 150, [True, False]) for _ in range(50)]
            rs.extend([-utils.play(env, rndm, train_agent, 150, [False, True]) for _ in range(50)])
            s = [0] * 3
            for r in rs:
                s[r] += 1
            print('Vs Random, draw:{} win{} lose:{}'.format(*s))



def train(epochs, model, dataloader, loss_p, loss_v, optimizer, device):
    for epoch in tqdm(range(epochs)):
        train_loss = 0

        for obsv, policy, value in dataloader:
            obsv = obsv.to(device)
            policy = policy.to(device)
            value = value.to(device)

            out_p, out_v = model(obsv)
            loss = loss_p(policy, out_p) + loss_v(value, out_v)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss

