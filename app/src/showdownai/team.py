# app/src/showdownai/team.py

from app.src.showdownai.pokemon import Pokemon

class Team():

    def __init__(self, list_of_pokemon):
        self.list_of_pokemon = list_of_pokemon
        self.pokemon_fighting = 0


    def team_state(self):
        to_print = ""
        for pokemon in self.list_of_pokemon:
            to_print = to_print + ", " + pokemon.name
        print(to_print)


    def set_primary_pokemon_from_webstring(self,webstring):
        primary_pokemon = 0
        iterator = 0
        for string in webstring:
            if "(active)" in string:
                primary_pokemon = iterator
                print("ya un active !")
            iterator = iterator + 1
        self.pokemon_fighting = primary_pokemon


    def get_primary_pokemon(self):
        return self.list_of_pokemon[self.pokemon_fighting].name
