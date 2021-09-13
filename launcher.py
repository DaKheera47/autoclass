import pyautogui as pag
import time
import os
import yaml
import sys
import json
import cursor
from helpers import findAndClick, findAndInputText, loadFiles

cursor.hide()
CUR_PATH = os.path.dirname(os.path.realpath(__file__))

MSGS = {
    "join": {
        "searching": "Searching Join Button",
        "error": "Couldn't find Join Button",
    },
    "enterCode": {
        "searching": "Searching Join Meeting Text Input",
        "error": "Couldn't find Join Meeting Text Input",
    },
    "enterPW": {
        "searching": "Searching for Password Text Input",
        "error": "Couldn't find Password Text Input",
    },
    "compAudio": {
        "searching": "Have Not Been Accepted Into Class",
        "error": "Couldn't Find Join With Computer Audio Button or The Host Didn't Allow Entry",
    },
}


def configureOBS():
    SETUP, CLASS_INFO = loadFiles()
    # start button
    pag.press("winleft")

    # launch zoom
    pag.write("OBS")
    pag.press("enter")

    time.sleep(5)

    # tools
    pag.hotkey("alt", "t")

    # output timer
    response = findAndClick(["outputTimer.png"], "Searching for output timer",
                            "Unable to find output timer option", timeout=90)
    if response["error"]:
        return

    # tools
    pag.press("tab", presses=6)
    pag.write(str(SETUP["timeToRecordClass"]))
    # going to start button
    pag.press("tab", presses=2)
    pag.press("enter")


def main(code, password):
    SETUP, CLASS_INFO = loadFiles()
    pag.PAUSE = SETUP["delayBetweenActions"]

    if SETUP["recordClasses"]:
        configureOBS()

    # start button
    pag.press("winleft")

    # launch zoom
    pag.write("zoom")
    pag.press("enter")

    joinBtn = findAndClick(["joinUnsigned.PNG", "joinBtn.png"],
                           MSGS["join"]["searching"],
                           MSGS["join"]["error"])
    if joinBtn["error"]:
        return joinBtn

    # enter code into meeting id field
    joinMeeting = findAndInputText(["joinMeeting.PNG"],
                                   MSGS["enterCode"]["searching"],
                                   MSGS["enterCode"]["error"], code)
    if joinMeeting["error"]:
        return joinMeeting

    # enter password into password field
    joinPassword = findAndInputText(["enterMeetingPw.png"],
                                    MSGS["enterPW"]["searching"],
                                    MSGS["enterPW"]["error"], password)
    if joinPassword["error"]:
        return joinPassword

    # join with computer audio
    joinWithCompAudioBtn = findAndClick(["joinWithComputerAudioBtn.PNG"],
                                        MSGS["compAudio"]["searching"],
                                        MSGS["compAudio"]["error"])
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
