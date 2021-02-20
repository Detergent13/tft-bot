# Detergent's TFT Bot
# Branch: main

import pkg_resources

pkg_resources.require("PyAutoGUI==0.9.50")
pkg_resources.require("opencv-python==4.2.0.34")
pkg_resources.require("python-imageseach-drov0==1.0.6")

import requests
import base64
import os
import pyautogui as auto
from python_imagesearch.imagesearch import imagesearch as search
import time
from printy import printy
from printy import inputy
import urllib3
import pydirectinput
import json

urllib3.disable_warnings()
# If you haven't installed your game in default path (Windows) set your path here
PATH = "default"
auto.FAILSAFE = False

class xtra:
    def base64encode(text):
        text = base64.b64encode(text.encode("ascii")).decode("ascii")
        return text

class lcu:
    def connect(lockfile_path="default"):
        if lockfile_path == "default":
            lockfile_path = "C:\\Riot Games\\League of Legends\\lockfile"
        if lcu.check_exist(lockfile_path):
            return lcu.readFile(lockfile_path)
        else:
            raise Exception("Couldn't read lockfile!\nThis could mean that either the \
path is not the right or the League Client is not opened!")

    def check_exist(lockfile_path):
        return os.path.exists(lockfile_path)

    def readFile(lockfile_path):
        lockfile = open(lockfile_path, "r")
        data = lockfile.read().split(":")
        data_dict = {
            "port": data[2],
            "url": "https://127.0.0.1:{}".format(data[2]),
            "auth": "riot:{}".format(data[3]),
            "connection_method": data[4]
        }
        return data_dict

    def start_search(lcu_data):
        auth = xtra.base64encode(lcu_data["auth"])
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": F"Basic {auth}"
        }
        url = lcu_data["url"] + "/lol-lobby/v2/lobby/matchmaking/search"
        request = requests.post(url, headers=headers, verify=False)
        return request.status_code

    def play_again(lcu_data):
        auth = xtra.base64encode(lcu_data["auth"])
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": F"Basic {auth}"
        }
        url = lcu_data["url"] + "/lol-lobby/v2/play-again"
        request = requests.post(url, headers=headers, verify=False)
        return request.status_code

    def create_game_lobby_tft(lcu_data, gm:str="Normal"):
        if gm.upper() != "NORMAL" and gm.upper() != "RANKED":
            raise ValueError("Defined gamemode is invalid!\nValid gamemodes are Normal and Ranked.")
        else:
            if gm.upper() == "NORMAL":
                q_id = 1090
            if gm.upper() == "RANKED":
                q_id = 1100
        auth = xtra.base64encode(lcu_data["auth"])
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": F"Basic {auth}"
        }
        data = '{{"queueId":{}}}'.format(q_id)
        url = lcu_data["url"] + "/lol-lobby/v2/lobby/"
        request = requests.post(url, headers=headers, data=data, verify=False)
        return request.status_code

    def create_tutorial_lobby_tft(lcu_data):
        auth = xtra.base64encode(lcu_data["auth"])
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": F"Basic {auth}"
        }
        data = '{"queueId":1110}'
        url = lcu_data["url"] + "/lol-lobby/v2/lobby/"
        request = requests.post(url, headers=headers, data=data, verify=False)
        return request.json()

    def get_current_summoner_in_queue(lcu_data, rc=False):
        auth = xtra.base64encode(lcu_data["auth"])
        headers = {
            "Accept": "application/json",
            "Authorization": F"Basic {auth}"
        }
        url = lcu_data["url"] + "/lol-matchmaking/v1/ready-check"
        request = requests.get(url, headers=headers, verify=False)
        request_json = request.json()
        if "state" in request_json:
            if request_json["state"] == "Invalid":
                return True
            elif request_json["state"] == "InProgress":
                if rc == True:
                    return 2
                return True
        elif request_json["httpStatus"] == 404:
            return False

    def get_current_summoner_ready_check(lcu_data, rc=False):
        is_in_q = lcu.get_current_summoner_in_queue(lcu_data,True)
        if is_in_q == 2:
            return True
        if is_in_q == True and is_in_q != 2 and rc == True:
            return 2
        return False

    def auto_accept_current_ready_check(lcu_data):
        ready_check = lcu.get_current_summoner_ready_check(lcu_data,True)
        if ready_check == True:
            auth = xtra.base64encode(lcu_data["auth"])
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": F"Basic {auth}"
            }
            url = lcu_data["url"] + "/lol-matchmaking/v1/ready-check/accept"
            requests.post(url, headers=headers, verify=False)
            return "Accepted!"
        elif ready_check == 2:
            return "Waiting for ready check..."
        else:
            return "Not in queue!"

