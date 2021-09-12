from genTable import genTable
import os
import time
import pyautogui as pag
import json
import yaml

CUR_PATH = os.path.dirname(os.path.realpath(__file__))


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    genTable()


def findImage(imageUrl: str, message: str, confidence: int = 0.90):
    try:
        x, y = pag.locateCenterOnScreen(
            f"{CUR_PATH}/static/{imageUrl}", confidence=confidence)
        return (x, y)
    except TypeError:
        return (-1, -1)


def enterTextInput(x: int, y: int, text: str, message: str):
    pag.click(x=x, y=y)
    pag.write(text.replace(" ", ""))
    print(f"\n{message}")
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


def findAndClick(imageUrls: list, searchingText: str, errorMessage: str, timeout: int = 60 * 10):
    output = {}
    i = 1

    while True:
        if i <= timeout:
            for imageUrl in imageUrls:
                print(f"Searching for {imageUrl}")
                x, y = findImage(imageUrl, searchingText)
                if x != -1 and y != -1:
                    pag.click(x, y)
                    return {"error": False, "message": None}
                    break
            i += 1
        else:
            return {"error": True, "message": f"Timed Out: {errorMessage}"}
            break


def findAndInputText(imageUrls: list, searchingText: str, errorMessage: str, textToInput: str, timeout: int = 60 * 10):
    output = {}
    i = 1

    while True:
        if i <= timeout:
            for imageUrl in imageUrls:
                print(f"Searching for {imageUrl}")
                x, y = findImage(imageUrl, searchingText)
                if x != -1 and y != -1:
                    pag.click(x, y + 60)
                    pag.write(textToInput.replace(" ", ""))
                    pag.press("enter")
                    return {"error": False, "message": None}
            i += 1
        else:
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


def getYamlFiles():
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

    return SETUP, CLASS_INFO
