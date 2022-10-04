# Detergent's TFT Bot

import pkg_resources
import pyautogui as auto
from python_imagesearch.imagesearch import imagesearch as search
import time
from printy import printy

pkg_resources.require("PyAutoGUI==0.9.50")
pkg_resources.require("opencv-python==4.5.1.48")
pkg_resources.require("python-imageseach-drov0==1.0.6")

auto.FAILSAFE = False

global gamecount
gamecount = 0

# Start utility methods
def onscreen(path, precision=0.8):
    return search(path, precision)[0] != -1


def search_to(path):
    pos = search(path)
    if onscreen(path):
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
    if onscreen(path):
        auto.moveTo(search(path))
        click_left(delay)
# End utility methods


# Start main process
def queue():
    if onscreen("./captures/tft logo.png"):
        click_to("./captures/find match ready.png")
    while not onscreen("./captures/loading.png"):
        time.sleep(1)
        click_to("./captures/accept.png")
    global starttimer
    starttimer = time.time()
    print("Loading!")
    loading()


def loading():
    while not onscreen("./captures/1-1.png"):
        time.sleep(1)

    print("Match starting!")
    start()


def start():
    while onscreen("./captures/1-1.png"):
        auto.moveTo(1270, 795)   # use print(auto.position()) to look for a better position
        click_right()

    print("In the match now!")
    main()

######################################################################################################################################
def buy(iterations):
    for i in range(iterations):
        if not onscreen("./captures/gold/0.png"):
                click_to("./captures/trait/jade/jade.png")
                time.sleep(0.5)
        if not onscreen("./captures/gold/0.png"):
                click_to("./captures/trait/bruiser/bruiser.png")
                time.sleep(0.5)

######################################################################################################################################
def checks():  # checks to see if game was interrupted
    if onscreen("./captures/play again.png"):
        won_match()
    if onscreen("./captures/dead.PNG"):  # check for loss
        click_to("./captures/dead.PNG")
        won_match()
    if onscreen("./captures/reconnect.png"):
        print("reconnecting!")
        time.sleep(0.5)
        click_to("./captures/reconnect.png")


def main():
    while not onscreen("./captures/2-4.png"):
        buy(5)
        time.sleep(1)
        checks() 
    while onscreen("./captures/2-4.png"):
        auto.moveTo(928, 396)
        click_right()
        time.sleep(0.25)

    time.sleep(5)

    if onscreen("./captures/2-5.png"):
        while not onscreen("./captures/3-2.png"):  # change this if you want to surrender at a different stage, also the image recognition struggles with 5 being it sees it as 3 so i had to do 6 as that's seen as a 5
            buy(5)
            if not onscreen("./captures/gold/0.png") or not ("./captures/1.png") or not ("./captures/2.png") or not ("./captures/3.png"):
                click_to("./captures/xp_buy.png")
                time.sleep(1)
            time.sleep(1)
            if onscreen ("./captures/take_all.png"): #treasure dragon, dont reroll just take it
                click_to("./captures/take_all.png")
                time.sleep(1)
            if not onscreen("./captures/gold/0.png") or not ("./captures/1.png") or not ("./captures/2.png") or not ("./captures/3.png") or not ("./captures/4.png") or not ("./captures/5.png") or not ("./captures/6.png"):
                click_to("./captures/reroll.png")
                time.sleep(1)
            #tactician runs to position to collect astral orbs
            auto.moveTo(866, 820)
            click_right()
            #
            time.sleep(1)
            checks() 
        print("Surrendering now!")
        surrender()


def end_match():
    while not onscreen("./captures/find match ready.png"):  # added a main loop for the end match function to ensure you make it to the find match button.
        while onscreen("./captures/missions ok.png"):
            #screenshot if you have an "ok" button
            t = time.localtime()    # added for printing time
            current_time = time.strftime("%H%M%S", t) #for the changing file name
            myScreenshot = auto.screenshot()
            myScreenshot.save(rf'./screenshots\{current_time}.png')
            time.sleep(2)
            print("SS saved")
            click_to("./captures/missions ok.png")
            time.sleep(2)
        while onscreen("./captures/skip waiting for stats.png"):
            click_to("./captures/skip waiting for stats.png")
            time.sleep(5)
        while onscreen("./captures/play again.png"):
            click_to("./captures/play again.png")
            
            
def won_match(): 
    print_timer()    

    time.sleep(3)

    end_match()

    time.sleep(5)
    print("Queuing up again!")
    queue()

    
def surrender():
    click_to("./captures/settings.png")

    while not onscreen("./captures/surrender 1.png"):
        click_to("./captures/settings.png")  # just in case it gets interrupted or misses
        time.sleep(1)
    while not onscreen("./captures/surrender 2.png"):
        click_to("./captures/surrender 1.png")
        checks()  # added a check here for the rare case that the game ended before the surrender finished.

    time.sleep(1)
    click_to("./captures/surrender 2.png")
    time.sleep(10)

    time.sleep(1)

    end_match()

    time.sleep(5)
    
    print_timer()
    
    print("Queuing up again!")
    queue()


def print_timer():
    global gamecount
    global endtimer
    endtimer = time.time()
    gamecount += 1
    sec = (endtimer - starttimer)
    hours = sec // 3600
    sec = sec - hours*3600
    mu = sec // 60
    ss = sec - mu*60
    gamecount2 = str(gamecount)
    t = time.localtime()    # added for printing time
    current_time = time.strftime("%H:%M:%S", t)
    #result_list = str(datetime.timedelta(seconds=sec)).split(".")
    print("-------------------------------------")
    print("Game End",current_time)
    print("Play Time : ", int(float(hours)), "Hour", int(float(mu)), "Min", int(float(ss)), "Sec")
    print("Gamecount : ", gamecount2)
    print("-------------------------------------")
    print("Queuing up again!")
# End main process
    
    
# Start auth + main script
print("Developed by:")
printy(r"""
[c>] _____       _                            _     @
[c>]|  __ \     | |                          | |    @
[c>]| |  | | ___| |_ ___ _ __ __ _  ___ _ __ | |_   @
[c>]| |  | |/ _ \ __/ _ \ '__/ _` |/ _ \ '_ \| __|  @
[c>]| |__| |  __/ ||  __/ | | (_| |  __/ | | | |_   @
[c>]|_____/ \___|\__\___|_|  \__, |\___|_| |_|\__|  @
[c>]                          __/ |                 @
[c>]                         |___/                  @
[c>]                                                @
[c>]   _________       __    _________    .________ @
[c>]  /   _____/ _____/  |_  \______  \   |   ____/ @
[c>]  \_____  \_/ __ \   __\     /    /   |____  \  @
[c>]  /        \  ___/|  |      /    /    /       \ @
[c>] /_______  /\___  >__|     /____/ /\ /______  / @
[c>]         \/     \/                \/        \/  @
""")

printy(f"Welcome! You're running Detergent's TFT bot.\nPlease feel free to ask questions or contribute at https://github.com/Detergent13/tft-bot", "nB")
auto.alert("Press OK when you're in a TFT lobby!\n")
print("Bot started, queuing up!")
queue()

# End auth + main script
