import pyautogui as pag
import time
from launcher import main as launcherMain
from helpers import clear, logging, getYamlFiles
import schedule
from datetime import datetime
import cursor
import os
cursor.hide()


def checkForClassTime():
    SETUP, CLASS_INFO = getYamlFiles()
    clear()
    currTime = datetime.now().strftime("%H:%M")

    for cls in CLASS_INFO.items():
        if currTime == cls[1]["time_weekday"]:
            # getting class code
            code_to_use = str(CLASS_INFO[cls[0]]["code"])
            password_to_use = str(CLASS_INFO[cls[0]]["password"])

            print(
                f"\nUsing {cls[0]} class information \n  Code: {code_to_use} \n  Pass: {password_to_use}")

            # if confirmation is required
            if SETUP["requireConfirmation"]:
                isConfirmed = pag.confirm(
                    text=f'Join {cls[0]} class?', title=f'Confirm joining of {cls[0]} class', buttons=['OK', 'Cancel'])

                if isConfirmed == "OK":
                    status = launcherMain(code_to_use, password_to_use)

                    logging(currTime, cls[0], datetime.today().strftime(
                        '%Y-%m-%d'), status["message"])

                    checkForClassTime()

            # if confirmation not needed
            else:
                status = launcherMain(code_to_use, password_to_use)

                logging(currTime, cls[0], datetime.today().strftime(
                    '%Y-%m-%d'), status["message"])

                checkForClassTime()


checkForClassTime()
schedule.every(30).seconds.do(checkForClassTime)

while True:
    schedule.run_pending()
    time.sleep(5)
