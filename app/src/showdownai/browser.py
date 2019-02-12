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
        time.sleep(1)
        print("Logging in...")
        elem = self.driver.find_element_by_name("login")
        elem.click()
        time.sleep(1)
        user = self.driver.find_element_by_name("username")
        user.send_keys(username)
        user.send_keys(Keys.RETURN)
        while not self.check_exists_by_name("password"):
            time.sleep(1)
        passwd = self.driver.find_element_by_name("password")
        passwd.send_keys(password)
        passwd.send_keys(Keys.RETURN)
        time.sleep(1)


    def choose_tier(self, tier='gen7ou'):
        try:
            print("Selecting tier...")
            while not self.check_exists_by_css_selector(".select.formatselect"):
                time.sleep(1)
            form = self.driver.find_element_by_css_selector(".select.formatselect")
            form.click()
            time.sleep(2)
            #self.driver.save_screenshot('ou.png')
            tier = self.driver.find_element_by_css_selector("[name='selectFormat'][value='%s']" % tier)
            tier.click()
        except:
            raise TierException()


    def start_ladder_battle(self):
        print("Starting ladder battle!")
        url1 = self.driver.current_url
        battle = self.driver.find_element_by_css_selector(".button.big")
        battle.click()
        battle_click = True
        time.sleep(1)
        if url1 == self.driver.current_url and self.check_exists_by_name("username"):
            ps_overlay = self.driver.find_element_by_xpath("/html/body/div[4]")
            ps_overlay.click()
            battle_click = False
        while url1 == self.driver.current_url and self.check_exists_by_name("login"):
            time.sleep(1)
        if url1 == self.driver.current_url and not battle_click:
            battle = self.driver.find_element_by_css_selector(".button.big")
            battle.click()
            time.sleep(1)
        while url1 == self.driver.current_url:
            time.sleep(1.5)


    def start_challenge_battle(self, name, tier='gen7ou'):
        print("Starting challenge battle!")

        findUser = self.driver.find_element_by_css_selector(".button.mainmenu5.onlineonly")
        findUser.click()
        time.sleep(2)
        if self.check_exists_by_css_selector(".textbox.autofocus"):
            userBox = self.driver.find_element_by_css_selector(".textbox.autofocus")
            userBox.send_keys(name)
            userBox.send_keys(Keys.RETURN)
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
        tier = self.driver.find_element_by_css_selector("[name='selectFormat'][value='gen7ou']")
        tier.click()
        time.sleep(2)

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
        builder = self.driver.find_element_by_css_selector(".button[value='teambuilder']")
        builder.click()
        new_team = self.driver.find_element_by_css_selector("[name='newTop']")
        new_team.click()
        time.sleep(3)
        import_button = self.driver.find_element_by_css_selector(".button.big[name='import']")
        import_button.click()
        textfield = self.driver.find_element_by_css_selector(".teamedit .textbox")
        textfield.send_keys(team)
        save = self.driver.find_element_by_css_selector(".savebutton[name='saveImport']")
        save.click()
        # On click sur le format OU
        while not self.check_exists_by_css_selector(".teambuilderformatselect"):
            time.sleep(1)
        formatSelect = self.driver.find_element_by_css_selector(".teambuilderformatselect")
        formatSelect.click()
        time.sleep(2)
        format = self.driver.find_element_by_css_selector("[name='selectFormat'][value='gen7ou']")
        format.click()

        validate = self.driver.find_element_by_css_selector(".button[name='validate']")
        validate.click()

        while not self.check_exists_by_css_selector(".autofocus"):
            time.sleep(1)
        buttonOk = self.driver.find_element_by_css_selector(".autofocus")
        buttonOk.click()
        time.sleep(2)
        #self.screenshot('log.png')
        close_button = self.driver.find_element_by_css_selector(".closebutton[name='closeRoom']")
        close_button.click()
        #self.screenshot('log.png')
        time.sleep(2)


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
                save_replay = self.driver.find_element_by_css_selector("[name='saveReplay']")
                save_replay.click()
                while not self.check_exists_by_id(self.get_battle_id()):
                    time.sleep(1)
                ps_overlay = self.driver.find_element_by_css_selector(".ps-overlay")
                ps_overlay.click()
                raise GameOverException()


    def start_timer(self):
        if self.check_exists_by_name("openTimer"):
            timer = self.driver.find_element_by_name("openTimer")
            if timer.text == "Timer":
                timer.click()
                if self.check_exists_by_name("timerOn"):
                    startTimerButton = self.driver.find_element_by_name("timerOn")
                    print("Starting timer...")
                    startTimerButton.click()
                    self.timer_on = True


    def random_Attack(self):
        print("Making a move...")
        if (self.check_alive()) and (self.check_exists_by_css_selector(".movemenu")):
            if self.check_exists_by_name('megaevo'):
                mega_button = self.driver.find_element_by_name('megaevo')
                mega_button.click()
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
        img = self.driver.find_elements_by_css_selector(".battle img")[6]
        text = img.get_attribute('src')
        poke = text.split("/")[-1]
        poke = poke[:-4]
        print("my primary : ", poke)
        return poke


    def get_opponent_primary(self):
        img = self.driver.find_elements_by_css_selector(".battle img")[5]
        text = img.get_attribute('src')
        poke = text.split("/")[-1]
        poke = poke[:-4]
        print("opponent primary : ", poke)
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

    def check_alive(self):
        return self.check_exists_by_css_selector(".rstatbar")


    def chat(self, message):
        chatbox = self.driver.find_elements_by_css_selector(".chatbox .textbox")[-1]
        chatbox.send_keys(message)
        chatbox.send_keys(Keys.RETURN)


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
        sound = self.driver.find_element_by_css_selector(".icon[name='openSounds']")
        sound.click()
        mute = self.driver.find_element_by_css_selector("[name='muted']")
        mute.click()
