def play(env, agent0, agent1, turn):
    env = env()
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


def self_play_history(env, agent, turn):
    env = env()
    state = env.reset(agent.init_red(), agent.init_red())
    legal_act = env.get_legal_actions()

    r = 0
    dummy = [None, None, 0, state, legal_act]
    history = [dummy]*2
    for i in range(turn):
        action = agent.get_action(state, legal_act)

        history.append([state, action, 0, None, None])

        state = env.step(action)
        history[-2][-2] = state

        legal_act = env.get_legal_actions()
        history[-2][-1] = legal_act

        if env.done:
            r = 1 if env.winner == 0 else -1
            # last step is second player
            r = -r if i % 2 else r
        
            history[-1][2] = r
            history[-2][2] = -r
            history[-1][3:] = dummy[3:]
            return history[2:]

    return history[2:-2]


if __name__ == '__main__':
    import torch
    from tqdm import tqdm
    from concurrent.futures.thread import ThreadPoolExecutor
    from envs.cgeister import cGeister
    from agents.random.agent import Random
    from agents.dqn.agent import Greedy

    env = cGeister
    rndm = Random()
    agent = Greedy(torch.load('weights/dqn/49999.pth'), 0.5)

    n = 10
    rate = 0
    hist = []

    for _ in tqdm(range(n)):
        hist.extend(self_play_history(env, rndm, 180))

    for i in range(-3, 0):
        print(hist[i][0], hist[i][1:-2], hist[i][-2], hist[i][-1])
        print('"""""""""""""""""""""""""""""""""""""""')
