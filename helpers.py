import os
import time
import pyautogui as pag
import json
import yaml
from datetime import datetime
from collections import OrderedDict
from rich.progress import Progress
from win32gui import IsWindowVisible, GetWindowText, EnumWindows, ShowWindow, SetForegroundWindow, SystemParametersInfo


def logToTxt(command: str):
    # logging command executed
    with open(f"{CUR_PATH}/out/log.txt", "a") as f:
        f.write(f"{command}\n")


def loadFiles():
    CURR_DAY_NUM = datetime.today().weekday()
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

    return SETUP, CLASS_INFO


CUR_PATH = os.path.dirname(os.path.realpath(__file__))


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


def findImageTimeout(imageUrl: str, message: str, timeout: int = 10 * 60, confidence: int = 0.90):
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


def findAndClick(imageUrls: list, message: str, errorMessage: str,  timeout: int = 60 * 10, confidence: int = 0.95):
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
                        logToTxt(message)
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
                logToTxt(errorMessage)
                return {"error": True, "message": f"Timed Out: {errorMessage}"}


def findAndInputText(imageUrls: list, message: str, errorMessage: str, textToInput: str, timeout: int = 60 * 10, confidence: int = 0.95):
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
                        pag.write(textToInput.replace(" ", ""))
                        pag.press("enter")
                        progress.stop()
                        logToTxt(message)
                        return {"error": False, "message": None}
                    else:
                        # calculating amount to increase based on time taken by image to attempt to find
                        amountToIncrease = (
                            len(imageUrls) * t2 / len(imageUrls))
                        i += amountToIncrease
                        progress.update(task, advance=amountToIncrease)
            else:
                logToTxt(errorMessage)
                progress.stop()
                return {"error": True, "message": f"Timed Out: {errorMessage}"}


def logging(time: str, className: str, date: str, status: str):
    # logging classes entered
    currClassInfo = {
        "time": time,
        "className": className,
        "date": date,
        "status": status,
    }
    with open(f"{CUR_PATH}/out/log.json", "r+") as f:
        output = []
        fileData = json.loads(f.read())
        for entry in fileData:
            output.append(entry)
        output.append(currClassInfo)

        f.seek(0)
        json.dump(output, f)


def bringWindowToFocus(partial_window_name):
    def window_enum_handler(hwnd, resultList):
        if IsWindowVisible(hwnd) and GetWindowText(hwnd) != '':
            resultList.append((hwnd, GetWindowText(hwnd)))
    SystemParametersInfo(8193, 0, 2 | 1)
    handles = []
    EnumWindows(window_enum_handler, handles)
    for i in handles:
        if str(partial_window_name).upper() in str(i[1]).upper():
            ShowWindow(i[0], 3)
            SetForegroundWindow(i[0])
            return True
    return False
