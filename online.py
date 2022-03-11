import argparse
from envs.cgeister import cGeister
from envs.remote import RemoteEnv


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-h', '--host', type=str, default='localhost')
    parser.add_argument('-p', '--port', type=int, default=10000)
    parser.add_argument('-g', '--games', type=int, default=1)
    parser.add_argument('-a', '--agent', type=str, default='random')
    parser.add_argument('-w', '--weight', type=str)
    args = parser.parse_args()



    if args.agent == 'random':
        from agents.random.agent import Random
        agent = Random()

    env = RemoteEnv(cGeister, args.host, args.port)
    result = [0, 0, 0]

    for i in range(args.games):
        state = env.reset(agent.init_red())

        while not env.done:
            legal_act = env.get_legal_actions()
            act = agent.get_action(state, legal_act)

            env.render()
            state = env.step(act)

        print('Game {}: {}'.format(i + 1, ['Win', 'Draw', 'Lose'][env.result])) 
        result[env.result] += 1

    print('Result ==> Win:{}, Draw:{}, Lose{}'.format(*result))



