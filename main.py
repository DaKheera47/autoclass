from launcher import launchClass, startLaunching, startLeaving
from helpers import loadFiles, getConfigValue
from genTable import genTable
import schedule
from datetime import datetime
import time
from functools import partial
import cursor
cursor.hide()


def checkForClassTime():
    SETUP, CLASS_INFO, _ = loadFiles()
    CURR_TIME = datetime.now().strftime("%H:%M")
    CURR_DAY_NUM = datetime.today().weekday()
    EVENT_LOOP = []

    genTable(CLASS_INFO)

    for cls in CLASS_INFO:
        # getting class code
        code_to_use = str(cls["meeting id"])
        password_to_use = str(cls["meeting password"])

        # add a launch event to event loop if join time
        if CURR_TIME == cls["join time"]:
            EVENT_LOOP.append((partial(startLaunching, cls)))

        # add a leave event to event loop if leaving time
        if CURR_TIME == cls["leave time"]:
            EVENT_LOOP.append((partial(startLeaving, cls)))

    for event in EVENT_LOOP:
        event()


checkForClassTime()
schedule.every(60).seconds.do(checkForClassTime)

while True:
    schedule.run_pending()
    time.sleep(30)
