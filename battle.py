import numpy as np
from tqdm import tqdm
from envs.geister import Geister
from envs.cgeister import cGeister
from agents.random.agent import Random


def play(env, agent0, agent1, turn):
    state = env.reset(agent0.init_red(), agent1.init_red())
    agents = [agent0, agent1]

    p = 0
    for i in range(turn):
        legal_act = env.get_legal_actions()
        act = agents[p].get_action(state, legal_act)
        state = env.step(act)
        p ^= 1

        if env.done:
            return 1 if env.winner == 0 else -1
    return 0


def play_history(env, agent0, agent1, turn):
    state = env.reset(agent0.init_red(), agent1.init_red())
    agents = [agent0, agent1]

    history = []

    p = 0
    r = 0
    for i in range(turn):
        legal_act = env.get_legal_actions()
        action = agents[p].get_action(state, legal_act)

        history.append([state, action, None, None])

        state = env.step(action)
        history[i][-1] = state

        p ^= 1

        if env.done:
            r = 1 if env.winner == 0 else -1
            break

    # last step is first player
    r = r if turn % 2 else -r

    history[-1][-2] = r
    history[-2][-2] = -r
    return history




if __name__ == '__main__':
    n = 1
    env = cGeister()
    agent0 = Random()
    agent1 = Random()

    rate = 0
    turn = []
    for _ in tqdm(range(n)):
        h = play_history(env, agent0, agent1, 200)
    print(h)

