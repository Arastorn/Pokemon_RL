# app/src/showdownai/team.py

from app.src.showdownai.pokemon import Pokemon

class Team():

    def __init__(self, list_of_pokemon):
        self.list_of_pokemon = list_of_pokemon
        self.pokemon_fighting = 0
