from app.src.showdownai.browser import Selenium
from app.src.showdownai.gamestate import GameState
from app.src.showdownai.pokemon import Pokemon
from app.src.showdownai.team import Team
from app.src.showdownai.exceptions import *
from path import Path

import time
import sys
import os
import platform
import signal
import requests
import json
import re
import traceback


class Showdown():

    def __init__(self, team_text, username, password=None, proxy=False):
        self.username = username
        self.password = password
        self.team_text = team_text
        self.battle_url = None
        self.lib_dir = os.getcwd() + "/app/driver/"
        self.selenium = Selenium(proxy=proxy, browser='chrome', lib_dir=self.lib_dir)
        self.gamestate = None


    def reset(self):
        print("Resetting...")
        self.selenium.reset()


    def init(self):
        print("Initializing showdown")
        self.selenium.start_driver()
        self.selenium.clear_cookies()
        self.selenium.turn_off_sound()
        self.selenium.login(self.username, self.password)
        self.selenium.make_team(self.team_text)


    def parse_text_to_pokemon(self):
        #TODO
        pokemon = None
        return pokemon


    def parse_web_to_pokemon(self):
        #TODO
        pokemon = None
        return pokemon


    def create_team(self):
        #TODO
        team = None
        return team


    def string_list_to_team(self,string_list):
        team = []
        for string in string_list:
            team.append(Pokemon(string))
        team_of_pokemon = Team(team)
        return team_of_pokemon


    def set_initial_gamestate(self):
        my_team_string = self.selenium.get_my_team()
        my_team = self.string_list_to_team(my_team_string)
        opponent_team_string = self.selenium.get_opponent_team()
        opponent_team = self.string_list_to_team(opponent_team_string)
        self.gamestate = GameState(my_team,opponent_team)


    def change_current_gamestate(self):
        my_team_string = self.selenium.get_my_team()
        self.gamestate.set_my_primary(my_team_string)
        print(self.gamestate.get_my_primary())
        opponent_team_string = self.selenium.get_opponent_team()
        self.gamestate.set_opponent_primary(opponent_team_string)
        print(self.gamestate.get_opponent_primary())
        #print("health : " + str(self.selenium.get_my_primary_health()))
        #self.selenium.get_opponent_primary()
        #print("health : " + str(self.selenium.get_opponent_primary_health()))


    def play_game(self, challenge=None):
        print("Finding a game...")
        tier_click = False
        while not tier_click:
            try:
                if challenge:
                    self.selenium.start_challenge_battle(challenge)
                else:
                    self.selenium.choose_tier()
                    self.selenium.start_ladder_battle()
                tier_click = True
            except TierException:
                print("Unable to click tier. Trying again...")
            self.battle_url = self.selenium.driver.current_url
            print("Found game: ", self.battle_url)
            self.selenium.waiting_opponent_action()
            self.selenium.chat("gl hf!")
            self.set_initial_gamestate()
            self.gamestate.print_game_state()
            self.selenium.choose_pokemon_at_game_start(0)
            over = False
            while not over:
                print("==========================================================================================")
                self.change_current_gamestate()
                self.gamestate.print_game_state()
                print ("My move:")
                self.selenium.random_Attack()


    def print_game_log(self):
        chat_log = self.selenium.get_log()
        print("=============================================")
        print("Game log : ")
        print(chat_log)
        id = self.selenium.get_battle_id()
        battle_url = "http://replay.pokemonshowdown.com/battle-%s" % id
        print("=============================================")
        print("Finished game! Replay can be found at: ", battle_url)


    def run(self, num_games=1, challenge=None):
        if challenge:
            print("Set to challenge: %s" % challenge)
        else:
            print("Set to play %u games" % num_games)
        self.init()
        for i in range(num_games):
            result, error = None, None
            try:
                self.play_game(challenge=challenge)
            except GameOverException:
                print("Game " + i +" is over")
            except UserNotOnlineException:
                print("User not online: %s" % challenge)
                print("Exiting...")
                return
            except:
                error = traceback.format_exc()
                print("Error", error)
            self.print_game_log()
            self.reset()
        self.selenium.close()
        print("Done!")
