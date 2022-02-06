import os
import random
import numpy as np
from tqdm import tqdm


def self_play_history(env, agent, turn, gamma=1.0, all_purple=False):
    env = env()

    if all_purple:
        obsv = env.update('14U24U34U44U15U25U35U45U41u31u21u11u40u30u20u10u')
    else:
        obsv = env.reset(agent.init_red(), agent.init_red())

    r = 0
    history = []
    for i in range(turn):
        state = env.make_state(usePurple=True)

        legal_act = env.get_legal_actions()
        policy = agent.get_policy(state, gamma)

        all_policy = np.zeros(144)
        all_policy[legal_act] = policy

        history.append([obsv, all_policy, None])

        act = random.choices(legal_act, policy)[0]
        obsv = env.step(act)

        if env.done:
            r = 1 if env.winner == 0 else -1
            break

    r = np.array([r], dtype=np.float32)
    for h in history:
        h[-1] = r
        r = -r

    return history

