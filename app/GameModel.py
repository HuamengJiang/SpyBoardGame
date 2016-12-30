from sets import Set
# from enum import Enum
import random
import os

# Role = Enum('TRAP', 'RED', 'BLUE', 'NEUTRAL')
class Role:
    TRAP = "trap"
    BLUE = "blue"
    RED = "red"
    NEUTRAL = "neutral"

class GameBoard:
    def __init__(self, n=5, m=5):
        self.n = n
        self.m = m
        self.board = [["" for i in range(m)] for j in range(n)]
        self.tiling = [[[Role.NEUTRAL, False] for i in range(m)] for j in range(n)]

    def reset_board(self, word_set):
        self.construct_main_board(word_set)
        self.construct_tiling()

    def construct_main_board(self, word_set):
        word_list = list(word_set)
        for i in range(self.n):
            for j in range(self.m):
                self.board[i][j] = word_list[i * self.m + j]
        return

    # decide what each tile is (NEUTRAL, BLUE, RED, black)
    def construct_tiling(self):
        self.trap_tiles = self.n * self.m % 3
        base_tile_count = self.n * self.m / 3
        self.blue_tiles = self.red_tiles = base_tile_count
        # randomly decide who moves first
        if random.randint(0, 1):
            self.current_turn = Role.BLUE
            self.blue_tiles += 1
        else:
            self.current_turn = Role.RED
            self.red_tiles += 1

        # TODO: now randomly assign tiling
        tiling_sequence = []
        tiling_sequence += [Role.TRAP for i in range(self.trap_tiles)]
        tiling_sequence += [Role.BLUE for i in range(self.blue_tiles)]
        tiling_sequence += [Role.RED for i in range(self.red_tiles)]
        tiling_sequence += [Role.NEUTRAL for i in range(base_tile_count - 1)]
        sequence = random.shuffle(tiling_sequence)
        board_size = self.n * self.m
        for i in range(self.n):
            for j in range(self.m):
                self.tiling[i][j][0] = tiling_sequence[i * self.m + j]

    # when a guess is made, reveal a tile, returns if there is a turn change
    def reveal_tile(self, x, y):
        [status, revealed] = self.tiling[x][y]
        if revealed:
            return 0
        self.tiling[x][y] = [status, True]
        if status:
            if status == Role.BLUE:
                self.blue_tiles -= 1
            elif status == Role.RED:
                self.red_tiles -= 1
        else:
            # game over
            self.current_turn = Role.TRAP
            return 2

        if status == self.current_turn:
            return 0
        else:
            self.switch_turn()
            if is_game_over():
                return 2
            # change turn
            return 1

    def is_game_over(self):
        return self.current_turn == Role.TRAP or blue_tiles == 0 \
            or red_tiles == 0

    def switch_turn(self):
        if self.current_turn == Role.RED:
            self.current_turn = Role.BLUE
        else:
            self.current_turn = Role.RED

    def terminate_game(self):
        self.current_turn = Role.TRAP;

class WordSetGenerator:
    def __init__(self, filename):
        self.set_word_source(filename)
        self.reset_word_pool()

    def set_word_source(self, filename):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, filename)
        f = open(filename, 'r')
        self.words = f.readlines()
        f.close()
        self.source_size = len(self.words)

    def gen_word_set(self, set_size, unique = True):
        word_set = Set()
        while len(word_set) < set_size:
            print len(word_set)
            index = random.randint(0, self.source_size - 1)
            word = self.words[index]
            print word
            if unique:
                if word not in self.word_pool:
                    word_set.add(word)
            else:
                word_set.add(word)
            # TODO: it doesn't matter if Set is multiset, but be sure about the behavior for simple set
            self.word_pool.add(word)
        return word_set

    # We will need to do this when we have exhausted all the words in
    # our source.
    def reset_word_pool(self):
        self.word_pool = Set()

def main():
    wsg = WordSetGenerator("./data/TestText")
    g = GameBoard()
    g.construct_main_board(wsg.gen_word_set(g.n * g.m))
    g.construct_tiling()
    for i in range(g.n):
        print g.tiling[i]

if __name__ == "__main__":
    main()
