import os
import torch
from agents.dqn.net import DQN

m = DQN()
os.makedirs('weights/dqn', exist_ok=True)
torch.save(DQN().state_dict(), 'weights/dqn/example.pth')

