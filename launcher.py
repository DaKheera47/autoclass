import pyautogui as pag
import time
import os
import yaml
import sys
import json
from helpers import findAndClick, findAndInputText, loadFiles
import cursor
cursor.hide()

CUR_PATH = os.path.dirname(os.path.realpath(__file__))
MSGS = {
    "join": {
        "searching": "Locating Join Button",
        "error": "Unable to find Join Button",
    },
    "enterCode": {
        "searching": "Locating Join Meeting Text Input",
        "error": "Unable to find Join Meeting Text Input",
    },
    "enterPW": {
        "searching": "Locating Password Text Input",
        "error": "Unable to find Password Text Input",
    },
    "compAudio": {
        "searching": "Have Not Been Accepted Into Class",
        "error": "Couldn't Find Join With Computer Audio Button or The Host Didn't Allow Entry",
    },
}


def main(code, password):
    SETUP, CLASS_INFO = loadFiles()
    pag.PAUSE = SETUP["delayBetweenActions"]

    # start button
    pag.press("winleft")

    # launch zoom
    pag.write("zoom")
    pag.press("enter")

    joinBtn = findAndClick(["joinUnsigned.PNG", "joinBtn.png"],
                           MSGS["join"]["searching"],
                           MSGS["join"]["error"], confidence=0.99)
    if joinBtn["error"]:
        return joinBtn

    # enter code into meeting id field
    joinMeeting = findAndInputText(["joinMeeting.PNG"],
                                   MSGS["enterCode"]["searching"],
                                   MSGS["enterCode"]["error"], code,
                                   confidence=SETUP["globalConfidence"])
    if joinMeeting["error"]:
        return joinMeeting

    # enter password into password field
    joinPassword = findAndInputText(["enterMeetingPw.png"],
                                    MSGS["enterPW"]["searching"],
                                    MSGS["enterPW"]["error"], password,
                                    confidence=SETUP["globalConfidence"])
    if joinPassword["error"]:
        return joinPassword

    # join with computer audio
    joinWithCompAudioBtn = findAndClick(["joinWithComputerAudioBtn.PNG"],
                                        MSGS["compAudio"]["searching"],
                                        MSGS["compAudio"]["error"],
                                        confidence=SETUP["globalConfidence"])
    if joinWithCompAudioBtn["error"]:
        return joinWithCompAudioBtn

    # force full screen zoom
    pag.hotkey("winleft", "up")

    # show controls at all times
    pag.press("alt", presses=2)

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
        print(f"Line 138: {e}")
