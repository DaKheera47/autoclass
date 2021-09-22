import pyautogui as pag
import time
from launcher import main as launcherMain
from helpers import clear, logging, loadFiles, bringWindowToFocus, findAndClick
from genTable import genTable
import schedule
from datetime import datetime
import os
import cursor
cursor.hide()


def startLaunching(className, code_to_use, password_to_use):
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
        logging(f"{className} - {status['message']}")


def startLeaving(cls, code_to_use, password_to_use):
    SETUP, CLASS_INFO = loadFiles()
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
                logging(f"Successfully left {cls[0]}")

        else:
            logging(f"{cls[0]} was not running")

        # checking if today is between monday and thursday before joining
        if (CURR_TIME == cls[1]["time_weekday"] and CURR_DAY_NUM in range(0, 4)):
            startLaunching(cls[0], code_to_use, password_to_use)
            return

        # checking if today is friday before joining
        if (CURR_TIME == cls[1]["time_friday"] and CURR_DAY_NUM == 4):
            startLaunching(cls[0], code_to_use, password_to_use)
            return


def checkForClassTime():
    SETUP, CLASS_INFO = loadFiles()
    CURR_TIME = datetime.now().strftime("%H:%M")
    CURR_DAY_NUM = datetime.today().weekday()
    clear()
    genTable()

    for cls in CLASS_INFO.items():
        # getting class code
        code_to_use = str(CLASS_INFO[cls[0]]["code"])
        password_to_use = str(CLASS_INFO[cls[0]]["password"])

        # checking if today is between monday and thursday before joining
        if (CURR_TIME == cls[1]["time_weekday"] and CURR_DAY_NUM in range(0, 4)):
            startLaunching(cls[0], code_to_use, password_to_use)
            return

        # checking if today is friday before joining
        if (CURR_TIME == cls[1]["time_friday"] and CURR_DAY_NUM == 4):
            startLaunching(cls[0], code_to_use, password_to_use)
            return

        # checking if today is friday before leaving
        if (CURR_TIME == cls[1]["time_of_leaving_friday"] and CURR_DAY_NUM == 4):
            startLeaving(cls, code_to_use, password_to_use)
            return

        # checking if today is weekday before leaving
        if (CURR_TIME == cls[1]["time_of_leaving_weekday"] and CURR_DAY_NUM in range(0, 4)):
            startLeaving(cls, code_to_use, password_to_use)
            return


checkForClassTime()
schedule.every(60).seconds.do(checkForClassTime)

while True:
    schedule.run_pending()
    time.sleep(30)
