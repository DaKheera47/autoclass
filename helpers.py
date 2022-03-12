import cursor
import os
import time
import pyautogui as pag
import json
import yaml
from datetime import datetime, timedelta
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, TimeElapsedColumn
import csv

CUR_PATH = os.path.dirname(os.path.realpath(__file__))
CUR_PATH_CONFIG = f"{CUR_PATH}/config"
cursor.hide()
defaultTimeout = 1 * 60

SAMPLE_CLASS = [
    ["Class", "Day", "Meeting ID", "Meeting Password",
     "Join Time", "Leave Time"],
    ["Test Class", "Monday", "Update Me!", "Update Me!", "00:00", "00:01"],
    ["Test Class", "Tuesday", "Update Me!",
     "Update Me!", "00:00", "00:01"],
    ["Test Class", "Wednesday", "Update Me!",
     "Update Me!", "00:00", "00:01"],
    ["Test Class", "Thursday", "Update Me!",
     "Update Me!", "00:00", "00:01"],
    ["Test Class", "Friday", "Update Me!", "Update Me!", "00:00", "00:01"],
    ["Test Class", "Saturday", "Update Me!",
     "Update Me!", "00:00", "00:01"],
    ["Test Class", "Sunday", "Update Me!", "Update Me!", "00:00", "00:01"],
]

SAMPLE_CONFIG = [
    {'description': 'Delay between every action taken',
     'value': 0.8, 'name': 'delayBetweenActions', "suffix": "s"},
    {'description': 'Percentage accuracy to match image',
     'value': 0.99, 'name': 'globalConfidence', "suffix": "%"},
    {'description': 'Confirm before joining', 'value': False,
     'name': 'requireConfirmationBeforeJoining', "suffix": ""},
    {'description': 'Confirm before leaving', 'value': False,
     'name': 'requireConfirmationBeforeLeaving', "suffix": ""},
    {'description': 'Record meetings with OBS Studio',
     'value': True, 'name': 'record', "suffix": ""},
    {'description': 'Prune past classes of the day',
     'value': True, 'name': 'prune', "suffix": ""},
    {'description': 'Fixed late-ness in joining time',
     'value': 0, 'name': 'lateness', "suffix": "mins"},
    {'description': 'Time from end to keep joining',
     'value': 10, 'name': 'timeFromEndToCheck', "suffix": "mins"},
]

SAMPLE_STYLES = {
    "text-color": "white",
    "future": "cyan",
    "past": "bright_black",
    "enabled": "green",
    "disabled": "red",
    "highlight": "cyan",
}


def getConfigValue(name: str):
    SETUP = getFileData(f"{CUR_PATH_CONFIG}/config.yaml",
                        SAMPLE_CONFIG, "yaml")

    for option in SETUP:
        for _, value in option.items():
            if value == name:
                return option["value"]


def getFileData(path: str, data: dict, fileType: str):
    # create folder
    os.makedirs(f"{CUR_PATH}/config", exist_ok=True)

    if not os.path.exists(path):
        if fileType == "yaml":
            with open(path, "w") as f:
                yaml.dump(data, f)
            return data

        if fileType == "csv":
            with open(path, "w") as csv_file:
                writer = csv.writer(csv_file)

                for i, value in enumerate(data):
                    writer.writerow(value)

                timings = []
                with open(path, "r") as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    line_count = 0
                    for row in csv_reader:
                        if line_count == 0:
                            line_count += 1
                        timings.append(row)
                        line_count += 1
                return timings
    # if path exists
    else:
        if fileType == "yaml":
            # read
            with open(path, 'r') as stream:
                try:
                    return yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)

        if fileType == "csv":
            # read
            timings = []
            with open(path, "r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    timings.append(row)
                    line_count += 1
            return timings


def loadFiles(prune: bool = None):
    prune = getConfigValue("prune")

    # create default settings if they dont exist already
    TIMINGS = getFileData(
        f"{CUR_PATH_CONFIG}/classes.csv", SAMPLE_CLASS, "csv")
    SETUP = getFileData(f"{CUR_PATH_CONFIG}/config.yaml",
                        SAMPLE_CONFIG, "yaml")
    # https://rich.readthedocs.io/en/stable/appendix/colors.html
    COLORS = getFileData(
        f"{CUR_PATH_CONFIG}/styles.yaml", SAMPLE_STYLES, "yaml")

    # cleaning up collected data
    now = datetime.now()
    TODAY = now.strftime("%A")
    CLASS_INFO = []

    # adding correct data to CLASS_INFO
    for i, time in enumerate(TIMINGS):
        # converting keys to lowercase
        time = {k.lower(): v for k, v in time.items()}

        if time["day"] == TODAY:
            delta = timedelta(minutes=int(getConfigValue("lateness")))

            # converting string time to datetime
            joinDatetimeDelta = datetime.strptime(
                time["join time"], "%H:%M") + delta
            joinDatetime = datetime.strptime(time["join time"], "%H:%M")
            leaveDatetime = datetime.strptime(time["leave time"], "%H:%M")

            # converting datetime object to correct string format ie 09:40
            time["join time"] = joinDatetimeDelta.strftime("%H:%M")
            time["leave time"] = leaveDatetime.strftime("%H:%M")

            # setting duration
            durationOfClassDelta = str(leaveDatetime - joinDatetimeDelta)[:-3]
            durationOfClass = str(leaveDatetime - joinDatetime)[:-3]
            time["duration"] = durationOfClassDelta

            # converting twice removes date and leaves only time
            now = datetime.strptime(now.strftime("%H:%M"), "%H:%M")
            # dont add classes with 0 duration, to indicate no class
            if str(durationOfClass) == "0:00":
                continue
            # dont add past classes, if pruning enabled
            if prune and now > leaveDatetime:
                continue

            CLASS_INFO.append(time)

    # sort according to joinTime
    CLASS_INFO = sorted(CLASS_INFO, key=lambda d: d['join time'])
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


def findAndClick(imageUrls: list, message: str, errorMessage: str,  timeout: int = defaultTimeout, confidence: int = getConfigValue("globalConfidence")):
    i = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        transient=True,
        refresh_per_second=60,
        speed_estimate_period=30,
        expand=True
    ) as progress:
        task = progress.add_task(f"{message}...", total=timeout)

        while not progress.finished:
            if i < timeout:
                for imageUrl in imageUrls:
                    t1 = time.time()
                    x, y = findImage(imageUrl, confidence)
                    # calculating time taken to find this image
                    t2 = time.time() - t1
                    if x != -1 and y != -1:
                        pag.click(x, y)
                        progress.stop_task(task)
                        progress.stop()
                        return {"error": False, "message": None, "coords": {"x": x, "y": y}}
                        break
                    else:
                        # calculating amount to increase based on time taken by image to attempt to find
                        amountToIncrease = (
                            len(imageUrls) * t2 / len(imageUrls))
                        if (i + amountToIncrease) <= timeout:
                            i += amountToIncrease
                            progress.update(task, advance=amountToIncrease)
                        else:
                            i = timeout
                            break
            else:
                progress.stop_task(task)
                progress.stop()
                return {"error": True, "message": f"Timed Out: {errorMessage}"}


