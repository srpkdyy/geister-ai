import numpy as np
from .board import Board


class Geister:
    N_ACTION = 144
    INIT_POS = ((14, 24, 34, 44, 15, 25, 35, 45),
                (41, 31, 21, 11, 40, 30, 20, 10))

    def __init__(self):
        self.board = None
        self.next_player = None
        self.turn = 0
        self.done = False
        self.winner = None

    def reset(self, red0, red1):
        self.board = Board((red0, red1), Geister.INIT_POS)
        self.next_player = 0
        self.turn = 0
        self.done = False
        self.winner = None
        return self.board.state()

    def update(self, state, turn):
        self.board = Board(self.encode(state))
        self.next_player = 0
        self.turn = turn
        self.done = self.board.game_over()
        self.winner = None
        return self.board.state()
    

    def step(self, action):
        assert not self.done
        assert 0 <= action < Geister.N_ACTION

        self.turn += 1

        self.board.move(action)

        if self.board.game_over():
            self._set_winner()
            self.done = True
        else:
            self._change_side()

        return self.board.state(), self.done


    def render(self):
        print('Turn: '+str(self.turn), 'DONE: '+str(self.done))
        board, taken = self.board.state()
        print('Taken: B:{} R:{} b:{} r:{}'.format(*taken))
        print('Escaped: '+str(self.board.have_escaped))
        print(board[0] | board[1]*2 | board[2]*-1)

    
    def get_legal_actions(self):
        return self.board.get_next_act()

    def _encode(self, state):
        pass


    def _change_side(self):
        self.next_player ^= 1
        self.board.swap()


    def _set_winner(self):
        p = self.board.get_winner()
        self.winner = self.next_player ^ p



if __name__ == '__main__':
    import random

    g = Geister()

    rs = random.sample
    r = range(8)

    red0, red1 = rs(r, 4), rs(r, 4)

    observe = g.reset(red0, red1)
    g.render()

    done = False
    while not done:
        a = random.choice(g.get_legal_actions())
        _, done = g.step(a)

    g.render()
    print(g.winner)

