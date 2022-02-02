import pyautogui as pag
import time
import os
import yaml
import sys
import json
from datetime import datetime
from helpers import findAndClick, findAndInputText, loadFiles, clear, bringWindowToFocus, log
from genTable import genTable
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
    "endedConfirmation": {
        "searching": "Searching if there is a confirmation for has this meeting ended or not",
        "error": "There's no confirmation required!",
    },
}


def launchClass(code, password):
    SETUP, CLASS_INFO, _ = loadFiles()
    pag.PAUSE = SETUP["delayBetweenActions"]

    # start button
    pag.press("winleft")

    # launch zoom
    pag.write("zoom")
    pag.press("enter")

    endedConfirmation = findAndClick("meetingHasEndedConfirmation.PNG",
                           MSGS["endedConfirmation"]["searching"],
                           MSGS["endedConfirmation"]["error"], confidence=0.8)

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


def startLaunching(className, code_to_use, password_to_use):
    # if confirmation is required
    SETUP, CLASS_INFO, _ = loadFiles()
    isConfirmed = "OK"
    if SETUP["requireConfirmationBeforeJoining"]:
        isConfirmed = pag.confirm(
            text=f'Do you want to join {className} class?',
            title=f'Confirm joining of {className} class',
            buttons=['OK', 'Cancel']
        )

    if isConfirmed == "OK":
        status = launchClass(code_to_use, password_to_use)
        log(f"Joined {className}" if not status['error'] else status['message'])


def startLeaving(cls, code_to_use, password_to_use):
    SETUP, CLASS_INFO, _ = loadFiles()
    CURR_TIME = datetime.now().strftime("%H:%M")
    CURR_DAY_NUM = datetime.today().weekday()
    isConfirmed = "OK"

    if SETUP["requireConfirmationBeforeLeaving"]:
        isConfirmed = pag.confirm(
            text=f'Are you sure you want to leave the {cls[0]} class?',
            title=f'Confirm leaving class?',
            buttons=['OK', 'Cancel']
        )

    if isConfirmed == "OK":
        isMeetingRunning = bringWindowToFocus("Zoom Meeting")
        if isMeetingRunning:
            response = findAndClick(["leaveBtn.png"], "Attempting to leave meeting",
                                    "Unable to find leave button", timeout=90)
            if not response["error"]:
                coords = response["coords"]
                # confirm button
                pag.click(coords["x"], coords["y"] - 50)
                log(f"Left {cls[0]}")

        else:
            log(f"{cls[0]} was not running")


# if this file is ran directly
if __name__ == '__main__':
    SETUP, CLASS_INFO, _ = loadFiles()

    genTable(CLASS_INFO, footer=False)
    cls = input(f"Choose your code here ==>")
    className = list(CLASS_INFO.keys())[int(cls) - 1]
    print(list(CLASS_INFO.keys())[int(cls) - 1])

    classToLaunch = CLASS_INFO[list(CLASS_INFO.keys())[int(cls) - 1]]

    leftMdx = """# Instructions
-   Choose your class from the options given in this table
-   The class with the code will be opened
-   The meeting ID and password will be entered automatically
"""
    genTable({className: classToLaunch}, leftMdx=leftMdx, footer=False)

    try:
        chosenClass = list(CLASS_INFO.items())[int(cls) - 1][1]
        launchClass(chosenClass["code"], chosenClass["password"])
    except Exception as e:
        print(f"{e}")
