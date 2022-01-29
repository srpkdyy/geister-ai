import os
import cPickle as pickle
from datetime import datetime
from tqdm import tqdm
from ...envs.cgeister import CGeister
from .agent import PGreedy


SELF_PLAY_NUM = 2000


def self_play(eps=0.3):
    histories = []

    env = CGeister()
    agent = PGreedy('./weights/head.pth', eps_greedy=True, eps=eps)

    for i in tqdm(range(SELF_PLAY_NUM)):
        history = play(env, agent)
        histories.extend(history)

    save_history(histories)


def play(env, agent):
    history = []
    
    state = env.reset(agent.init_red(), agent.init_red())

    while not env.done:
        legal_act = env.get_legal_actions()
        act = agent.get_action(state, legal_act)








def first_player_value(env):
    if env.done:
        return 1 if env.winner == 0 else -1
    return 0


def save_history(history):
    now = datetime.now()
    os.makedirs('./data', exist_ok=True)
    path = './data/' + '{:%Y%m%d%H%M%S}'.format(now) + '.history'
    with open(path, 'wb') as f:
        pickle.dump(history, f)


