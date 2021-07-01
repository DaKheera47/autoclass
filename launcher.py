import pyautogui as pag
import time
import os
import yaml
import sys
from termcolor import cprint
import json
import cursor
cursor.hide()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

    # to show preview of all classes to join
    with open("classes.yaml", 'r') as stream:
        try:
            CLASS_INFO = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    cprint("""
    ______  _____   _____  _______             _______ _     _ __   _ _______ _     _ _______  ______    
     ____/ |     | |     | |  |  |      |      |_____| |     | | \  | |       |_____| |______ |_____/    
    /_____ |_____| |_____| |  |  |      |_____ |     | |_____| |  \_| |_____  |     | |______ |    \_    
                                                                                                         
    ______  __   __      ______  _______ _     _ _     _ _______ _______  ______ _______                 
    |_____]   \_/        |     \ |_____| |____/  |_____| |______ |______ |_____/ |_____|                 
    |_____]    |         |_____/ |     | |    \_ |     | |______ |______ |    \_ |     |                 
                                                                                                         
""", "green")
    cprint(f"CLASS LIST", "grey", attrs=["bold"])

    for cls in list(CLASS_INFO.keys()):
        print(
            f"{cls} => {list(CLASS_INFO[cls].values())[1]} => {list(CLASS_INFO[cls].values())[2]}")


def findImage(imageUrl, message, timeout, confidence=0.8):
    i = 1
    while True:
        if i <= timeout:
            try:
                x, y = pag.locateCenterOnScreen(
                    imageUrl, confidence=confidence)
            except TypeError:
                time.sleep(1)
                print(f"{message} (Time Elapsed: {i}s)", end="\r")
                i += 1
                continue
            break
        else:
            return (-1, -1)

    clear()
    return (x, y)


def enterTextInput(x, y, text, message):
    pag.click(x=x, y=y)
    pag.write(text)
    print(f"\n{message}")
    pag.press("enter")


def main(code, password):
    pag.PAUSE = 0.6
    globalConfidence = 0.8
    # start button
    pag.press("winleft")

    # launch zoom
    pag.write("zoom")
    pag.press("enter")

    # locate join button on zoom
    x, y = findImage(
        "joinBtn.png", "Searching for Join Button", timeout=60 * 10, confidence=globalConfidence)
    if x != -1 and y != -1:
        pag.click(x, y)
    else:
        return

    # enter code into meeting id field
    x, y = findImage(
        "joinMeeting.png", "Searching for meeting ID input field", timeout=60 * 10, confidence=globalConfidence)
    if x != -1 and y != -1:
        enterTextInput(x, y + 60, code, "Code entered!")
    else:
        return

    # enter password into password field
    x, y = findImage(
        "enterMeetingPw.png", "Searching for password field", timeout=60 * 10, confidence=globalConfidence)
    if x != -1 and y != -1:
        enterTextInput(x, y + 60, password, "Password entered!")
    else:
        return

    # locate join with computer audio button on zoom
    x, y = findImage("joinWithComputerAudioBtn.png",
                     "Have not been accepted into class", timeout=60 * 10, confidence=globalConfidence)
    if x != -1 and y != -1:
        pag.click(x, y)
    else:
        return

    # force full screen zoom
    pag.hotkey("winleft", "up")


# if this file is ran directly
if __name__ == '__main__':
    with open("classes.yaml", 'r') as stream:
        try:
            CLASS_INFO = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    print("""
┌─┐┬ ┬┌─┐┌─┐┌─┐┌─┐  ┌─┐┬  ┌─┐┌─┐┌─┐
│  ├─┤│ ││ │└─┐├┤   │  │  ├─┤└─┐└─┐
└─┘┴ ┴└─┘└─┘└─┘└─┘  └─┘┴─┘┴ ┴└─┘└─┘""")

    i = 1
    for cls in CLASS_INFO.items():
        print(f"[{i}] {cls[0]}: {cls[1]['code']}")
        i += 1

    className = input(f"=>>")

    try:
        chosenClass = list(CLASS_INFO.items())[int(className) - 1][1]
        print(list(CLASS_INFO.items())[int(className) - 1][1])

        main(chosenClass["code"], chosenClass["password"])
    except:
        print("Invalid input")
