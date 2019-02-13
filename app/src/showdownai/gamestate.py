# app/src/showdownai/gamestate.py

from app.src.showdownai.team import Team

class GameState():

    def __init__(self,my_team,opponent_team):
        self.my_team = my_team
        self.opponent_team = opponent_team
