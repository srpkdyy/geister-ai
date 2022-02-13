import argparse


def run(args):
    if args.agent == 'dqn':
        from agents.dqn import train
        params = {
            'epochs': 100000,
            'weight': None,
            'plays': 20,
            'trains': 10,
            'updates': 1,
            'views': 100,
            'saves': 1000
        }
    elif args.agent == 'alphazero':
        from agents.alphazero import train

    train.run(**params)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('agent', type=str)
    args = parser.parse_args()

    run(args)

