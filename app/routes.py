# app/views.py

from flask import Flask, jsonify, send_from_directory, render_template
from webargs import fields
from webargs.flaskparser import use_args
from threading import Thread, Timer
from path import Path

from app import app
from app.main import fichier

play_game_args = {
'iterations': fields.Int( default=1),
'username': fields.Str(required=True),
'password': fields.Str(required=True),
'teamfile':fields.Str(required=True),
'challenge': fields.Str(default=None),
'browser': fields.Str(default="chrome"),
}

@app.route('/')
def index():
    files = fichier.get_team_files()
    return render_template('index.html', teamfiles=files)


@app.route("/api/play_game", methods=['get', 'post'])
@use_args(play_game_args)
def play_game(args):
    team_text = (Path("teams") / args['teamfile']).text()
    """showdown = Showdown(
    team_text,
    PessimisticMinimaxAgent(2, self.pokedata),
    args['username'],
    self.pokedata,
    browser=args['browser'],
    password=args['password'],
    )
    id = self.run_showdown(showdown, args)
    response = {'id': id}"""
    return jsonify(**args)

    #@app.route("/api/shodown/<int:id>", methods=['get'])
