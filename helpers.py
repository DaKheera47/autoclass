import cursor
import os
import time
import pyautogui as pag
import json
import yaml
from rich import print
from datetime import datetime
from collections import OrderedDict
from rich.progress import Progress
from win32gui import IsWindowVisible, GetWindowText, EnumWindows, ShowWindow, SetForegroundWindow, SystemParametersInfo
CUR_PATH = os.path.dirname(os.path.realpath(__file__))
cursor.hide()
defaultTimeout = 600


def loadFiles():
    CURR_DAY_NUM = datetime.today().weekday()

    if not os.path.exists(os.path.dirname(f"{CUR_PATH}/config/classes.yaml")):
        try:
            os.makedirs(os.path.dirname(f"{CUR_PATH}/config/classes.yaml"))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # making new classes file if it doesnt already exist
    if not os.path.exists(f"{CUR_PATH}/config/classes.yaml"):
        file = open(f"{CUR_PATH}/config/classes.yaml", "w")
        SAMPLE_CLASS = {
            "Default Class": {
                "code": 'Change code',
                "password": 'Change Password',
                "time_friday": "00:00",
                "time_of_leaving_friday": "00:01",
                "time_of_leaving_weekday": "00:01",
                "time_weekday": "00:00"
            }
        }

        yaml.dump(SAMPLE_CLASS, file)
        file.close()

    if not os.path.exists(f"{CUR_PATH}/config/config.yaml"):
        file = open(f"{CUR_PATH}/config/config.yaml", "w")
        SAMPLE_CONFIG = [
            {'description': 'Delay between every action taken', 'value': 0.8},
            {'description': 'Percentage accuracy to match image', 'value': 0.99},
            {'description': 'Confirm before joining', 'value': False},
            {'description': 'Confirm before leaving', 'value': False},
            {'description': 'Record meetings with OBS Studio', 'value': True}
        ]

        yaml.dump(SAMPLE_CONFIG, file)
        file.close()

    # https://rich.readthedocs.io/en/stable/appendix/colors.html
    if not os.path.exists(f"{CUR_PATH}/config/styles.yaml"):
        file = open(f"{CUR_PATH}/config/styles.yaml", "w")
        SAMPLE_CONFIG = {
            "text-color": "white",
            "future": "cyan",
            "past": "bright_black",
            "enabled": "green",
            "disabled": "red",
            "highlight": "cyan",
        }

        yaml.dump(SAMPLE_CONFIG, file)
        file.close()

    # importing external files
    with open(f"{CUR_PATH}/config/config.yaml", 'r') as stream:
        try:
            SETUP = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(f"{CUR_PATH}/config/classes.yaml", 'r') as stream:
        try:
            CLASS_INFO = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(f"{CUR_PATH}/config/styles.yaml", 'r') as stream:
        try:
            COLORS = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # sorting classes
    # https://stackoverflow.com/questions/42398375/sorting-a-dictionary-of-dictionaries-python
    if CURR_DAY_NUM == 4:
        # friday timings
        CLASS_INFO = OrderedDict(
            sorted(CLASS_INFO.items(), key=lambda x: x[1]["time_friday"]))
    else:
        # any other day
        CLASS_INFO = OrderedDict(
            sorted(CLASS_INFO.items(), key=lambda x: x[1]["time_weekday"]))

    # removing classes with 0 duration, to indicate no class
    for index, clsName in enumerate(list(CLASS_INFO.keys()), start=1):
        timeJoining = datetime.strptime(
            CLASS_INFO[clsName]["time_friday" if CURR_DAY_NUM == 4 else "time_weekday"], "%H:%M")
        timeLeaving = datetime.strptime(
            CLASS_INFO[clsName]["time_of_leaving_friday" if CURR_DAY_NUM == 4 else "time_of_leaving_weekday"], "%H:%M")

        # https://stackoverflow.com/questions/3096953/how-to-calculate-the-time-interval-between-two-time-strings
        durationOfClass = timeLeaving - timeJoining
        CLASS_INFO[clsName]["duration"] = str(durationOfClass)[:-3]

        if str(durationOfClass) == "0:00:00":
            del CLASS_INFO[clsName]

    return SETUP, CLASS_INFO, COLORS


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def findImage(imageUrl: str, confidence: int):
    try:
        x, y = pag.locateCenterOnScreen(
            f"{CUR_PATH}/static/{imageUrl}", confidence=confidence)
        return (x, y)
    except TypeError:
        return (-1, -1)


def enterTextInput(x: int, y: int, text: str, message: str):
    pag.click(x=x, y=y)
    pag.write(text.replace(" ", ""))
    pag.press("enter")


def findImageTimeout(imageUrl: str, message: str, timeout: int = defaultTimeout, confidence: int = 0.90):
    i = 1
    while True:
        if i <= timeout:
            try:
                x, y = pag.locateCenterOnScreen(
                    f"{CUR_PATH}/static/{imageUrl}", confidence=confidence)
            except TypeError:
                time.sleep(1)
                i += 1
                continue
            break
        else:
            return (-1, -1)

    return (x, y)


