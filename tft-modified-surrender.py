import pkg_resources
pkg_resources.require("PyAutoGUI==0.9.50")
pkg_resources.require("opencv-python==4.5.1.48")
pkg_resources.require("python-imageseach-drov0==1.0.6")
import pyautogui as auto
from python_imagesearch.imagesearch import imagesearch as search
import time
from printy import printy
auto.FAILSAFE = False

import tkinter as tk
from tkinter import messagebox as tkMessagebox

# records the number of games has been played
gameCount = 1
winCount = 0

# flag used to terminating the program
cancel = False

def interrupt():
    global cancel
    cancel = True

# I/O methods
# Checks whether a picture is shown on screen
def onscreen(path, precision=0.8):
    return search(path, precision)[0] != -1

def onscreenHigh(path, precision=0.95):
    return search(path, precision)[0] != -1

def onscreenLow(path, precision=0.5):
    return search(path, precision)[0] != -1


# performs a left click
def click_left(delay=.1):
    auto.mouseDown()
    time.sleep(delay)
    auto.mouseUp()


# performs a right click
def click_right(delay=.1):
    auto.mouseDown(button='right')
    time.sleep(delay)
    auto.mouseUp(button='right')


# click to the input picture on screen
def click_to(path, delay=.1):
    if onscreen(path):
        auto.moveTo(search(path))
        click_left(delay)



# Helper methods
# buys arbitrary champions
def buy_first(iterations):
    for i in range(iterations):
        #updated troops     
        click_to("./captures/ziggs.png")
        click_to("./captures/lulu.png")
        click_to("./captures/kled.png")
        click_to("./captures/kennen.png")


def buy_second(iterations):
    for i in range(iterations):
        #updated troops     
        click_to("./captures/poppy.png")
        click_to("./captures/gragas.png")
        click_to("./captures/vlad.png")


def buy_xp_once():
    click_to("./captures/buy xp.png")
        
def reroll_once():
    click_to("./captures/reroll.png")


# buys item at certain rounds
def buy_item_once():
    if onscreenLow("./captures/item.png"):
        if onscreen("./captures/2-2.png"):
            print("- Item stage detected. Buying items")
            auto.moveTo(734,974)
            click_left()
        if onscreen("./captures/3-2.png"):
            auto.moveTo(734,974)
            click_left()
        # not needed since we are surrendering at 3-4
        # if onscreen("./captures/4-2.png"):
        #     auto.moveTo(734,974)
        #     click_left()


def carousel():
    if onscreen("./captures/2-4.png"):
        for x in range(2):
            auto.moveTo(928, 396)
            click_right()
            time.sleep(0.25)
    # not needed since we are surrending at 3-4
    # if onscreen("./captures/3-4.png"):
    #     for x in range(2):
    #         auto.moveTo(928, 396)
    #         click_right()
    #         time.sleep(0.25)
    # if onscreen("./captures/4-4.png"):
    #     for x in range(2):
    #         auto.moveTo(928, 396)
    #         click_right()
    #         time.sleep(0.25)

    
# States in the program
def init_run():
    print("Developed by Detergent")
    # printy(r"""
    # [c>] _____       _                            _   @
    # [c>]|  __ \     | |                          | |  @
    # [c>]| |  | | ___| |_ ___ _ __ __ _  ___ _ __ | |_ @
    # [c>]| |  | |/ _ \ __/ _ \ '__/ _` |/ _ \ '_ \| __|@
    # [c>]| |__| |  __/ ||  __/ | | (_| |  __/ | | | |_ @
    # [c>]|_____/ \___|\__\___|_|  \__, |\___|_| |_|\__|@
    # [c>]                          __/ |               @
    # [c>]                         |___/                @
    # """)
    # printy(f"Welcome! You're running Detergent's TFT bot.\nPlease feel free to ask questions \nor contribute at https://github.com/Detergent13/tft-bot", "nB")
    printy(f"Welcome! You're running Detergent's TFT bot.", "nB")
    printy(f"This script will end the game at stage 3-4 or potentially earlier.", "nB")
    root = tk.Tk()
    root.overrideredirect(1)
    root.withdraw()
    proceed = tkMessagebox.askyesno("Proceed?", "Make sure you are in the TFT lobby. \nProceed?")
    if proceed:
        print("Bot started, queuing up!")
        print("Currently on game " + str(gameCount) + ".")
    else:
        exit()


def run():
    print("")
    print("Times you ended with top 3: " + str(winCount))
    print("Currently on game " + str(gameCount) + ".")


def queue():  
    if onscreen("./captures/tft logo.png"):
        click_to("./captures/find match ready.png")
    while not onscreen("./captures/loading.png"):
        time.sleep(1)
        click_to("./captures/accept.png")
    print("Loading!")


def loading():
    while not onscreen("./captures/1-1.png"):
        time.sleep(1)
    print("Match starting!")


def start():
    while onscreen("./captures/1-1.png"):
        auto.moveTo(888, 376)
        click_right()
        time.sleep(0.25)
    print("In the match now!")


# Splitted operation so that while condition is checked more frequently
# returns true if game ended early, false if surrendering
def main():
    x = 0
    # global end_early
    while not (onscreen("./captures/end continue.png") or onscreen("./captures/end exit.png") or onscreen("./captures/3-4.png")):
        if x % 5 == 0:
            carousel()
        if x % 5 == 1:
            buy_item_once()
        if x % 5 == 2:
            buy_first(1)
        if x % 5 == 3:
            buy_second(1)
        if x % 5 == 4:
            buy_xp_once()
            reroll_once()
        x += 1
    if(onscreen("./captures/end continue.png") or onscreen("./captures/end exit.png")):
        print("- Game has ended early. Returning to lobby")
        return True
    else:
        print("- Game has not ended early. Surrendering")
        return False
        


def surrender():
    print("- In surrendering process")
    click_to("./captures/settings.png")
    while not onscreen("./captures/surrender 1.png"):
        time.sleep(1)
    while not onscreen("./captures/surrender 2.png"):
        click_to("./captures/surrender 1.png")
    time.sleep(1)
    click_to("./captures/surrender 2.png")
    time.sleep(10)
    while onscreen("./captures/missions ok.png"):
        click_to("./captures/missions ok.png")
        time.sleep(2)
    while onscreen("./captures/skip waiting for stats.png"):
        click_to("./captures/skip waiting for stats.png")
    time.sleep(5)
    while onscreen("./captures/play again.png"):
        click_to("./captures/play again.png")
    time.sleep(10)
    print("Queuing up again!")


def end():
    print("- In ending process")
    click_to("./captures/end continue.png")
    click_to("./captures/end exit.png")
    time.sleep(15)
    while onscreen("./captures/missions ok.png"):
        click_to("./captures/missions ok.png")
        time.sleep(2)
    time.sleep(5)
    if onscreenHigh("./captures/winning1.png") or onscreenHigh("./captures/winning2.png") or onscreenHigh("./captures/winning3.png"):
        global winCount
        winCount = winCount + 1
    while onscreen("./captures/skip waiting for stats.png"):
        click_to("./captures/skip waiting for stats.png")
        time.sleep(2)
    time.sleep(5)
    while onscreen("./captures/play again.png"):
        click_to("./captures/play again.png")
        time.sleep(2)
    time.sleep(10)
    print("Queuing up again!")




# main program that includes state transitions 
if not cancel:
    init_run()


while not cancel:
    queue()
    loading()
    start()
    end_early = main()
    if end_early:
        end()
    else:
        surrender()
    gameCount = gameCount + 1
    run()