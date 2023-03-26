# Important: 
1) With 8.5 you need to rerun the requirements: `pip install -r requirements.txt`
The Surrender Button doesn't work, so this is part 1 of the workaround.
2) In `tft.py` near the end 'def surrender():' you have to personally change the '/' to be "fit" your keyboard layout, so the /ff can be executed.
[here](https://pyautogui.readthedocs.io/en/latest/keyboard.html) under "KEYBOARD_KEYS" you can find the phrasing for the keys. By default, it should be compatible with US/UK keyboard layouts.

Thanks for checking out my release!

# Installation:

* Install Python 3.8.3 from [here](https://www.python.org/downloads/), or the Windows Store
* Navigate to your install directory using `cd` and run `pip install -r requirements.txt` in Command Prompt
* Navigate to your install directory using `cd` and run `py "tft.py"` in Command Prompt
* Follow the instructions in your terminal window! Get into a TFT lobby, have the created window visible on your screen, and press 'OK' to start the bot!

# Troubleshooting:

* If these steps don't work, try running the file with `python "tft.py"` instead (For Windows Store/MacOS/Linux users especially) Likewise, try `pip3` instead of `pip` for installing requirements.
* If pip doesn't seem to exist, try installing it [here](https://pip.pypa.io/en/stable/installing/). Essentially 'save as' from [here](https://bootstrap.pypa.io/get-pip.py), then run `py get-pip.py` and try to use pip again
* The bot is configured to work with in-game resolution 1920x1080, and League client resolution 1280x720. (Also Windows scaling 100%) You can switch this up though, just re-capture the images in the captures folder!
* If you're having issues with Python not working properly, please make sure you have the correct version (3.8.3) installed, and all of the correct module versions installed, as listed in requirements.txt
* Make sure to run League and the bot on your main monitor, as it doesn't support additional monitors!
If you need additional help, feel free to reach out to me via an [issue](https://github.com/Detergent13/tft-bot/issues).

Hope you enjoy!
-Detergent <3
