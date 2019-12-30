import numpy as np


class Model:
    def __init__(self):
        self.h_color = None
        self.board = None
        self.winner = None
        self.next_player = None

        self.lines = []
        self.lines.append([(0, 0), (0, 1), (0, 2)])
        self.lines.append([(1, 0), (1, 1), (1, 2)])
        self.lines.append([(2, 0), (2, 1), (2, 2)])
        self.lines.append([(0, 0), (1, 0), (2, 0)])
        self.lines.append([(0, 1), (1, 1), (2, 1)])
        self.lines.append([(0, 2), (1, 2), (2, 2)])
        self.lines.append([(0, 0), (1, 1), (2, 2)])
        self.lines.append([(0, 2), (1, 1), (2, 0)])

    def start_game(self, h_color: str):
        self.h_color = h_color
        self.board = np.full((3, 3), ".")
        self.winner = None
        self.next_player = "black"

    @property
    def over(self):
        return self.winner is not None

    @property
    def turn(self):
        return np.where(self.board == "o", 1, 0).sum() + np.where(self.board == "x", 1, 0).sum()

    @property
    def is_next_human(self):
        return self.h_color == self.next_player

    def is_legal(self, y, x):
        return self.board[y, x] == "."

    def move(self, y, x):
        if self.next_player == "black":
            self.board[y, x] = "o"
            self.next_player = "white"
        else:
            self.board[y, x] = "x"
            self.next_player = "black"
        self.check_game_over()

    def move_by_ai(self):
        p = np.where(self.board.reshape(-1) == ".", 1, 0).astype(float)
        p /= np.sum(p)
        i = np.random.choice(9, 1, p=p)
        y, x = i // 3, i % 3
        self.move(y, x)

    def check_game_over(self):

        for line in self.lines:
            s = "".join([self.board[y, x] for y, x in line])
            if s == "ooo":
                self.winner = "black"
                return
            if s == "xxx":
                self.winner = "white"
                return
        if self.turn >= 9:
            self.winner = "draw"
