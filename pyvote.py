#!/usr/bin/env python3
# Leonardo José Zanotti
# https://github.com/LeonardoZanotti/pyvote

import json
import os
import platform
import sys
import unittest
from datetime import datetime
from random import randint, randrange, uniform
from time import sleep, time

import numpy as np
import scipy.interpolate as si
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def cpf():
    def calculate_number(digs):
        s = 0
        qtd = len(digs)
        for i in range(qtd):
            s += n[i] * (1+qtd-i)
        res = 11 - s % 11
        if res >= 10:
            return 0
        return res
    n = [randrange(10) for i in range(9)]
    n.append(calculate_number(n))
    n.append(calculate_number(n))
    return "%d%d%d.%d%d%d.%d%d%d-%d%d" % tuple(n)


# Colors to outputs
BGreen = "\033[1;32m"  # Bold Green
BYellow = "\033[1;33m"  # Bold Yellow
BPurple = "\033[1;35m"  # Bold Purple
Yellow = "\033[0;33m"  # Yellow
Blue = "\033[0;34m"  # Blue
Green = "\033[0;32m"  # Green
Red = "\033[0;31m"  # Red

# Randomization Related
MIN_RAND = 0.64
MAX_RAND = 1.27
LONG_MIN_RAND = 4.78
LONG_MAX_RAND = 11.1

