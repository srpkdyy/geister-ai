
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


def self_play_history(env, agent, turn):
    state = env.reset(agent.init_red(), agent.init_red())

    r = 0
    history = []
    for i in range(turn):
        legal_act = env.get_legal_actions()
        action = agent.get_action(state, legal_act)

        history.append([state, action, 0, None])

        state = env.step(action)
        history[i][-1] = state

        if env.done:
            r = 1 if env.winner == 0 else -1
            break

    # last step is second player
    r = -r if i % 2 else r

    history[-1][-2] = r
    history[-2][-2] = -r
    return history




if __name__ == '__main__':
    from tqdm import tqdm
    from concurrent.futures.thread import ThreadPoolExecutor
    from envs.cgeister import cGeister
    from agents.random.agent import Random
    from agents.dqn.agent import Greedy
    n = 100
    env = cGeister()
    agent = Greedy('head.pth', seed=42)

    rate = 0
    for _ in tqdm(range(n)):
        h = self_play_history(env, agent, 180)

    print('rate: ', rate)

