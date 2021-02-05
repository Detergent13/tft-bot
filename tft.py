# Detergent's TFT Bot @ Nulled.to

import pkg_resources

pkg_resources.require("PyAutoGUI==0.9.50")
pkg_resources.require("opencv-python==4.2.0.34")
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
    while not onscreen("./captures/loading 1.png"):
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
        click_to("./captures/diana.png")
        click_to("./captures/fiora new.png")
        click_to("./captures/yasuo new.png")
        click_to("./captures/garen.png")
        click_to("./captures/wukong.png")
        click_to("./captures/nidalee.png")


def main():
    while not onscreen("./captures/2-4.png"):
        buy(1)
        time.sleep(1)
    while onscreen("./captures/2-4.png"):
        auto.moveTo(928, 396)
        click_right()
        time.sleep(0.25)

    time.sleep(5)

    if onscreen("./captures/2-5.png"):
        while not onscreen("./captures/3-2.png"):
            buy(1)
            click_to("./captures/reroll.png")
            time.sleep(1)
    if onscreen("./captures/3-2.png"):
        print("Surrendering now!")
        surrender()


def surrender():
    click_to("./captures/settings.png")

    while not onscreen("./captures/surrender 1.png"):
        time.sleep(1)
    while not onscreen("./captures/surrender 2 new.png"):
        click_to("./captures/surrender 1.png")

    time.sleep(1)
    click_to("./captures/surrender 2 new.png")
    time.sleep(15)

    time.sleep(1)

    while onscreen("./captures/missions ok.png"):
        click_to("./captures/missions ok.png")
    time.sleep(5)
    while onscreen("./captures/skip waiting for stats.png"):
        click_to("./captures/skip waiting for stats.png")
    time.sleep(5)
    while onscreen("./captures/play again.png"):
        click_to("./captures/play again.png")

    time.sleep(10)
    print("Queuing up again!")
    queue()
# End main process


# Start auth + main script
print("Developed by:")
printy(r"""
[c>] _____       _                            _   @[<b]            _   _       _ _          _  _        @
[c>]|  __ \     | |                          | |  @[<b]    ____   | \ | |     | | |        | || |       @
[c>]| |  | | ___| |_ ___ _ __ __ _  ___ _ __ | |_ @[<b]   / __ \  |  \| |_   _| | | ___  __| || |_ ___  @
[c>]| |  | |/ _ \ __/ _ \ '__/ _` |/ _ \ '_ \| __|@[<b]  / / _` | | . ` | | | | | |/ _ \/ _` || __/ _ \ @
[c>]| |__| |  __/ ||  __/ | | (_| |  __/ | | | |_ @[<b] | | (_| | | |\  | |_| | | |  __/ (_| || || (_) |@
[c>]|_____/ \___|\__\___|_|  \__, |\___|_| |_|\__|@[<b]  \ \__,_| |_| \_|\__,_|_|_|\___|\__,_(_)__\___/ @
[c>]                          __/ |               @[<b]   \____/                                        @
[c>]                         |___/                @[<b]                                                 @
""")

printy(f"Authorization successful!", "nB")
auto.alert("Press OK when you're in a TFT lobby!\n")
print("Bot started, queuing up!")
queue()

# End auth + main script
