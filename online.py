import argparse
import time
import torch
from envs.cgeister import cGeister
from envs.remote import RemoteEnv
from agents.wrapper import AgentWrapper



def main(args):
    cfg = {}

    cfg['env'] = cGeister

    if args.agent == 'random':
        from agents.random.agent import Random
        cfg['arch'] = Random
        params = {}
        use_info = ['obsv', 'legal_act']
    elif args.agent == 'mcts':
        from agents.montecarlo.agent import P_MCTS
        cfg['arch'] = P_MCTS
        params = {'calc_ms': 9500}
        use_info = ['state', 'legal_act']
    elif args.agent == 'dqn':
        from agents.dqn.agent import Greedy
        cfg['arch'] = Greedy
        params = {'weight': torch.load(args.weight)}
        use_info = {'obsv', 'legal_act'}

    env = RemoteEnv(cfg['env'], args.host, args.port, args.verbose)
    agent = AgentWrapper(cfg['arch'], params, use_info)
    results = {}

    for i in range(args.games):
        obsv = env.reset(agent.init_red())

        while not env.done:
            state = env.make_state()
            legal_act = env.get_legal_actions()

            act = agent.get_action(obsv, state, legal_act)

            obsv = env.step(act)

        print('Game {}: {}'.format(i + 1, env.result), end='\n'*2) 
        results[env.result] = results.get(env.result, 0) + 1

        time.sleep(1)

    print('Results ==> {}'.format(results))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('host', type=str)
    parser.add_argument('port', type=int)
    parser.add_argument('-g', '--games', type=int, default=1)
    parser.add_argument('-a', '--agent', type=str, default='random')
    parser.add_argument('-w', '--weight', type=str)
    parser.add_argument('--verbose', action='store_true')

    main(parser.parse_args())
