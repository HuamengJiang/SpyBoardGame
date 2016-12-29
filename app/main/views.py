# -*- coding: utf-8 -*- 
from . import main
from flask import render_template
from ..GameModel import GameBoard

menu = {"home":["/homepage",u"我的主页",""],
        "join":["/join",u"加入",""]}

@main.route('/')
def index():
    activate()
    return render_template('index.html',menu=menu)

@main.route('/homepage')
def homepage():
    activate("home")
    return render_template('home.html', menu=menu)

@main.route('/join')
def join():
    activate("join")
    return render_template('join.html', menu=menu)

@main.route('/findgame')
def findgame():
    board = GameBoard()
    board.construct_word_set("TestText", True)
    board.construct_main_board()
    return render_template('join.html', menu=menu, board=board)

def activate(name=None):
    for key in menu:
        menu[key][2] = ""
    if name is not None:
        menu[name][2] = "active"