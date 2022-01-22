import numpy as np
from tqdm import tqdm
from envs.geister import Geister
from envs.cgeister import CGeister
from agents.random.agent import Random

def battle(env, agent0, agent1):
    state = env.reset(agent0.init_red(), agent1.init_red())

    agents = [agent0, agent1]

    p = 0
    while not env.done:
        legal_act = env.get_legal_actions()

        act = agents[p].get_policy(state, legal_act)

        state = env.step(act)

        p ^= 1

    return env.winner, env.turn



if __name__ == '__main__':
    n = 10000
    #env = Geister()
    env = CGeister()
    agent0 = Random()
    agent1 = Random()

    rate = 0
    turn = []
    for _ in tqdm(range(n)):
        r, t =  battle(env, agent0, agent1)
        rate += r
        turn.append(t)

    print(1 - rate/n)
    turn = np.array(turn)
    print(turn.min(), turn.mean(), turn.max())

