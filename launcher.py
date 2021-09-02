import pyautogui as pag
import time
import os
import yaml
import sys
import json
import cursor
from helpers import findImage, enterTextInput, findAndClick, findAndInputText

cursor.hide()
CUR_PATH = os.path.dirname(os.path.realpath(__file__))


def main(code, password):
    pag.PAUSE = 0.6
    # start button
    pag.press("winleft")

    # launch zoom
    pag.write("zoom")
    pag.press("enter")

    joinBtn = findAndClick(["joinUnsigned.PNG", "joinBtn.png"],
                           "Searching Join Button",
                           "Couldn't find Join Button")
    if joinBtn["error"]:
        return joinBtn

    # enter code into meeting id field
    joinMeeting = findAndInputText(["joinMeeting.PNG"],
                                   "Searching Join Meeting Text Input",
                                   "Couldn't find Join Meeting Text Input", code)
    if joinMeeting["error"]:
        return joinMeeting

    # enter password into password field
    joinPassword = findAndInputText(["enterMeetingPw.png"],
                                    "Searching for Password Text Input",
                                    "Couldn't find Join Meeting Text Input", password)
    if joinPassword["error"]:
        return joinPassword

    # join with computer audio
    joinWithCompAudioBtn = findAndClick(["joinWithComputerAudioBtn.PNG"],
                                        "Have Not Been Accepted Into Class",
                                        "Couldn't Find Join With Computer Audio Button")
    if joinWithCompAudioBtn["error"]:
        return joinWithCompAudioBtn

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
    except Exception as e:
        print(f"Line 88: {e}")
