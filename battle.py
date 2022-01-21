import numpy as np
from tqdm import tqdm
from envs.geister import Geister
from agents.random_agent import RandomAgent

def battle(env, agent0, agent1):
    state = env.reset(agent0.init_red(), agent1.init_red())

    agents = [agent0, agent1]

    p = 0
    done = False
    while not done:
        legal_act = env.get_legal_actions()

        act = agents[p].get_policy(state, legal_act)

        state, done = env.step(act)

        p ^= 1

    return env.winner, env.turn



if __name__ == '__main__':
    n = 10000
    rate = 0
    turn = []
    env = Geister()
    agent0 = RandomAgent()
    agent1 = RandomAgent()

    for _ in tqdm(range(n)):
        r, t =  battle(env, agent0, agent1)
        rate += r
        turn.append(t)

    print(1 - rate/n)
    turn = np.array(turn)
    print(turn.min(), turn.mean(), turn.max())

