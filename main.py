import pyautogui as pag
import time
from launcher import main as launcherMain
from helpers import clear, logging, loadFiles, bringWindowToFocus, findAndClick
from genTable import genTable
import schedule
from datetime import datetime
import cursor
import os
cursor.hide()


def startLaunching(className, code_to_use, password_to_use, currTime):
    # if confirmation is required
    SETUP, CLASS_INFO = loadFiles()
    isConfirmed = "OK"
    if SETUP["requireConfirmationBeforeJoining"]:
        isConfirmed = pag.confirm(
            text=f'Do you want to join {className} class?',
            title=f'Confirm joining of {className} class',
            buttons=['OK', 'Cancel']
        )

    if isConfirmed == "OK":
        status = launcherMain(code_to_use, password_to_use)
        logging(currTime, className, datetime.today().strftime(
            '%Y-%m-%d'), status["message"])


def startLeaving():
    SETUP, CLASS_INFO = loadFiles()
    isConfirmed = "OK"
    if SETUP["requireConfirmationBeforeLeaving"]:
        isConfirmed = pag.confirm(
            text=f'Are you sure you want to leave the currently running class?',
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
    
    checkForClassTime()


def checkForClassTime():
    SETUP, CLASS_INFO = loadFiles()
    clear()
    genTable()
    CURR_TIME = datetime.now().strftime("%H:%M")
    CURR_DAY_NUM = datetime.today().weekday()

    for cls in CLASS_INFO.items():
        # getting class code
        code_to_use = str(CLASS_INFO[cls[0]]["code"])
        password_to_use = str(CLASS_INFO[cls[0]]["password"])

        # checking if today is between monday and thursday before joining
        if (CURR_TIME == cls[1]["time_weekday"] and CURR_DAY_NUM in range(0, 4)):
            startLaunching(cls[0], code_to_use, password_to_use, CURR_TIME)
            return

        # checking if today is friday before joining
        if (CURR_TIME == cls[1]["time_friday"] and CURR_DAY_NUM == 4):
            startLaunching(cls[0], code_to_use, password_to_use, CURR_TIME)
            return

        # checking if today is friday before leaving
        if (CURR_TIME == cls[1]["time_of_leaving_friday"] and CURR_DAY_NUM == 4):
            startLeaving()
            return

        # checking if today is weekday before leaving
        if (CURR_TIME == cls[1]["time_of_leaving_weekday"] and CURR_DAY_NUM in range(0, 4)):
            startLeaving()
            return


checkForClassTime()
schedule.every(60).seconds.do(checkForClassTime)

while True:
    schedule.run_pending()
    time.sleep(30)
