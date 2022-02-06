def boltzman(policy, gamma):
    policy = [p ** (1/gamma) for p in policy]
    s = sum(policy)
    return [p / s for p in policy]


def eval_network(battles, env, agent0, agent1):
    env = env()
    agents = [agent0, agent1]

    r = [0] * 2
    for turn in range(2):
        for b in range(battles):
            red = agent0.init_red()
            env.reset(red, red)

            p = 0
            for i in range(200):
                state = env.make_state(True)
                legal_act = env.get_legal_actions()
                act = agents[p].get_action(state, legal_act)

                env.step(act)
                p ^= 1

                if env.done:
                    r[turn] += 1 if env.winner == 0 else -1
                    break
        agents = agents[::-1]

    return r[0] - r[1]


