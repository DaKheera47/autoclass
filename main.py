import pyautogui as pag
import time
from launcher import main as launcherMain
from helpers import clear, logging, getYamlFiles
import schedule
from datetime import datetime
import cursor
import os
cursor.hide()


def startLaunching(className, code_to_use, password_to_use, currTime):
    # if confirmation is required
    SETUP, CLASS_INFO = getYamlFiles()
    isConfirmed = "OK"
    if SETUP["requireConfirmation"]:
        isConfirmed = pag.confirm(
            text=f'Do you want to join {className} class?',
            title=f'Confirm joining of {className} class',
            buttons=['OK', 'Cancel']
        )

    if isConfirmed == "OK":
        status = launcherMain(code_to_use, password_to_use)
        logging(currTime, className, datetime.today().strftime(
            '%Y-%m-%d'), status["message"])

    checkForClassTime()


def checkForClassTime():
    SETUP, CLASS_INFO = getYamlFiles()
    clear()
    currTime = datetime.now().strftime("%H:%M")
    currDayNum = datetime.today().weekday()

    for cls in CLASS_INFO.items():
        # getting class code
        code_to_use = str(CLASS_INFO[cls[0]]["code"])
        password_to_use = str(CLASS_INFO[cls[0]]["password"])

        # checking if today is between monday and thursday
        if (currTime == cls[1]["time_weekday"] and currDayNum in range(0, 4)):
            startLaunching(cls[0], code_to_use, password_to_use, currTime)
            return

        # checking if today is friday
        if (currTime == cls[1]["time_friday"] and currDayNum == 4):
            startLaunching(cls[0], code_to_use, password_to_use, currTime)
            return


checkForClassTime()
schedule.every(30).seconds.do(checkForClassTime)

while True:
    schedule.run_pending()
    time.sleep(5)