def findAndInputText(imageUrls: list, message: str, errorMessage: str, textToInput: str, timeout: int = defaultTimeout, confidence: int = getConfigValue("globalConfidence")):
    i = 0
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        transient=True,
        refresh_per_second=60,
        speed_estimate_period=30,
        expand=True
    ) as progress:
        task = progress.add_task(f"{message}...", total=timeout)

        while not progress.finished:
            if i < timeout:
                for imageUrl in imageUrls:
                    t1 = time.time()
                    x, y = findImage(imageUrl, confidence)
                    # calculating time taken to find this image
                    t2 = time.time() - t1
                    if x != -1 and y != -1:
                        pag.click(x, y + 60)
                        pag.write(str(textToInput).replace(" ", ""))
                        pag.press("enter")
                        progress.stop_task(task)
                        progress.stop()
                        return {"error": False, "message": None}
                    else:
                        # calculating amount to increase based on time taken by image to attempt to find
                        amountToIncrease = (
                            len(imageUrls) * t2 / len(imageUrls))
                        if (i + amountToIncrease) <= timeout:
                            i += amountToIncrease
                            progress.update(task, advance=amountToIncrease)
                        else:
                            i = timeout
                            break
            else:
                progress.stop_task(task)
                progress.stop()
                return {"error": True, "message": f"Timed Out: {errorMessage}"}


def log(message: str, success: bool):
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
            pass

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
        "success": success,
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
    partial_window_name = partial_window_name.lower()
    import sys
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        from win32gui import IsWindowVisible, GetWindowText, EnumWindows, ShowWindow, SetForegroundWindow, SystemParametersInfo    
        def window_enum_handler(hwnd, resultList):
            if IsWindowVisible(hwnd) and GetWindowText(hwnd) != '':
                resultList.append((hwnd, GetWindowText(hwnd)))
        handles = []
        EnumWindows(window_enum_handler, handles)
        for i in handles:
            if str(partial_window_name).upper() in str(i[1]).upper():
                ShowWindow(i[0], 3)
                SetForegroundWindow(i[0])
                return True
        return False

    elif sys.platform in ['linux', 'linux2']:
        # linux
        for program in os.popen("wmctrl -l").read().split("\n"):
            if partial_window_name in program.lower():
                os.popen(f"wmctrl -a {partial_window_name}")
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
    for CURR_CLASS in CLASS_INFO:
        timeToJoining = differenceNowToTime(CURR_CLASS["join time"])
        timeToLeaving = differenceNowToTime(CURR_CLASS["leave time"])

        if CURR_TIME < CURR_CLASS["join time"]:
            return {"class": CURR_CLASS["class"], "event": "Joining", "timeTillNextEvent": timeToJoining}

        if CURR_TIME < CURR_CLASS["leave time"]:
            return {"class": CURR_CLASS["class"], "event": "Leaving", "timeTillNextEvent": timeToLeaving}


def resetPrograms(procs: list = ["Zoom", "obs64"]):
    import psutil

    for proc in psutil.process_iter():
        for process in procs:
            if process.lower() in proc.name().lower():
                proc.kill()