# Start utility methods
class wrappers:
    def onscreen(path, precision=0.8):
        return search(path, precision)[0] != -1

    def search_to(path):
        pos = search(path)
        if wrappers.onscreen(path):
            auto.moveTo(pos)
            return pos

    def click_key(key, delay=.1):
        auto.keyDown(key)
        time.sleep(delay)
        auto.keyUp(key)


    def click_left(delay=.1):
        auto.mouseDown()
        time.sleep(delay)
        auto.mouseUp()


    def click_right(delay=.1):
        auto.mouseDown(button='right')
        time.sleep(delay)
        auto.mouseUp(button='right')


    def click_to(path, delay=.1):
        if wrappers.onscreen(path):
            auto.moveTo(search(path))
            wrappers.click_left(delay)

    def click_to_r(path, delay=.1):
        if wrappers.onscreen(path):
            auto.moveTo(search(path))
            wrappers.click_right(delay)
        # print(path + " clicked")
# End utility methods


# Start main process
class main:
    def queue():
        lcu_data = lcu.connect(PATH)
        print("Creating tft lobby...")
        lcu.create_game_lobby_tft(lcu_data)
        lcu.start_search(lcu_data)
        while True:
            response = lcu.auto_accept_current_ready_check(lcu_data)
            if response == "Accepted!":
                time.sleep(5)
                response = lcu.auto_accept_current_ready_check(lcu_data)
                if response == "Not in queue!":
                    break
        main.loading()


    def loading():
        while not wrappers.onscreen("./captures/1-1.png"):
            time.sleep(1)
        print("Match starting!")
        main.start()


    def start():
        while wrappers.onscreen("./captures/1-1.png"):
            auto.moveTo(888, 376)
            wrappers.click_right()
        print("In the match now!")
        main.main()

    def

    def buy(iterations):
        wanted_champs = main.get_combo(1)
        for i in range(iterations):
            for x in wanted_champs:
                wrappers.click_to("./captures/champions/{}.png".format(x.lower()))

    def get_combo(set:str=1):
        version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
        champion_id = {}
        champs_req = requests.get(F"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json").json()
        combojson = requests.get("https://raw.githubusercontent.com/BadMaliciousPyScripts/combo_json/main/combos.json").json()
        wanted_champs = []
        set = "Set{}".format(int(set))
        for x in list(champs_req["data"]):
            try:
                if file[set]["Champions"][x]:
                    wanted_champs.append(x)
            except KeyError:
                pass
        return wanted_champs

    def main():
        while not wrappers.onscreen("./captures/2-4.png"):
            main.orbs(1)
            main.buy(1)
            time.sleep(1)
        while wrappers.onscreen("./captures/2-4.png"):
            auto.moveTo(928, 396)
            wrappers.click_right()
            time.sleep(0.25)
        time.sleep(5)

        if wrappers.onscreen("./captures/2-5.png"):
            while not wrappers.onscreen("./captures/3-2.png"): # change this if you want to surrender at a different stage
                main.orbs(1)
                main.buy(1)
                pydirectinput.press('d')
                time.sleep(1)
        if wrappers.onscreen("./captures/3-2.png"): # (and this)
            print("Surrendering now!")
            main.surrender()

    def orbs(iterations=1):
        for i in range(iterations):
            wrappers.click_to_r("./captures/orb_white.png")
            wrappers.click_to_r("./captures/orb_blue.png")
            wrappers.click_to("./captures/orb_red.png")
            # wrappers.click_to("./captures/orb_fortune.png")

    def surrender():
        while not wrappers.onscreen("./captures/surrender 2.png"):
            pydirectinput.press('enter')
            auto.write("/ff")
            pydirectinput.press('enter')
        time.sleep(1)
        wrappers.click_to("./captures/surrender 2.png")
        time.sleep(15)

        while wrappers.onscreen("./captures/missions ok.png"):
            wrappers.click_to("./captures/missions ok.png")
            time.sleep(5)
        while wrappers.onscreen("./captures/skip waiting for stats.png"):
            wrappers.click_to("./captures/skip waiting for stats.png")
        time.sleep(5)

        lcu_data = lcu.connect(PATH)
        lcu.play_again(lcu_data)
        time.sleep(10)
        input()
        print("Queuing up again!")
        main.queue()
# End main process


# Start auth + main script
print("Developed by:")
printy(r"""
[c>] _____       _                            _   @
[c>]|  __ \     | |                          | |  @
[c>]| |  | | ___| |_ ___ _ __ __ _  ___ _ __ | |_ @
[c>]| |  | |/ _ \ __/ _ \ '__/ _` |/ _ \ '_ \| __|@
[c>]| |__| |  __/ ||  __/ | | (_| |  __/ | | | |_ @
[c>]|_____/ \___|\__\___|_|  \__, |\___|_| |_|\__|@
[c>]                          __/ |               @
[c>]                         |___/                @
""")

printy(f"Welcome! You're running Detergent's TFT bot.\nPlease feel free to ask questions or contribute at https://github.com/Detergent13/tft-bot", "nB")
print("Bot started, queuing up!")
main.queue()

# End auth + main script
