def self_play_history(env, agent, turn, mode='mix'):
    env = env(open=True)

    if mode == 'normal':
        state = env.reset(agent.init_red(), agent.init_red())
    elif mode == 'purple':
        state = env.update('14U24U34U44U15U25U35U45U41u31u21u11u40u30u20u10u')
    elif mode == 'mix':
        red = agent.init_red()
        env.reset(red, red)
        s = env.make_state(usePurple=True)
        state = env.update(s)

    legal_act = env.get_legal_actions()

    eps = agent.eps
    r = 0
    history = []
    for i in range(turn):
        agent.eps = (1 + i%2) * eps
        action = agent.get_action(state, legal_act)

        history.append([state, action, 0, None, None])

        state = env.step(action)
        history[-1][-2] = state

        legal_act = env.get_legal_actions()
        history[-1][-1] = legal_act

        if env.done:
            r = 1 if env.winner == 0 else -1
            r = -r if i % 2 else r
            history[-1][2] = r
            history[-2][2] = -r
            return history

    return []