# Update this list with proxybroker http://proxybroker.readthedocs.io
PROXY = [
    {"host": "34.65.217.248", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                   "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.15, "error_rate": 0.0},
    {"host": "198.46.160.38", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                   "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.36, "error_rate": 0.0},
    {"host": "18.162.100.154", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                    "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.62, "error_rate": 0.0},
    {"host": "18.210.69.172", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                   "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.22, "error_rate": 0.0},
    {"host": "204.12.202.198", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                    "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.3, "error_rate": 0.0},
    {"host": "23.237.100.74", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                   "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.32, "error_rate": 0.0},
    {"host": "206.189.192.5", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                   "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.63, "error_rate": 0.0},
    {"host": "23.237.173.109", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                    "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.4, "error_rate": 0.0},
    {"host": "167.71.83.150", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                   "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.41, "error_rate": 0.0},
    {"host": "34.93.171.222", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                   "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.92, "error_rate": 0.0},
    {"host": "157.245.67.128", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                    "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.61, "error_rate": 0.0},
    {"host": "18.162.89.135", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                   "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.71, "error_rate": 0.0},
    {"host": "198.98.55.168", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                   "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.65, "error_rate": 0.0},
    {"host": "157.245.124.217", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                     "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.7, "error_rate": 0.0},
    {"host": "129.146.181.251", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                     "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.76, "error_rate": 0.0},
    {"host": "134.209.188.111", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                     "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.78, "error_rate": 0.0},
    {"host": "68.183.191.140", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                    "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.82, "error_rate": 0.0},
    {"host": "35.192.138.9", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                  "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.29, "error_rate": 0.0},
    {"host": "157.245.207.112", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                     "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.85, "error_rate": 0.0},
    {"host": "68.183.191.248", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                    "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.87, "error_rate": 0.0},
    {"host": "165.22.54.37", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                  "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.88, "error_rate": 0.0},
    {"host": "71.187.28.75", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                  "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.34, "error_rate": 0.0},
    {"host": "157.245.205.81", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                    "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.92, "error_rate": 0.0},
    {"host": "45.76.255.157", "port": 808, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                  "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.45, "error_rate": 0.0},
    {"host": "157.245.197.92", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                    "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 1.01, "error_rate": 0.0},
    {"host": "159.203.87.130", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                    "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.47, "error_rate": 0.0},
    {"host": "50.195.185.171", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                    "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 1.03, "error_rate": 0.0},
    {"host": "144.202.20.56", "port": 808, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                  "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.51, "error_rate": 0.0},
    {"host": "157.230.250.116", "port": 8080, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                     "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 1.14, "error_rate": 0.0},
    {"host": "104.196.70.154", "port": 3128, "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown",
                                                                                                                    "name": "Unknown"}, "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.64, "error_rate": 0.0}
]

index = int(uniform(0, len(PROXY)))
PROXY = PROXY[index]["host"]+":"+str(PROXY[index]["port"])


class Pyvote(unittest.TestCase):
    number = None
    headless = False
    options = None
    profile = None
    capabilities = None

    # Simple logging method
    def log(s, t=None):
        now = datetime.now()
        if t == None:
            t = "Main"
        print(f"{Blue}%s :: %s -> %s{Yellow}" % (str(now), t, s))

    def success(s, t):
        print(f"{BGreen}{t}")

    def error(s, t):
        print(f"{Red}{t}")

    # Use time.sleep for waiting and uniform for randomizing
    def wait_between(self, a, b):
        rand = uniform(a, b)
        sleep(rand)

    def setUpOptions(self):
        self.options = webdriver.FirefoxOptions()
        self.options.headless = self.headless
        self.log('OPTIONS OK')

    def setUpProfile(self):
        self.profile = webdriver.FirefoxProfile()
        # add buster extension path
        self.profile._install_extension(
            "buster_captcha_solver_for_humans-0.7.2-an+fx.xpi", unpack=False)
        # disable Strict Origin Policy
        self.profile.set_preference(
            "security.fileuri.strict_origin_policy", False)
        self.profile.update_preferences()  # Update profile with new configs
        self.log('PROFILE OK')

    def setUpCapabilities(self):
        self.capabilities = webdriver.DesiredCapabilities.FIREFOX
        self.capabilities['marionette'] = True
        self.log('CAPABILITIES OK')

    def setUpProxy(self):
        self.capabilities['proxy'] = {
            "proxyType": "MANUAL", "httpProxy": PROXY, "ftpProxy": PROXY, "sslProxy": PROXY}
        self.log('PROXY OK')
        self.log(PROXY)

    def setUp(self):
        self.log('Starting bot...')
        self.checkColors()
        self.setUpProfile()  # for setup profiles
        self.setUpOptions()  # options for running gecko
        self.setUpCapabilities()  # enable some abilities like marionette
        self.setUpProxy()  # setup proxy if you get ban
        self.driver = webdriver.Firefox(
            options=self.options, capabilities=self.capabilities, firefox_profile=self.profile)  # initialize web driver

    def checkColors(self):
        global BGreen
        global BYellow
        global BPurple
        global BCyan
        global Yellow
        global Green
        global Red
        global Blue
        global On_Black

        # colors
        colors = True  # output colored c:
        machine = sys.platform  # detecting the os
        checkPlatform = platform.platform()  # get current version of os

        if machine.lower().startswith(("os", "win", "darwin", "ios")):
            colors = False  # Mac and Windows shouldn't display colors :c

        if (
            checkPlatform.startswith("Windows-10")
            and int(platform.version().split(".")[2]) >= 10586
        ):
            color = True  # coooolorssss \o/
            # Enables the ANSI -> standard encoding that reads that colors
            os.system("")

        if not colors:
            BGreen = BYellow = BPurple = BCyan = Yellow = Green = Red = Blue = On_Black = ""

        self.log('COLORS OK')

    # Using B-spline for simulate humane like mouse movments
    def human_like_mouse_move(self, action, start_element):
        points = [[6, 2], [3, 2], [0, 0], [0, 2]]
        points = np.array(points)
        x = points[:, 0]
        y = points[:, 1]

        t = range(len(points))
        ipl_t = np.linspace(0.0, len(points) - 1, 100)

        x_tup = si.splrep(t, x, k=1)
        y_tup = si.splrep(t, y, k=1)

        x_list = list(x_tup)
        xl = x.tolist()
        x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        yl = y.tolist()
        y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

        x_i = si.splev(ipl_t, x_list)
        y_i = si.splev(ipl_t, y_list)

        startElement = start_element

        action.move_to_element(startElement)
        action.perform()

        c = 5  # change it for more move
        i = 0
        for mouse_x, mouse_y in zip(x_i, y_i):
            action.move_by_offset(mouse_x, mouse_y)
            action.perform()
            self.log("Move mouse to, %s ,%s" % (mouse_x, mouse_y))
            i += 1
            if i == c:
                break

    def test_run(self):
        action = ActionChains(self.driver)

        streamers = [
            "RuivoShun",
            "Azulaozim",
            "Tominho",
            "oivan1",
            "presto_dog",
            "Serotristina",
            "Gargulaex",
            "Elfo de Touca",
            "Imunizado",
            "diabolic_girl",
            "Raphajack",
            "ahvitum",
            "Buxudinho",
            "titizao44",
            "lc_ximenes",
            "HorikoShoga",
            "Fahamum",
            "JulienioD",
            "Miixs",
            "Hartteman",
            "koppzn",
            "ImViniZaggo",
            "SoMaisUmNoobNaInternet",
            "https://www.twitch.tv/axcse",
            "dartziiin",
            "vettorazz1",
            "RealYocartBR532",
            "eltinfull9",
            "Massukiabo",
            "td_g4mes",
            "Imerlinnn",
            "Felfo",
            "Chanssita",
            "goordao01",
            "Tititiltada",
            "Sammy Dixoon",
            "kratos__ps4",
            "Feijao1002",
            "Manggini",
            "Andrei_sls",
            "BangerzGG",
            "opaidalunnaa",
            "Cavalcante85",
            "milenacolinm",
            "liachan_ceci",
            "deusafogado",
            "LordMec",
            "Rayuchuu",
            "Ccorongs",
            "lionleoheart",
            "Dyksada",
            "r0xaslol",
            "REPPUKK",
            "Luuh3k",
            "Khaluxofc",
            "qusttavo2",
            "Kyrahimeoficial",
            "Lysanziel",
            "aioko",
            "KimPiine",
            "SonataAnpan",
            "Dillianresende",
            "twZaya",
            "Drakonann",
            "tifelixg",
            "tijolo0",
            "Gratuzlol",
            "hilugui",
            "Bryanrc0",
            "topzzs",
            "luigidrett",
            "leonasser",
            "samunelso",
            "AAkirazin",
            "zac_sh0w",
            "VimingGamer",
            "sladefate",
            "fabexbr",
            "avogato007",
            "godhighlander",
            "Jessiedm",
            "Gtoyoshima",
            "dvaragorn",
            "mv_mistery",
            "spadille_tv",
            "TheLiraa",
            "Snowmate204",
            "iAsh_31",
            "ichisakura",
            "0pipcoco",
            "ChronosHenry",
            "Dignidade",
            "soweoff",
            "https://www.twitch.tv/mathola",
            "https://www.twitch.tv/lhamaeu2",
            "https://www.twitch.tv/japao1",
            "https://www.twitch.tv/paquitodefogo",
            "https://www.twitch.tv/srporcao",
            "https://www.twitch.tv/gises_oni",
            "twitch.tv/isaladonerd",
            "caiodvl",
            "birdybr"
        ]

        # first page
        searchBar = "/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[1]/form/div/div/input"
        searchButton = "/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[1]/form/div/button"
        voteButton = "/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/button"

        # modal
        nameInput = '/html/body/div[1]/div/div[2]/div[3]/div[1]/div/div[3]/div/form/div[1]/div/input'
        emailInput = '/html/body/div[1]/div/div[2]/div[3]/div[1]/div/div[3]/div/form/div[2]/div/input'
        cpfInput = '/html/body/div[1]/div/div[2]/div[3]/div[1]/div/div[3]/div/form/div[3]/div/input'
        submitButton = '/html/body/div[1]/div/div[2]/div[3]/div[1]/div/div[3]/div/form/div[4]/button'

        # vote done modal
        okButton = "/html/body/div[6]/div/div[3]/button[1]"

        # success definition
        successText = '//*[@id="swal2-content"]'

        self.driver.get('https://streamers.cnb.gg/votacao?page=streamers')

        for streamer in streamers:
            self.log('Search bar')
            searchBarElement = self.driver.find_element_by_xpath(searchBar)
            searchBarElement.clear()
            searchBarElement.send_keys(streamer)

            self.log('Search button')
            searchButtonElement = self.driver.find_element_by_xpath(
                searchButton)
            self.driver.execute_script(
                "arguments[0].click();", searchButtonElement)

            self.wait_between(MIN_RAND, MAX_RAND)

            for version in range(1, 2000):
                self.log('Vote button')
                voteButtonElement = self.driver.find_element_by_xpath(
                    voteButton)
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, voteButton)))
                self.driver.execute_script(
                    "arguments[0].click();", voteButtonElement)

                self.log('Name input')
                nameInputElement = self.driver.find_element_by_xpath(nameInput)
                nameInputElement.clear()
                nameInputElement.send_keys(
                    'new {} {}'.format(streamer, version))

                self.log('Email input')
                emailInputElement = self.driver.find_element_by_xpath(
                    emailInput)
                emailInputElement.clear()
                emailInputElement.send_keys(
                    'new{}username{}@gmail.com'.format(streamer, version))

                self.log('CPF input')
                cpfInputElement = self.driver.find_element_by_xpath(cpfInput)
                cpfInputElement.clear()
                cpfInputElement.send_keys(cpf())

                submitButtonElement = self.driver.find_element_by_xpath(
                    submitButton)
                self.driver.execute_script(
                    "arguments[0].click();", submitButtonElement)

                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, successText)))
                success = self.driver.find_element_by_xpath(successText)
                if (success.text == "Voto realizado com sucesso"):
                    self.success(
                        'Vote success {} - {}'.format(streamer, version))
                else:
                    self.error(success.text)

                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, okButton))).click()

    def tearDown(self):
        self.log('Ending bot...')
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
