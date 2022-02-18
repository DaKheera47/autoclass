import pyautogui as pag
import time
import os
import yaml
import sys
import json
from datetime import datetime
from helpers import findAndClick, findAndInputText, loadFiles, clear, bringWindowToFocus, log, getConfigValue
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


def toggleRecording(event="start"):
    # if it can't get it to open
    if not bringWindowToFocus("OBS"):
        if event == "start":
            pag.press("winleft")
            pag.write("OBS Studio")
            pag.press("enter")
            time.sleep(10)
        else:
            # dont launch if OBS isnt running
            return

    pag.hotkey("winleft", "up")
    # start recording button
    pag.click(x=1778, y=908)


def launchClass(className: str):
    SETUP, CLASS_INFO, _ = loadFiles()
    pag.PAUSE = getConfigValue("delayBetweenActions")
    leftMdx = f"""# Now Launching {className}
-   Steps involved:
    -   Open Zoom
    -   Click on Join Now button
    -   Enter Meeting ID
    -   Enter Meeting password
    -   Join with Computer Audio
"""

    for i, cls in enumerate(CLASS_INFO):
        if cls["class"] == className:
            # classDetails = CLASS_INFO
            # generating custom table
            genTable([cls], leftMdx=leftMdx,
                     footer=False, tagline=f"Now Launching {className}")
            code = cls["meeting id"]
            password = cls["meeting password"]

    if getConfigValue("record"):
        # start recording
        toggleRecording()

    # start button
    pag.press("winleft")

    # launch zoom
    pag.write("zoom")
    pag.press("enter")

    findAndClick(["meetingHasEndedConfirmation.png"],
                 MSGS["endedConfirmation"]["searching"],
                 MSGS["endedConfirmation"]["error"], timeout=15, confidence=0.8)

    joinBtn = findAndClick(["joinUnsigned.PNG", "joinBtn.png"],
                           MSGS["join"]["searching"],
                           MSGS["join"]["error"], confidence=0.99)
    if joinBtn["error"]:
        return joinBtn

    # enter code into meeting id field
    joinMeeting = findAndInputText(["joinMeeting.PNG"],
                                   MSGS["enterCode"]["searching"],
                                   MSGS["enterCode"]["error"], code,
                                   confidence=getConfigValue("globalConfidence"))
    if joinMeeting["error"]:
        return joinMeeting

    # enter password into password field
    joinPassword = findAndInputText(["enterMeetingPw.png"],
                                    MSGS["enterPW"]["searching"],
                                    MSGS["enterPW"]["error"], password,
                                    confidence=getConfigValue("globalConfidence"))
    if joinPassword["error"]:
        return joinPassword

    # join with computer audio
    joinWithCompAudioBtn = findAndClick(["joinWithComputerAudioBtn.PNG"],
                                        MSGS["compAudio"]["searching"],
                                        MSGS["compAudio"]["error"],
                                        timeout=60 * 20,
                                        confidence=getConfigValue("globalConfidence"))
    if joinWithCompAudioBtn["error"]:
        return joinWithCompAudioBtn

    # force full screen zoom
    pag.hotkey("winleft", "up")

    # show controls at all times
    pag.press("alt", presses=2)

    return {"error": False, "message": "Success"}


def startLaunching(className):
    # if confirmation is required
    SETUP, CLASS_INFO, _ = loadFiles()
    isConfirmed = "OK"
    if getConfigValue("requireConfirmationBeforeJoining"):
        isConfirmed = pag.confirm(
            text=f'Do you want to join {className} class?',
            title=f'Confirm joining of {className} class',
            buttons=['OK', 'Cancel']
        )

    if isConfirmed == "OK":
        status = launchClass(className["class"])
        log(f'{className["class"]} - {status["message"]}', status["error"])


def startLeaving(cls):
    SETUP, CLASS_INFO, _ = loadFiles()
    CURR_TIME = datetime.now().strftime("%H:%M")
    CURR_DAY_NUM = datetime.today().weekday()
    isConfirmed = "OK"

    # end recording
    toggleRecording(event="end")

    if getConfigValue("requireConfirmationBeforeLeaving"):
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
                log("Left Currently Running Meeting", True)

        else:
            log("No Running Meeting", False)


# if this file is ran directly
if __name__ == '__main__':
    SETUP, CLASS_INFO, _ = loadFiles()

    genTable(CLASS_INFO, tagline="Choose a class from the table above", footer=False)
    cls = input(f"Choose your code here ==>")
    className = CLASS_INFO[int(cls) - 1]["class"]
    # className = list(CLASS_INFO.keys())[int(cls) - 1]
    launchClass(className)
