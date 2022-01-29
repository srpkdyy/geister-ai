class Client:
    def __init__(self, host, port):
        pass


    def send(self, action):


class GeisterClient:


        


if __name__ == '__main__':
    import argparse
    from env.cgeister import cGeister

    parser = argparse.ArgumentParser()
    parser.add_argument('-h', '--host', type=str, default='localhost')
    parser.add_argument('-p', '--port', type=int, default=10000)
    parser.add_argument('-g', '--games', type=int, default=1)
    parser.add_argument('-a', '--agent', type=str, default='greedy')
    parser.add_argument('-w', '--weight', type=str, default='weights/dqn/latest.pth')
    args = parser.parse_args()

    env = cGeister()

    result = [0, 0, 0]
    for i in range(args.games):




