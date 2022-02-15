import pyautogui as pag
import time
from launcher import launchClass, startLaunching, startLeaving
from helpers import loadFiles
from genTable import genTable
import schedule
from datetime import datetime
import os
from functools import partial
import cursor
cursor.hide()

# If True, save screenshots for clicks and key presses.
pag.LOG_SCREENSHOTS = True

# If not None, PyAutoGUI deletes old screenshots when this limit has been reached:
pag.LOG_SCREENSHOTS_LIMIT = 50


def checkForClassTime():
    SETUP, CLASS_INFO, _ = loadFiles()
    CURR_TIME = datetime.now().strftime("%H:%M")
    CURR_DAY_NUM = datetime.today().weekday()
    EVENT_LOOP = []

    genTable(CLASS_INFO)

    for cls in CLASS_INFO.items():
        # getting class code
        code_to_use = str(CLASS_INFO[cls[0]]["code"])
        password_to_use = str(CLASS_INFO[cls[0]]["password"])

        # checking if today is between monday and thursday before joining
        if CURR_TIME == cls[1]["time_weekday"] and CURR_DAY_NUM in range(0, 4):
            EVENT_LOOP.append((partial(startLaunching, cls[0])))

        # checking if today is friday before joining
        if CURR_TIME == cls[1]["time_friday"] and CURR_DAY_NUM == 4:
            EVENT_LOOP.append((partial(startLaunching, cls[0])))

        # checking if today is friday before leaving
        if CURR_TIME == cls[1]["time_of_leaving_friday"] and CURR_DAY_NUM == 4:
            EVENT_LOOP.append(
                (partial(startLeaving, cls, code_to_use, password_to_use)))

        # checking if today is weekday before leaving
        if CURR_TIME == cls[1]["time_of_leaving_weekday"] and CURR_DAY_NUM in range(0, 4):
            EVENT_LOOP.append(
                (partial(startLeaving, cls, code_to_use, password_to_use)))

    for event in EVENT_LOOP:
        event()


checkForClassTime()
schedule.every(60).seconds.do(checkForClassTime)

while True:
    schedule.run_pending()
    time.sleep(30)
