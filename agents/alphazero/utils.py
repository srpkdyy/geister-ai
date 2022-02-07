def boltzman(policy, gamma):
    policy = [p ** (1/gamma) for p in policy]
    s = sum(policy)
    return [p / s for p in policy]


def eval_network(battles, env, agent0, agent1, verbose=False):
    env = env()
    agents = [agent0, agent1]

    r = [0] * 2
    for turn in range(2):
        for b in range(battles):
            p = turn
            red = agents[p].init_red()
            env.reset(red, red)

            for i in range(200):
                state = env.make_state(True)
                legal_act = env.get_legal_actions()
                act = agents[p].get_action(state, legal_act, gamma=1)
                env.step(act)
                p ^= 1

                if env.done:
                    r[turn] += 1 if env.winner == 0 else -1
                    break

    if views:
        print('r: {}, {}'.format(*r))
    return r[0] - r[1]


def play(env, agent0, agent1, turn, use_state=[False]*2):
    env = env()
    state = env.reset(agent0.init_red(), agent1.init_red())
    agents = [agent0, agent1]

    p = 0
    for i in range(turn):
        if use_state[p]:
            state = env.make_state(usePurple=True)
        legal_act = env.get_legal_actions()
        act = agents[p].get_action(state, legal_act)
        state = env.step(act)
        p ^= 1

        if env.done:
            return 1 if env.winner == 0 else -1
            
    return 0

