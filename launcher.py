import pyautogui as pag
import time
import os
import yaml
import sys
from termcolor import cprint
import json
import cursor
from genTable import genTable
cursor.hide()
CUR_PATH = os.path.dirname(os.path.realpath(__file__))


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    genTable()


def findImage(imageUrl, message, timeout=10 * 60, confidence=0.98):
    i = 1
    while True:
        if i <= timeout:
            try:
                x, y = pag.locateCenterOnScreen(
                    f"{CUR_PATH}/static/{imageUrl}", confidence=confidence)
            except TypeError:
                print(f"{message} (Time Elapsed: {i}s)", end="\r")
                time.sleep(1)
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
    # start button
    pag.press("winleft")

    # launch zoom
    pag.write("zoom")
    pag.press("enter")

    # locate join button on zoom
    x, y = findImage("joinBtn.png", "Searching for Join Button")
    if x != -1 and y != -1:
        pag.click(x, y)
    else:
        return {"error": True, "message": "ERR - joinBtn.png"}

    # enter code into meeting id field
    x, y = findImage("joinMeeting.png", "Searching for meeting ID input field")
    if x != -1 and y != -1:
        enterTextInput(x, y + 60, code, "Code entered!")
    else:
        return {"error": True, "message": "ERR - joinMeeting.png"}

    # enter password into password field
    x, y = findImage("enterMeetingPw.png", "Searching for password field")
    if x != -1 and y != -1:
        enterTextInput(x, y + 60, password, "Password entered!")
    else:
        return {"error": True, "message": "ERR - enterMeetingPw.png"}

    # locate join with computer audio button on zoom
    x, y = findImage("joinWithComputerAudioBtn.png",
                     "Have not been accepted into class")
    if x != -1 and y != -1:
        pag.click(x, y)
    else:
        return {"error": True, "message": "ERR - joinWithComputerAudioBtn.png"}

    # force full screen zoom
    pag.hotkey("winleft", "up")

    return {"error": False, "message": "Success"}


# if this file is ran directly
if __name__ == '__main__':
    with open(f"{CUR_PATH}/config/classes.yaml", 'r') as stream:
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
