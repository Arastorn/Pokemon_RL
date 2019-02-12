from app.src.showdownai.browser import Selenium
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


    def __init__(self, team_text, username, password=None, proxy=False, browser='chrome'):
        self.username = username
        self.password = password
        self.team_text = team_text
        self.battle_url = None
        self.opp_team = None
        self.lib_dir = os.getcwd() + "/app/driver/"
        self.selenium = Selenium(proxy=proxy, browser=browser, lib_dir=self.lib_dir)


    def reset(self):
        print("Resetting...")
        self.selenium.reset()
        self.opp_team = None


    def init(self):
        print("Initializing showdown")
        self.selenium.start_driver()
        self.selenium.clear_cookies()
        self.selenium.turn_off_sound()
        self.selenium.login(self.username, self.password)
        self.selenium.make_team(self.team_text)


    def current_state(self):
        print("State of the game :")
        print("My pokemon : " + self.selenium.get_my_primary() + " health : " +  self.selenium.get_my_primary_health())
        print("Opponent pokemon : " + self.selenium.get_opponent_primary() + " health : " + self.selenium.get_opponent_primary_health())


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
            self.selenium.wait_for_move()
            self.selenium.chat("gl hf!")
            self.selenium.choose_pokemon_at_game_start(0)
            over = False
            while not over:
                print("==========================================================================================")
                #self.current_state()
                print ("My move:")
                self.selenium.random_Attack()


    def run(self, num_games=1, challenge=None):
        if challenge:
            print("Set to challenge: %s", challenge)
        else:
            print("Set to play %u games", num_games)
        self.init()
        def signal_handler(signal, frame):
            sys.exit(0)
        #signal.signal(signal.SIGINT, signal_handler)
        for i in range(num_games):
            result, error = None, None
            try:
                self.play_game(challenge=challenge)
            except GameOverException:
                print("GameOverException")
            except UserNotOnlineException:
                print("User not online: %s" % challenge)
                print("Exiting...")
                return
            except:
                error = traceback.format_exc()
                print("Error", error)
            chat_log = self.selenium.get_log()
            print("=============================================")
            print("Game log : ")
            print(chat_log)
            id = self.selenium.get_battle_id()
            battle_url = "http://replay.pokemonshowdown.com/battle-%s" % id
            print("=============================================")
            print("Finished game! Replay can be found at: ", battle_url)
            self.reset()
        self.selenium.close()
        print("Done!")
