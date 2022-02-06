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


if __name__ == '__main__':
    import torch
    from tqdm import tqdm
    from concurrent.futures.thread import ThreadPoolExecutor
    from envs.cgeister import cGeister
    from agents.random.agent import Random
    from agents.dqn.agent import Greedy

    env = cGeister
    rndm = Random()
    agent = Greedy(torch.load('weights/dqn/66000-d9w84l7.pth'))

    n = 100
    rate = 0
    hist = []

    for _ in tqdm(range(n)):
        rate += play(env, agent, rndm, 200)

    print('rate: {}'.format(rate))

