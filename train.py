#import argparse
#from agents import dqn, alphazero
from agents.alphazero import train

if __name__ == '__main__':

    train.run()

    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--epochs', type=int, default=100000)
    parser.add_argument('-w', '--weight', type=str)
    parser.add_argument('-p', '--plays', type=int, default=10)
    parser.add_argument('-t', '--trains', type=int, default=1)
    parser.add_argument('-u', '--updates', type=int, default=1)
    parser.add_argument('-v', '--views', type=int, default=100)
    parser.add_argument('-s', '--saves', type=int, default=1000)
    args = parser.parse_args()

    train.run(args.epochs,
            weight=args.weight,
            plays=args.plays,
            trains=args.trains,
            updates=args.updates,
            views=args.views,
            saves=args.saves)
    '''

