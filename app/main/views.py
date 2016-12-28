# -*- coding: utf-8 -*- 
from . import main
from flask import render_template

@main.route('/')
def index():
    words = ['word1','word2','word3','word4','word5']
    return render_template('index.html',items=words)

# @main.route('/static/<filename>')
# def file(filename):
# 	return app.send_static_file(filename)