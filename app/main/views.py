# -*- coding: utf-8 -*-
from . import main
from ..Game import Game
from ..GameModel import GameBoard, WordSetGenerator
from flask import render_template, flash, request
from flask_login import current_user

menu = {"home":["/homepage",u"我的主页",""],
        "join":["/join",u"加入",""]}

active_games = {}

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
    if active_games.has_key(current_user.id):
        flash(u'你已经有一盘游戏在进行中', 'success')
        return render_template('join.html', menu=menu, game=active_games[current_user.id], gameid=current_user.id)

    game_id = request.args.get('id')
    if game_id:
        if active_games.has_key(int(game_id)):
            return render_template('join.html', menu=menu, game=active_games[int(game_id)],gameid=int(game_id))
        else:
            flash(u'你寻找的游戏不存在', 'danger')
            return render_template('join.html', menu=menu)

    if len(active_games):
        return render_template('join.html', menu=menu, game=active_games[active_games.keys()[0]],gameid=active_games.keys()[0])
    else:
        flash(u'没有可以加入的游戏', 'danger')
        return render_template('join.html', menu=menu)

@main.route('/startgame')
def startgame():
    if active_games.has_key(current_user.id):
        flash(u'你已经有一盘游戏在进行中', 'success')
        return render_template('join.html', menu=menu, game=active_games[current_user.id], gameid=current_user.id)
    wsg = WordSetGenerator("./data/TestText")
    game = Game("./data/TestText")
    game.reset_game()
    active_games[current_user.id] = game
    game.start_game()
    return render_template('join.html', menu=menu, game=game, gameid=current_user.id)

@main.route('/lzstart')
def lzstartgame():
    return

@main.route('/clearall')
def clearall():
    active_games.clear()
    flash(u'已关闭所有游戏', 'success')
    return render_template('join.html', menu=menu)

@main.route('/quitgame')
def quitgame():
    if active_games.has_key(current_user.id):
        active_games.pop(current_user.id)
    flash(u'已退出当前游戏', 'success')
    return render_template('join.html', menu=menu)

@main.route('/showallgames')
def showallgames():
    if len(active_games.keys()) == 0:
        flash(u'目前还没有游戏', 'danger')
    return render_template('join.html', menu=menu, all_games=active_games.keys())

@main.route('/update')
def update():
    return "nima"

def activate(name=None):
    for key in menu:
        menu[key][2] = ""
    if name is not None:
        menu[name][2] = "active"
