import numpy as np


class Board:
    WIDTH = 6
    MAX_IDX = 36

    GOAL = (-6, -1)
    ESCAPED = 56
    TOMB = 63

    def __init__(self, red, pos):
        PLAYER_NUM = 2
        PIECE_NUM = 8
        COLOR_NUM = 2

        # UP, LEFT, RIGHT, DOWN
        self.direction = (
            (-Board.WIDTH,),
            (-1,),
            (+1,),
            (+Board.WIDTH,))

        # Blue: False, Red: True; [[A,...,H], [a,...,h]]
        self.red = np.zeros((PLAYER_NUM, PIECE_NUM), dtype=bool)
        self.red[0][red[0]] = True
        self.red[1][red[1]] = True

        # 0-35 index; [[A,...,H], [a,...,h]]
        self.pos = self.toindex(np.array(pos, dtype=np.int16))

        # was taken; Bool; [[A,...,H],[a,...,h]
        self.taken = self.pos == Board.TOMB

        # was taken; [[B, R], [b, r]]
        b, r = self.taken[~self.red], self.taken[self.red]
        t = PIECE_NUM // COLOR_NUM
        self.n_taken = np.count_nonzero((b[:t],r[:t],b[t:],r[t:]), axis=1)
        self.n_taken = self.n_taken.reshape(PLAYER_NUM, COLOR_NUM)

        self.have_escaped = False
        self.all_taken = False

    def toindex(self, p):
        return (p % 10) * Board.WIDTH + p // 10


    def swap(self):
        self.red = self.red[::-1]

        idx = self.pos < Board.MAX_IDX
        self.pos[idx] = Board.MAX_IDX - self.pos[idx] - 1
        self.pos = self.pos[::-1]

        self.taken = self.taken[::-1]

        self.n_taken = self.n_taken[::-1]


    def state(self):
        channels = 3
        pos = self.pos
        red = self.red[0]
        on_board = (~self.taken) & (self.pos != Board.ESCAPED)

        board = np.zeros([channels, Board.MAX_IDX], np.int16)
        board[0][pos[0][on_board[0] & ~red]] = 1
        board[1][pos[0][on_board[0] & red]] = 1
        board[2][pos[1][on_board[1]]] = 1
        board = board.reshape(channels, Board.WIDTH, Board.WIDTH)

        n_taken = self.n_taken.reshape(-1).copy()
        return board, n_taken


    def get_next_act(self):
        ally = self.pos[0]
        edge = Board.WIDTH - 1

        no_stack = ~np.isin(ally + self.direction, ally)
        on_board = ((
            ally // Board.WIDTH > 0,
            ally % Board.WIDTH > 0,
            ally % Board.WIDTH < edge,
            ally // Board.WIDTH < edge))

        can_move = no_stack & on_board & ~self.taken[0]

        # if can goal
        can_move[0] |= ((ally == 0) | (ally == edge)) & ~self.red[0]

        act = ally*4 + ((0,),(1,),(2,),(3,),)
        
        return act[can_move]


    def move(self, act_i):
        now_pos, move = act_i // 4, act_i % 4
        moved_pos = now_pos + self.direction[move][0]

        if moved_pos in Board.GOAL:
            moved_pos = Board.ESCAPED

        self.pos[self.pos == now_pos] = moved_pos

        taken = self.pos[1] == moved_pos

        if taken.any():
            self.pos[1][taken] = Board.TOMB
            self.taken[1] |= taken

            color = int(self.red[1][taken])
            self.n_taken[1][color] += 1


    def game_over(self):
        self.have_escaped = (self.pos == Board.ESCAPED).any()
        self.all_taken = (self.n_taken == 4).any()
        return self.have_escaped or self.all_taken


    # 0: now_player
    def get_winner(self):
        if self.have_escaped:
            return int((self.pos[1] == Board.ESCAPED).any())
        if self.all_taken:
            return int((self.n_taken[(0, 1),(0, 1)] == 4).any())
        return None


    def disp(self):
        print('Red:\n', self.red)
        print('Position:\n', self.pos)
        print('Taken:\n', self.taken)
        print('Winner:\n', self.get_winner())
        print('Board:\n', *self.state())


if __name__ == '__main__':
    red = [[0, 1, 2, 3] ,[0, 1, 2, 4]]
    pos = [[14, 24, 33, 44, 15, 25, 35, 50],
           [55, 31, 21, 11, 40, 30, 20, 5]]

    b = Board(red, pos)

    while not b.game_over():
        b.move(b.get_next_act()[0])

    b.disp()

