import socket



class Client:
    def __init__(self):
        self.session = None
        self.buf_size = 4096

    def connect(self, host, port):
        self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session.connect((host, port))


    def close(self):
       self.session.close()


    def set_red(self, red):
        assert 'SET' in self._recv()

        red_cmd = 'SET:' + red + '\r\n'
        self._send(red_cmd)
        assert 'OK' in self._recv()

        return self._clip_state(self._recv())


    def move(self, mov):
        mov_cmd = 'MOV:' + mov + '\r\n'
        self._send(mov_cmd)

        res = self._recv()
        assert 'OK' in res

        res = res.split()

        # Not game end
        if len(res) == 1:
            return self._clip_state(self._recv())
        else:
            return self._clip_state(res[-1])


    def _send(self, cmd):
        self.session.send(cmd.encode())


    def _recv(self):
        return self.session.recv(self.buf_size).decode()


    def _clip_state(self, response):
        res = response.split()[0]
        return res[4:], res[:3] in ('WON', 'DRW', 'LST')

