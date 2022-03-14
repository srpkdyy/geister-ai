import string
from .client import Client



class RemoteEnv:
    def __init__(self, env, host, port, verbose):
        self.env = env()
        self.client = Client()
        self.host = host
        self.port = port
        self.verbose = verbose
        self.done = False

        self.to_str = lambda x: string.ascii_uppercase[x]


    def reset(self, red):
        self.client.connect(self.host, self.port)

        red_ascii = ''.join(map(self.to_str, red))
        if self.verbose:
            print('SET:' + red_ascii)
        state, self.done = self.client.set_red(red_ascii)
        obsv = self.env.update(state)
        return obsv


    def get_legal_actions(self):
        return self.env.get_legal_actions()


    def step(self, action):
        position, direction = action // 4, action % 4
        x, y, mov = position % 6, position // 6, ('N', 'W', 'E', 'S')[direction]
        state = self.env.make_state()

        unit = None
        for i in range(8):
            if x == int(state[i*3]) and y == int(state[i*3+1]):
                unit = self.to_str(i)
        assert unit is not None

        cmd = unit + ',' + mov
        state, self.done = self.client.move(cmd)

        obsv = self.env.update(state)

        if self.verbose:
            print('MOV:' + cmd)

        if self.done:
            self.client.close()
            self.result = ('Win', 'Lose', 'Draw')[self.env.winner]

        return obsv


    def make_state(self):
        return  self.env.make_state()

