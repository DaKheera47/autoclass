from genTable import genTable
import os
import time
import pyautogui as pag

CUR_PATH = os.path.dirname(os.path.realpath(__file__))


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    genTable()


def findImage(imageUrl: str, message: str, confidence: int = 0.98):
    try:
        x, y = pag.locateCenterOnScreen(
            f"{CUR_PATH}/static/{imageUrl}", confidence=confidence)
        return (x, y)
    except TypeError:
        return (-1, -1)

    # clear()


def enterTextInput(x: int, y: int, text: str, message: str):
    pag.click(x=x, y=y)
    pag.write(text)
    print(f"\n{message}")
    pag.press("enter")


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
                    pag.write(textToInput)
                    pag.press("enter")
                    return {"error": False, "message": None}
            i += 1
        else:
            return {"error": True, "message": f"Timed Out: {errorMessage}"}