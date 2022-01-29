def self_play_history(env, agent, turn):
    env = env()
    state = env.reset(agent.init_red(), agent.init_red())
    legal_act = env.get_legal_actions()

    r = 0
    history = []
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

