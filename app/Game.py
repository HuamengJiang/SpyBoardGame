from GameModel import WordSetGenerator, GameBoard

class Game:
    def __init__(self, filename):
        self.wsg = WordSetGenerator(filename)
        self.board = GameBoard()
        self.team_capacity = 1
        self.blue_team = Team()
        self.blue_team.color = "blue";
        self.red_team = Team()
        self.red_team.color = "red";
        self.is_running = False

    def is_open(self):
        return len(self.red_team.players) < self.team_capacity or \
            len(self.blue_team.players) < self.team_capacity


    def is_running(self):
        return self.is_running

    def reset_word_source(self, filename):
        self.wsg.reset_word_source(filename)

    def reset_word_pool(self):
        self.wsg.reset_word_pool()

    def add_player(self, id, color):
        if color == "red":
            if len(self.red_team.players) == self.team_capacity:
                return
            self.red_team.players += [id]
            if not self.red_team.leader:
                self.red_team.leader = id
        elif color == "blue":
            if len(self.blue_team.players) == self.team_capacity:
                return
            self.blue_team.players += [id]
            if not self.blue_team.leader:
                self.blue_team.leader = id

    def drop_player(self, id):
        if id in self.red_team.players:
            self.red_team.players.remove(id)
            if id == self.red_team.leader:
                self.red_team.leader = None
        if id in self.blue_team.players:
            self.blue_team.players.remove(id)
            if id == self.blue_team.leader:
                self.blue_team.leader = None

    def reset_game(self):
        self.is_running = False
        self.board.reset_board(
            self.wsg.gen_word_set(self.board.n * self.board.m))

    def start_game(self):
        self.is_running = True;

    def terminate_game(self):
        self.is_running = False;
        self.board.terminate_game()

    def switch_turn(self):
    	self.board.switch_turn()


class Team:
	color = ""
	players = []
	leader = None
