# -*- coding: utf-8 -*-
from . import main
from ..Game import Game
from ..GameModel import GameBoard, WordSetGenerator
from flask import render_template, flash, request
from flask_login import current_user
import json
from ..models import User

menu = {"home":["/homepage",u"我的主页",""],
        "join":["/join",u"加入",""]}

active_games = {}
user_game_mapping = {}

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
    # already has a game
    if user_game_mapping.has_key(current_user.id):
        flash(u'你已经有一盘游戏在进行中', 'success')
        return render_template('join.html', menu=menu, 
            game=active_games[user_game_mapping[current_user.id]], 
            gameid=user_game_mapping[current_user.id])
    else:
        print user_game_mapping
    # search a game
    game_id = request.args.get('id')
    if game_id:
        if active_games.has_key(int(game_id)):
            if active_games[int(game_id)].is_open():
                user_game_mapping[current_user.id] = long(game_id)
                active_games[int(game_id)].add_player(current_user.id, "red")
                return render_template('join.html', menu=menu, game=active_games[int(game_id)],gameid=int(game_id))
            else:
                flash(u'此游戏人已满', 'danger')
                return render_template('join.html', menu=menu)
        else:
            flash(u'你寻找的游戏不存在', 'danger')
            return render_template('join.html', menu=menu)

@main.route('/startgame')
def startgame():
    # already has a game
    if user_game_mapping.has_key(current_user.id):
        flash(u'你已经有一盘游戏在进行中', 'success')
        return render_template('join.html', menu=menu, game=active_games[current_user.id], gameid=current_user.id)
    
    # create a new game and initialize
    wsg = WordSetGenerator("./data/TestText")
    game = Game("./data/TestText")
    game.reset_game()
    game.add_player(current_user.id, "blue")
    active_games[current_user.id] = game
    user_game_mapping[current_user.id] = current_user.id
    game.start_game()
    return render_template('join.html', menu=menu, game=game, gameid=current_user.id)

@main.route('/lzstart')
def lzstartgame():
    return

@main.route('/clearall')
def clearall():
    active_games.clear()
    user_game_mapping.clear()
    flash(u'已关闭所有游戏', 'success')
    return render_template('join.html', menu=menu)

@main.route('/quitgame')
def quitgame():
    if active_games.has_key(current_user.id):
        for p in active_games[current_user.id].blue_team.players:
            user_game_mapping.pop(p)
        for p in active_games[current_user.id].red_team.players:
            user_game_mapping.pop(p)
        active_games[current_user.id].drop_player(current_user.id)
        active_games.pop(current_user.id)
    else:
        active_games[user_game_mapping[current_user.id]].drop_player(current_user.id)
        user_game_mapping.pop(current_user.id)

    flash(u'已退出当前游戏', 'success')
    return render_template('join.html', menu=menu)

@main.route('/showallgames')
def showallgames():
    if len(active_games.keys()) == 0:
        flash(u'目前还没有游戏', 'danger')
    return render_template('join.html', menu=menu, all_games=active_games.keys())

@main.route('/update')
def update():
    print user_game_mapping
    print active_games
    if not user_game_mapping.has_key(current_user.id):
        return json.dumps({})
    gameid = user_game_mapping[current_user.id]
    dic = {}
    dic["players"] = []
    for p in active_games[gameid].blue_team.players:
        un = User.query.get(int(p)).username
        dic["players"].append(un)

    for p in active_games[gameid].red_team.players:
        un = User.query.get(int(p)).username
        dic["players"].append(un)
    print dic["players"]
    return json.dumps(dic)

def activate(name=None):
    for key in menu:
        menu[key][2] = ""
    if name is not None:
        menu[name][2] = "active"
