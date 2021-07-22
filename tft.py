# Detergent's TFT Bot
# Branch: main

import pkg_resources

pkg_resources.require("PyAutoGUI==0.9.50")
pkg_resources.require("opencv-python==4.5.1.48")
pkg_resources.require("python-imageseach-drov0==1.0.6")

import pyautogui as auto
from python_imagesearch.imagesearch import imagesearch as search
import time
from printy import printy
from printy import inputy


auto.FAILSAFE = False


# Start utility methods
def onscreen(path, precision=0.8):
    return search(path, precision)[0] != -1


def search_to(path):
    pos = search(path)
    if onscreen(path):
        auto.moveTo(pos)
        # print(path + " found")
        return pos
#   else:
    #   print(path + " not found")


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
    if onscreen(path):
        auto.moveTo(search(path))
        click_left(delay)
        # print(path + " clicked")
# End utility methods


# Start main process
def queue():
    if onscreen("./captures/tft logo.png"):
        click_to("./captures/find match ready.png")
    while not onscreen("./captures/loading.png"):
        time.sleep(1)
        click_to("./captures/accept.png")

    print("Loading!")
    loading()


def loading():
    while not onscreen("./captures/1-1.png"):
        time.sleep(1)

    print("Match starting!")
    start()


def start():
    while onscreen("./captures/1-1.png"):
        auto.moveTo(888, 376)
        click_right()

    print("In the match now!")
    main()


def buy(iterations):
    for i in range(iterations):
        #updated troops
        click_to("./captures/ziggs.png")
        click_to("./captures/lulu.png")
        click_to("./captures/kled.png")
        click_to("./captures/kennen.png")
        click_to("./captures/poppy.png")
        click_to("./captures/gragas.png")
        click_to("./captures/vlad.png")


#new function, get the item from 2-2 and 3-2, working properly
def buy_item():
    click_to("./captures/choose_one.png")    #changed this to just another image that it clicks.

def checks(): #added checks to see if game was interrupted 
    if onscreen("./captures/play again.png"):
        won_match()
    if onscreen("./captures/dead.PNG"):   #added another check for if you actually lose in cases where you surrender at a later time. 
            click_to("./captures/dead.PNG")
            won_match()
    if onscreen("./captures/reconnect.png"):
        print("reconnecting!")
        time.sleep(0.5)
        click_to("./captures/reconnect.png")


def main():
    while not onscreen("./captures/2-4.png"):
        buy(1)
        buy_item()
        time.sleep(1)
        checks() 
    while onscreen("./captures/2-4.png"):
        auto.moveTo(928, 396)
        click_right()
        time.sleep(0.25)

    time.sleep(5)

    if onscreen("./captures/2-5.png"):
        while not onscreen("./captures/6-6.png"): # change this if you want to surrender at a different stage, also the image recognition struggles with 5 being it sees it as 3 so i had to do 6 as that's seen as a 5
            buy(1)
            buy_item()
            click_to("./captures/reroll.png")
            time.sleep(1)
            checks() 
        print("Surrendering now!") #moved these two lines out of the if statement to make it more streamline.
        surrender()


def end_match():
    while not onscreen("./captures/find match ready.png"):   #added a main loop for the end match function to ensure you make it to the find match button.
        while onscreen("./captures/missions ok.png"):
            click_to("./captures/missions ok.png")
            time.sleep(2)
        while onscreen("./captures/skip waiting for stats.png"):
            click_to("./captures/skip waiting for stats.png")
            time.sleep(5)
        while onscreen("./captures/play again.png"):
            click_to("./captures/play again.png"
def won_match(): 
    print("Looks like we won! Re-queuing")
    time.sleep(3)

    end_match()

    time.sleep(5)
    queue()

def surrender():
    click_to("./captures/settings.png")

    while not onscreen("./captures/surrender 1.png"):
        click_to("./captures/settings.png")      #added this in case it gets interrupted or misses
        time.sleep(1)
    while not onscreen("./captures/surrender 2.png"):
        click_to("./captures/surrender 1.png")
        checks()     #added a check here for the rare case that the game ended before the surrender finished.

    time.sleep(1)
    click_to("./captures/surrender 2.png")
    time.sleep(10)

    time.sleep(1)

    end_match()

    time.sleep(5)
    print("Queuing up again!")
    queue()
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
auto.alert("Press OK when you're in a TFT lobby!\n")
print("Bot started, queuing up!")
queue()

# End auth + main script
