import pyautogui as pag
import time
import os
import yaml
import sys


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
#     print(r"""
#  ____        _    _       ____              _       ____ _                 _                           _
# |  _ \  __ _| | _( )___  |  _ \  __ _ _ __ | | __  / ___| | __ _ ___ ___  | |    __ _ _   _ _ __   ___| |__   ___ _ __
# | | | |/ _` | |/ /// __| | | | |/ _` | '_ \| |/ / | |   | |/ _` / __/ __| | |   / _` | | | | '_ \ / __| '_ \ / _ \ '__|
# | |_| | (_| |   <  \__ \ | |_| | (_| | | | |   <  | |___| | (_| \__ \__ \ | |__| (_| | |_| | | | | (__| | | |  __/ |
# |____/ \__,_|_|\_\ |___/ |____/ \__,_|_| |_|_|\_\  \____|_|\__,_|___/___/ |_____\__,_|\__,_|_| |_|\___|_| |_|\___|_|
# """)


def findImage(imageUrl, message, confidence):
    i = 1

    while True:
        time.sleep(1)
        try:
            joinMeetingX, joinMeetingY = pag.locateCenterOnScreen(
                imageUrl, confidence=confidence)
        except TypeError:
            print(f"{message} (attempts: {i})", end="\r")
            i += 1
            continue
        break

    clear()
    return (joinMeetingX, joinMeetingY)


def checkAbsence(imageUrl, message):
    i = 1

    while True:
        location = pag.locateOnScreen(imageUrl)

        if location == None:
            break
        else:
            print(
                f"{message} (attempts: {i})", end="\r")

        time.sleep(5)
        i += 1

    clear()


def enterTextInput(x, y, text, message):
    pag.click(x=x, y=y)
    pag.write(text)
    print(f"\n{message}")
    pag.press("enter")


def main(code, password):
    pag.PAUSE = 1
    globalConfidence = 0.8
    # start button
    pag.press("winleft")

    # launch zoom
    pag.write("zoom")
    pag.press("enter")

    # locate join button on zoom
    pag.click(findImage("joinUnsigned.png",
              "Join button not found... Searching again", globalConfidence))

    # enter code into meeting id field
    joinMeetingX, joinMeetingY = findImage(
        "joinMeeting.png", "Join Meeting button not found... Searching again", globalConfidence)
    enterTextInput(joinMeetingX, joinMeetingY + 60, code, "Code entered!")

    # enter password into password field
    enterPassX, enterPassY = findImage(
        "enterMeetingPw.png", "Enter Meeting Password text not found... Searching again", globalConfidence)
    enterTextInput(enterPassX, enterPassY + 60, password, "Password entered!")

    # locate join with computer audio button on zoom
    pag.click(findImage("joinWithComputerAudioBtn.png",
                        "Have not been accepted into class yet... trying again", globalConfidence))

    # force full screen zoom
    pag.hotkey("winleft", "up")


if __name__ == '__main__':
    with open("classes.yaml", 'r') as stream:
        try:
            CLASS_INFO = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


    print("Class to join, choose the number:")
    i = 1
    for cls in CLASS_INFO.items():
        print(f"[{i}] {cls[0]}")
        i += 1

    className = int(input(f">"))

    try:
        chosenClass = list(CLASS_INFO.items())[className - 1][1]
        print(list(CLASS_INFO.items())[className - 1][1])
    except:
        print("Invalid input")

    main(chosenClass["code"], chosenClass["password"])
