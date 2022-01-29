import os
import torch
from agents.dqn.net import DQN

m = DQN()
os.makedirs('weights/dqn', exist_ok=True)
torch.save(DQN().state_dict(), 'weights/dqn/example.pth')

os.chdir('envs')
os.system('c++ -O3 -Wall -shared -std=c++17 -fPIC `python -m pybind11 --includes` cboard.cpp cgeister.cpp cbuild.cpp -o cgeister.so')
os.chdir('..')

