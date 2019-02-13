# app/src/showdownai/gamestate.py

from app.src.showdownai.team import Team

class GameState():

    def __init__(self,my_team,opponent_team):
        self.my_team = my_team
        self.opponent_team = opponent_team

    def set_my_primary(self,webstring):
        self.my_team.set_primary_pokemon_from_webstring(webstring)


    def set_opponent_primary(self,webstring):
        self.opponent_team.set_primary_pokemon_from_webstring(webstring)


    def get_my_primary(self):
        return self.my_team.get_primary_pokemon()


    def get_opponent_primary(self):
        return self.opponent_team.get_primary_pokemon()


    def print_game_state(self):
        print("GameState : ")
        my_primary = self.my_team.get_primary_pokemon()
        print("My primary : " + my_primary.name + " health : " + str(my_primary.hp))
        opponent_primary = self.opponent_team.get_primary_pokemon()
        print("Opponent primary : " + opponent_primary.name + " health : " + str(opponent_primary.hp))
