from sets import Set
import random

class GameBoard:
    def __init__(self, n=5, m=5):
        self.n = n
        self.m = m
        self.word_set = Set()
        # necessary if a game with nonrepetitive vocabulary set is required.
        self.word_pool = Set()
        self.board = [["" for i in range(m)] for j in range(n)]
        self.tiling = [[[0, False] for i in range(m)] for j in range(n)]
        return

    def construct_word_set(self, filename, unique):
        f = open(filename, 'r')
        words = f.readlines()
        for i in range(n):
            for j in range(m):
                word = words[blah]
                if self.word_pool.has_key():
                    self.word_set.update(word)
                self.word_pool.update(word)
        return

    def reset_board(self):
        self.construct_main_board()
        self.construct_tiling()

    def construct_main_board(self):
        word_list = list(self.word_set)
        for i in range(n):
            for j in range(m):
                self.board[i][j] = word_list[i * m + j]
        return

    # decide what each tile is (neutral, blue, red, black)
    def construct_tiling(self):
        self.trap_tiles = n * m % 3
        base_tile_count = n * m / 3
        self.blue_tiles = self.red_tiles = base_tile_count
        # randomly decide who moves first
        if random.randint(0, 1):
            self.current_turn = 1
            self.blue_tiles += 1
        else:
            self.current_turn = -1
            self.red_tiles += 1

        # TODO: now randomly assign tiling
        return

    # We will need to do this when we have exhausted all the words in
    # our source.
    def reset_word_pool(self):
        self.word_pool = Set()

    # when a guess is made, reveal a tile, returns if there is a turn change
    def reveal_tile(self, x, y):
        [status, revealed] = self.tiling[x][y]
        if revealed:
            return 0
        self.tiling[x][y] = [status, True]
        if status:
            if status > 0:
                self.blue_tiles -= 1
            else:
                self.red_tiles -= 1
        else:
            # game over
            self.current_turn = 0
            return 2

        if status == self.current_turn:
            return 0
        else:
            self.current_turn *= -1
            if is_game_over():
                return 2
            # change turn
            return 1

    def is_game_over(self):
        return self.current_turn == 0 or blue_tiles == 0 or red_tiles == 0
