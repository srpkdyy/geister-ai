import numpy as np


class Geister:
    N_ACTION = 144

    def __init__(self):
        self.board = None
        self.next_player = None
        self.turn = 0
        self.done = False
        self.winner = None

    def reset(self, red1, red2):
        self.board = Board()
        self.next_player = 0
        self.turn = 0
        self.done = False
        self.winner = None
        return self

    def update(self, state, turn):
        self.board = Board(state)
        self.next_player = 0
        self.turn = turn
        self.done = False
        self.winner = None
        return self
    
    def set_red(self, unit_names):
        board.set_red(unit_names, self.next_player)
        return self

    def change_side(self):
        self.next_player ^= 1
        self.board.swap()
        return self

    def step(self, action):
        assert 0 <= action < N_ACTION

        self.turn += 1

        board.move(action, self.next_player)



    def observe(self):
        return self.board.get_board(self.next_player)

    def legal_action(self):
        return [board.can_act(i) for i in range(N_ACTION)]


