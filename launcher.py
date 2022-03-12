import pyautogui as pag
import time
import os
from datetime import timedelta, datetime
from helpers import findAndClick, findAndInputText, loadFiles, bringWindowToFocus, log, getConfigValue, resetPrograms
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
        "searching": "Locate end free meeting button",
        "error": "There's no confirmation required!",
    },
    "waitForHost": {
        "searching": "Checking previous class",
        "error": "No previously running class",
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
    _, CLASS_INFO, _ = loadFiles(prune=False)
    pag.PAUSE = getConfigValue("delayBetweenActions")

    for i, cls in enumerate(CLASS_INFO):
        if cls["class"] == className:
            # generating custom table
            genTable([cls], footer=False, tagline=f"Now Launching {className}")
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

    waitForHost = findAndClick(["waitForHost.png"],
                               MSGS["waitForHost"]["searching"],
                               MSGS["waitForHost"]["error"], timeout=5, confidence=0.8)
    if not waitForHost["error"]:
        pag.hotkey("alt", "f4")

    joinBtn = findAndClick(["joinUnsigned.png", "joinBtn.png"],
                           MSGS["join"]["searching"],
                           MSGS["join"]["error"], confidence=0.9)
    if joinBtn["error"]:
        return joinBtn

    # enter code into meeting id field
    joinMeeting = findAndInputText(["joinMeeting.png"],
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
    joinWithCompAudioBtn = findAndClick(["joinWithComputerAudioBtn.png"],
                                        MSGS["compAudio"]["searching"],
                                        MSGS["compAudio"]["error"], timeout=3 * 60)
    if joinWithCompAudioBtn["error"]:
        return joinWithCompAudioBtn

    # force full screen zoom
    pag.hotkey("winleft", "up")

    # show controls at all times
    pag.press("alt", presses=2)

    return {"error": False, "message": "Success"}


def startLaunching(className):
    # if confirmation is required
    isConfirmed = "OK"
    if getConfigValue("requireConfirmationBeforeJoining"):
        isConfirmed = pag.confirm(
            text=f'Do you want to join {className["class"]} class?',
            title=f'Confirm joining of {className["class"]} class',
            buttons=['OK', 'Cancel']
        )

    delta = timedelta(minutes=int(getConfigValue("timeFromEndToCheck")))
    delta = datetime.strptime(className["leave time"], "%H:%M") - delta

    if isConfirmed == "OK":
        now = datetime.now()
        nowFormatted = datetime.strptime(now.strftime("%H:%M"), "%H:%M")

        while nowFormatted > delta:
            status = launchClass(className["class"])
            if status["error"]:
                resetPrograms()
                continue
            else:
                out = f'{className["class"]} - {status["message"]}'
                log(out, not bool(status["error"]))
                break


def startLeaving(className):
    isConfirmed = "OK"

    if getConfigValue("requireConfirmationBeforeLeaving"):
        isConfirmed = pag.confirm(
            text=f'Are you sure you want to leave the {className["class"]} class?',
            title=f'Confirm leaving class?',
            buttons=['OK', 'Cancel']
        )

    if isConfirmed == "OK":
        # close meeting
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

        # end recording
        toggleRecording(event="end")


# if this file is ran directly
if __name__ == '__main__':
    SETUP, CLASS_INFO, _ = loadFiles(prune=False)

    genTable(CLASS_INFO, footer=False)
    cls = input(f"Choose your code here ==>")
    className = CLASS_INFO[int(cls) - 1]
    startLaunching(className)
