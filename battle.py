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

    r = 0
    history = []
    legal_act = env.get_legal_actions()
    for i in range(turn):
        action = agent.get_action(state, legal_act)

        history.append([state, action, 0, None, None])

        state = env.step(action)
        history[i][-2] = state

        legal_act = env.get_legal_actions()
        history[i][-1] = legal_act

        if env.done:
            r = 1 if env.winner == 0 else -1
            break

    # last step is second player
    r = -r if i % 2 else r

    history[-1][2] = r
    history[-2][2] = -r
    return history




if __name__ == '__main__':
    import torch
    from tqdm import tqdm
    from concurrent.futures.thread import ThreadPoolExecutor
    from envs.cgeister import cGeister
    from agents.random.agent import Random
    from agents.dqn.agent import Greedy
    n = 100
    rate = 0
    d = torch.device('cpu')
    rndm = Random(seed=0)
    agent = Greedy(torch.load('weights/dqn/200.pth'), seed=42, device=d)
    for _ in tqdm(range(n)):
        ##h = self_play_history(cGeister, agent, 180)
        rate += play(cGeister, agent, rndm, 180)

    print('rate: ', rate)

