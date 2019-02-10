# app/routes.py

from flask import Flask, jsonify, send_from_directory, render_template
from webargs import fields
from webargs.flaskparser import use_args
from threading import Thread, Timer
from path import Path

from app import app
from app.src.fichier import fichier
from app.src.showdownai.showdown import Showdown

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
    showdown = Showdown(
    team_text,
    args['username'],
    args['browser'],
    args['password'],
    )
    Thread(target=showdown.run, args=(args['iterations'],),
            kwargs={
                'challenge': args['challenge']
            }).start()
    response = {'id': id}
    return jsonify(**response)

    #@app.route("/api/shodown/<int:id>", methods=['get'])
