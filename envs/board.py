import numpy as np


class Board:
    WIDTH = 6
    MAX_IDX = 36
    TOMB = 63
    GOAL = 56

    def __init__(self, red, pos):
        PLAYER_NUM = 2
        PIECE_NUM = 8
        COLOR_NUM = 2

        # Blue: False, Red: True; [A,...,h]
        self.red = np.zeros(PLAYER_NUM * PIECE_NUM, dtype=bool)
        self.red[red] = True
        self.red = self.red.reshape(PLAYER_NUM, PIECE_NUM)

        # 0-35 index; [[A,...,H], [a,...,h]]
        self.pos = self.toindex(np.array(pos, dtype=np.int16))
        self.pos = self.pos.reshape(PLAYER_NUM, PIECE_NUM)

        # was taken; Bool; [A,...,h]
        self.taken = self.pos == Board.TOMB

        # was taken; [[B, R], [b, r]]
        b, r = self.taken[~self.red], self.taken[self.red]
        t = PIECE_NUM // COLOR_NUM
        self.n_taken = np.count_nonzero([b[:t], r[:t], b[t:], r[t:]], axis=1)
        self.n_taken = self.n_taken.reshape(PLAYER_NUM, COLOR_NUM)

    def toindex(self, p):
        return (p % 10) * Board.WIDTH + p // 10

    def swap(self):
        self.red = self.red[::-1]

        idx = self.pos < Board.MAX_IDX
        self.pos[idx] = Board.MAX_IDX - self.pos[idx] - 1
        self.pos = self.pos[::-1]

        self.taken = self.taken[::-1]

        self.n_taken = self.n_taken[::-1]

    def game_state(self):
        channels = 3
        pos = self.pos
        red = self.red
        taken = self.taken

        board = np.zeros([channels, Board.MAX_IDX])
        board[0][pos[0][~red[0] & ~taken[0]]] = 1
        board[1][pos[0][red[0] & ~taken[0]]] = 1
        board[2][pos[1][~taken[1]]] = 1
        board = board.reshape(channels, Board.WIDTH, Board.WIDTH)

        n_taken = self.n_taken.reshape(-1).copy()
        return board, n_taken


    def legal_move_index(self):
        pass

    def move(self, move_i):
        pass

    def game_over(self):
        return False


    def disp(self):
        print('Red:\n', self.red)
        print('Position:\n', self.pos)
        print('Taken:\n', self.taken)
        print('Board:\n', self.game_state())


if __name__ == '__main__':
    red = [0, 1, 6, 7, 8, 11, 13, 15]
    pos = [99, 24, 99, 44, 15, 25, 35, 45, 41, 31, 21, 11, 40, 30, 20, 99]

    b = Board(red, pos)
    b.disp()

    b.swap()
    b.disp()