def findAndClick(imageUrls: list, message: str, errorMessage: str,  timeout: int = defaultTimeout, confidence: int = 0.95):
    output = {}
    i = 0

    with Progress(transient=True) as progress:
        task = progress.add_task(f"{message}...", start=False, total=timeout)

        while not progress.finished:
            if i <= timeout:
                for imageUrl in imageUrls:
                    t1 = time.time()
                    x, y = findImage(imageUrl, confidence)
                    # calculating time taken to find this image
                    t2 = time.time() - t1
                    if x != -1 and y != -1:
                        pag.click(x, y)
                        progress.stop()
                        return {"error": False, "message": None, "coords": {"x": x, "y": y}}
                        break
                    else:
                        # calculating amount to increase based on time taken by image to attempt to find
                        amountToIncrease = (
                            len(imageUrls) * t2 / len(imageUrls))
                        i += amountToIncrease
                        progress.update(task, advance=amountToIncrease)
            else:
                progress.stop()
                return {"error": True, "message": f"Timed Out: {errorMessage}"}


def findAndInputText(imageUrls: list, message: str, errorMessage: str, textToInput: str, timeout: int = defaultTimeout, confidence: int = 0.95):
    output = {}
    i = 0

    with Progress(transient=True) as progress:
        task = progress.add_task(f"{message}...", start=False, total=timeout)

        while not progress.finished:
            if i <= timeout:
                for imageUrl in imageUrls:
                    t1 = time.time()
                    x, y = findImage(imageUrl, confidence)
                    # calculating time taken to find this image
                    t2 = time.time() - t1
                    if x != -1 and y != -1:
                        pag.click(x, y + 60)
                        pag.write(str(textToInput).replace(" ", ""))
                        pag.press("enter")
                        progress.stop()
                        return {"error": False, "message": None}
                    else:
                        # calculating amount to increase based on time taken by image to attempt to find
                        amountToIncrease = (
                            len(imageUrls) * t2 / len(imageUrls))
                        i += amountToIncrease
                        progress.update(task, advance=amountToIncrease)
            else:
                progress.stop()
                return {"error": True, "message": f"Timed Out: {errorMessage}"}


def log(message: str):
    now = datetime.now()
    fileName = "%s_%s_%s.json" % (
        now.year,
        str(now.month).rjust(2, "0"),
        str(now.day).rjust(2, "0"),
    )

    if not os.path.exists(os.path.dirname(f"{CUR_PATH}/out/{fileName}")):
        try:
            os.makedirs(os.path.dirname(f"{CUR_PATH}/out/{fileName}"))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # making new classes file if it doesnt already exist
    if not os.path.exists(f"{CUR_PATH}/out/{fileName}"):
        file = open(f"{CUR_PATH}/out/{fileName}", "w")
        placeholder = []
        json.dump(placeholder, file)
        file.close()

    CURR_TIME = datetime.now().strftime("%H:%M")
    CURR_DATE = datetime.now().strftime("%d-%m-%Y")

    finalOutput = {
        "time": CURR_TIME,
        "date": CURR_DATE,
        "message": message,
    }

    with open(f"{CUR_PATH}/out/{fileName}", "r+") as f:
        output = []
        fileData = json.loads(f.read())
        for entry in fileData:
            output.append(entry)
        output.append(finalOutput)

        f.seek(0)
        json.dump(output, f)


def bringWindowToFocus(partial_window_name):
    def window_enum_handler(hwnd, resultList):
        if IsWindowVisible(hwnd) and GetWindowText(hwnd) != '':
            resultList.append((hwnd, GetWindowText(hwnd)))
    # SystemParametersInfo(8193, 0, 2 | 1)
    handles = []
    EnumWindows(window_enum_handler, handles)
    for i in handles:
        if str(partial_window_name).upper() in str(i[1]).upper():
            ShowWindow(i[0], 3)
            SetForegroundWindow(i[0])
            return True
    return False


def differenceNowToTime(time1):
    # time must be in %H:%M format
    CURR_TIME = datetime.now().strftime("%H:%M")
    return str(datetime.strptime(time1, "%H:%M") - datetime.strptime(CURR_TIME, "%H:%M"))[:-3]


def getNextClass():
    SETUP, CLASS_INFO, _ = loadFiles()
    CURR_TIME = datetime.now().strftime("%H:%M")
    CURR_DAY_NUM = datetime.today().weekday()

    # find next class join or leave time
    for cls in list(CLASS_INFO.keys()):
        CURR_CLASS = CLASS_INFO[cls]

        if CURR_DAY_NUM == 4:

            if CURR_TIME < CLASS_INFO[cls]["time_friday"]:
                # time to next class
                TTNC = differenceNowToTime(CURR_CLASS["time_friday"])
                return {"class": cls, "event": "Joining", "timeTillNextEvent": TTNC}

            if CURR_TIME < CLASS_INFO[cls]["time_of_leaving_friday"]:
                TTNC = differenceNowToTime(
                    CURR_CLASS["time_of_leaving_friday"])
                return {"class": cls, "event": "Leaving", "timeTillNextEvent": TTNC}

        if CURR_DAY_NUM in range(0, 4):

            if CURR_TIME < CLASS_INFO[cls]["time_weekday"]:
                TTNC = differenceNowToTime(CURR_CLASS["time_weekday"])
                return {"class": cls, "event": "Joining", "timeTillNextEvent": TTNC}

            if CURR_TIME < CLASS_INFO[cls]["time_of_leaving_weekday"]:
                TTNC = differenceNowToTime(
                    CURR_CLASS["time_of_leaving_weekday"])
                return {"class": cls, "event": "Leaving", "timeTillNextEvent": TTNC}
