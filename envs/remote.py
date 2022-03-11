import string
import socket



class Client:
    def __init__(self, host, port):
        self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session.connect((host, port))
        self.buf_size = 4096


    def set_red(self, red):
        assert b'SET' in self.session.recv(self.buf_size)

        red_cmd = 'SET:' + red + '\r\n'
        self.session.send(red_cmd.encode())
        assert b'OK' in self.session.recv(self.buf_size)

        return self.__clip_state(self.session.recv(self.buf_size))


    def move(self, mov):
        mov_cmd = 'MOV:' + mov + '\r\n'
        self.session.send(mov.encode())

        res = self.session.recv(self.buf_size)
        assert b'OK' in res

        state = self.__clip_state(res)
        done = b'MOV' not in res

    def __clip_state(self):




class RemoteEnv:
    def __init__(self, env, host, port):
        self.env = env()
        self.client = Client(host, port)
        self.to_str = lambda x: string.ascii_uppercase[x]

    def reset(self, red):
        red_ascii = ''.join(map(self.to_str, red))
        res = self.client.set_red(red_ascii)
        state = self.env.update(res)
        return state

    def get_legal_actions(self):
        return self.env.get_legal_actions()

    def step(self, action):
        position, direction = action // 4, direction % 4
        x, y, mov = position % 6, position // 6, ('N', 'W', 'E', 'S')[direction]
        state = self.env.make_state()

        for i in range(8):
            if x == state[i*3] and y == state[i*3+1]:
                unit = to_str(i)

        return self.client.move(unit + ',' + mov)

    def render(self):


