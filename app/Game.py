class Game:
    def __init__(self):
        self.board = GameBoard("./data/TestText")
        self.board.construct_word_set(True)
        self.board.construct_main_board()
        self.board.construct_tiling()
        # for i in range(g.n):
        #     print g.tiling[i]
        self.teams = []

     def is_open(self):
     	pass

     def add_player(self, color):
     	pass

     def start_game(self):
     	pass

     def terminate_game(self):
     	pass

     def switch_turn(self):
     	self.board.switch_turn()


class Team:
	self.color = ""
	self.players = []
	self.leader = None
