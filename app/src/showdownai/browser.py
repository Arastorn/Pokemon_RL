import time
import re
import random

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from app.src.showdownai.exceptions import *


class Selenium():

    BASE_URL="http://play.pokemonshowdown.com"

    def __init__(self, url=BASE_URL, timer_on=False, proxy=False, browser='chrome', lib_dir="app/lib/linux64/"):
        self.url = url
        self.timer_on = timer_on
        self.browser = browser
        self.lib_dir = lib_dir
        chrome_path = self.lib_dir + "chromedriver"
        self.driver = webdriver.Chrome(executable_path=chrome_path)


    def start_driver(self):
        print("Starting driver...")
        self.driver.get(self.url)


    def get_state(self):
        url = self.driver.current_url
        if "battle" in url:
            return "battle"
        else:
            return "lobby"


    def wait_home_page(self):
        print("Waiting for home page to load...")
        while self.driver.find_element_by_css_selector(".select.formatselect").get_attribute('value') != "gen7randombattle":
            time.sleep(1)


    def login(self, username, password):
        self.wait_home_page()
        print("Logging in...")
        self.click_on_element_name("login")
        self.write_in_element_name("username",username)
        while not self.check_exists_by_name("password"):
            time.sleep(1)
        self.write_in_element_name("password",password)


    def choose_tier(self, tier='gen7ou'):
        try:
            print("Selecting tier...")
            while not self.check_exists_by_css_selector(".select.formatselect"):
                time.sleep(1)
            self.click_on_element_css(".select.formatselect")
            self.click_on_element_css("[name='selectFormat'][value='%s']" % tier)
        except:
            raise TierException()


    def start_ladder_battle(self):
        print("Starting ladder battle!")
        url = self.driver.current_url
        self.click_on_element_css(".button.big")
        battle_click = True
        if url == self.driver.current_url and self.check_exists_by_name("username"):
            ps_overlay = self.driver.find_element_by_xpath("/html/body/div[4]")
            ps_overlay.click()
            battle_click = False
        while url == self.driver.current_url and self.check_exists_by_name("login"):
            time.sleep(1)
        if url == self.driver.current_url and not battle_click:
            self.click_on_element_css(".button.big")
        while url == self.driver.current_url:
            time.sleep(1.5)


    def start_challenge_battle(self, name, tier='gen7ou'):
        print("Starting challenge battle!")
        self.click_on_element_css(".button.mainmenu5.onlineonly")
        if self.check_exists_by_css_selector(".textbox.autofocus"):
            self.write_in_element_css(".textbox.autofocus",name)
        else:
           print("%s is not online...exiting now" % name)
           raise UserNotOnlineException()
        time.sleep(3)
        #ps_overlay = self.driver.find_element_by_xpath("/html/body/div[4]")
        #challenge = ps_overlay.find_element_by_css_selector("[name='pm']")
        #challenge.click()
        #time.sleep(2)
        print("Waiting for user to click on challenge !")
        while not self.check_exists_by_css_selector(".challenge"):
            time.sleep(1)
        challengeWindow = self.driver.find_element_by_css_selector(".challenge")
        formatCombat = challengeWindow.find_element_by_css_selector(".select.formatselect")
        formatCombat.click()
        time.sleep(2)
        self.click_on_element_css("[name='selectFormat'][value='gen7ou']")
        make_challenge = challengeWindow.find_element_by_css_selector("[name='makeChallenge']")
        make_challenge.click()
        print("Sent a challenge!")


    def get_battle_id(self):
        url = self.driver.current_url
        url_list = url.split('-')
        id = url_list[-2:]
        return '-'.join(id)


    def make_team(self, team):
        print("Making team...")
        self.click_on_element_css(".button[value='teambuilder']")
        self.click_on_element_css("[name='newTop']")
        self.click_on_element_css(".button.big[name='import']")
        textfield = self.driver.find_element_by_css_selector(".teamedit .textbox")
        textfield.send_keys(team)
        self.click_on_element_css(".savebutton[name='saveImport']")
        # On click sur le format OU
        while not self.check_exists_by_css_selector(".teambuilderformatselect"):
            time.sleep(1)
        self.click_on_element_css(".teambuilderformatselect")
        self.click_on_element_css("[name='selectFormat'][value='gen7ou']")
        self.click_on_element_css(".button[name='validate']")
        while not self.check_exists_by_css_selector(".autofocus"):
            time.sleep(1)
        self.click_on_element_css(".autofocus")
        self.click_on_element_css(".closebutton[name='closeRoom']")


    def waiting_opponent_action(self):
        print("Waiting opponent action...")
        move_exists = self.check_exists_by_css_selector(".movemenu") or self.check_exists_by_css_selector(".switchmenu")
        while move_exists == False:
            try:
                time.sleep(2)
                #self.start_timer()
            except:
                pass
            time.sleep(2)
            move_exists = self.check_exists_by_css_selector(".movemenu") or self.check_exists_by_css_selector(".switchmenu")
            if self.check_exists_by_css_selector("[name='saveReplay']"):
                self.chat("gg")
                self.click_on_element_css("[name='saveReplay']")
                while not self.check_exists_by_id(self.get_battle_id()):
                    time.sleep(1)
                self.click_on_element_css(".ps-overlay")
                raise GameOverException()


    def start_timer(self):
        if self.check_exists_by_name("openTimer"):
            timer = self.driver.find_element_by_name("openTimer")
            if timer.text == "Timer":
                timer.click()
                if self.check_exists_by_name("timerOn"):
                    print("Starting timer...")
                    self.click_on_element_name("timerOn")
                    self.timer_on = True


    def random_Attack(self):
        print("Making a move...")
        if (self.check_alive()) and (self.check_exists_by_css_selector(".movemenu")):
            if self.check_exists_by_name('megaevo'):
                self.click_on_element_name("megaevo")
            attacks = self.driver.find_elements_by_css_selector(".movemenu button")
            if(len(attacks)>0):
                randomAttack = random.randint(1,len(attacks)-1)
                self.attack_Information(attacks[randomAttack])
                attacks[randomAttack].click()
        else:
            self.switch_pokemon_random()
        self.waiting_opponent_action()


    def attack_Information(self, attack):
        attack_name = attack.get_attribute("data-move")
        type = attack.find_element_by_css_selector(".type").text
        pp = attack.find_element_by_css_selector(".pp").text
        print("Attack used : ", attack_name)
        print("Type of the attack : ", type)
        print("pp left on the attack : ", pp)


    def choose_pokemon_at_game_start(self, index):
        print("Choosing first Pokemon...")
        choose = self.driver.find_elements_by_name("chooseTeamPreview")[index]
        choose.click()
        self.waiting_opponent_action()


    def switch_pokemon_random(self):
        print("Switching Pokemon Randomly...")
        switchMenu = self.driver.find_element_by_css_selector(".switchmenu")
        pokemonsAvailable = switchMenu.find_elements_by_css_selector("[name='chooseSwitch']")
        # Take a random number of PokemonsAvailable
        print(len(pokemonsAvailable))
        if(len(pokemonsAvailable) > 0 ):
            randomPokemon = random.randint(1,len(pokemonsAvailable)-1)
            pokemonsAvailable[randomPokemon].click()


    def get_my_primary(self):
        if self.check_exists_by_css_selector(".rstatbar strong"):
            text = self.driver.find_element_by_css_selector(".rstatbar strong").text
            poke = text
            return poke


    def get_opponent_primary(self):
        if self.check_exists_by_css_selector(".lstatbar strong"):
            text = self.driver.find_element_by_css_selector(".lstatbar strong").text
            poke = text
            return poke


    def get_my_primary_health(self):
        if self.check_exists_by_css_selector(".rstatbar .hpbar .hptext"):
            hp_text = self.driver.find_element_by_css_selector(".rstatbar .hpbar .hptext")
            hp = hp_text.text.strip("%")
            hp = int(hp)
        else:
            hp = 0
        return hp


    def get_opponent_primary_health(self):
        if self.check_exists_by_css_selector(".lstatbar .hpbar .hptext"):
            hp_text = self.driver.find_element_by_css_selector(".lstatbar .hpbar .hptext")
            hp = hp_text.text.strip("%")
            hp = int(hp)
        else:
            hp = 0
        return hp


    def get_my_team(self):
        if self.check_exists_by_css_selector(".leftbar .trainer .teamicons"):
            my_team_element = self.driver.find_elements_by_css_selector(".leftbar .trainer .teamicons span")
            my_team = []
            for element in my_team_element:
                pokemon_name = element.get_attribute("title")
                my_team.append(pokemon_name)
            return my_team


    def get_opponent_team(self):
        if self.check_exists_by_css_selector(".rightbar .trainer .teamicons"):
            my_team_element = self.driver.find_elements_by_css_selector(".rightbar .trainer .teamicons span")
            my_team = []
            for element in my_team_element:
                pokemon_name = element.get_attribute("title")
                my_team.append(pokemon_name)
            return my_team

    def check_alive(self):
        return self.check_exists_by_css_selector(".rstatbar")


    def chat(self, message):
        chatbox = self.driver.find_elements_by_css_selector(".chatbox .textbox")[-1]
        chatbox.send_keys(message)
        chatbox.send_keys(Keys.RETURN)


    def click_on_element_name(self,element):
        try:
            self.driver.find_element_by_name(element).click()
            time.sleep(1)
        except NoSuchElementException:
            print("Element : " + element + " Not Found")


    def click_on_element_css(self,element):
        try:
            self.driver.find_element_by_css_selector(element).click()
            time.sleep(1)
        except NoSuchElementException:
            print("Element : " + element + " Not Found")

    def write_in_element_name(self,element,stringToWrite):
        try:
            elem = self.driver.find_element_by_name(element)
            elem.send_keys(stringToWrite)
            elem.send_keys(Keys.RETURN)
            time.sleep(1)
        except NoSuchElementException:
            print("Element : " + element + " Not Found")

    def write_in_element_css(self,element,stringToWrite):
        try:
            elem = self.driver.find_element_by_css_selector(element)
            elem.send_keys(stringToWrite)
            elem.send_keys(Keys.RETURN)
            time.sleep(1)
        except NoSuchElementException:
            print("Element : " + element + " Not Found")

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True


    def check_exists_by_id(self, id):
        try:
            self.driver.find_element_by_id(id)
        except NoSuchElementException:
            return False
        return True


    def check_exists_by_name(self, name):
        try:
            self.driver.find_element_by_name(name)
        except NoSuchElementException:
            return False
        return True


    def check_exists_by_class(self, cls):
        try:
            self.driver.find_elements_by_class_name(cls)
        except NoSuchElementException:
            return False
        return True


    def check_exists_by_css_selector(self, css, elem=None):
        try:
            if elem:
                result = elem.find_elements_by_css_selector(css)
            else:
                result = self.driver.find_elements_by_css_selector(css)
            return len(result) > 0
        except NoSuchElementException:
            return False


    def get_log(self):
        log = self.driver.find_element_by_css_selector(".battle-log")
        return log.text.encode('utf-8')


    def reset(self):
        self.driver.get(self.url)
        time.sleep(2)


    def close(self):
        self.driver.close()


    def clear_cookies(self):
        self.driver.execute_script("localStorage.clear();")


    def turn_off_sound(self):
        print("Turning off sound...")
        self.click_on_element_css(".icon[name='openSounds']")
        self.click_on_element_css("[name='muted']")
