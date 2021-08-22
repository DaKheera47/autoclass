import pyautogui as pag
import time
import yaml
from launcher import main as launcherMain
from launcher import clear
import schedule
from datetime import datetime
from termcolor import cprint
import cursor
import json
cursor.hide()

# TODO: make central object with all messages so rest of the code is cleaner
# TODO: add support for using flag when launching to have confirmation or not
# TODO: optimise logging by having className parent, and history for dates below
# eg: {
#     "Computer Science": {
#         "date": "2021-08-16",
#         "time": "08:00",
#         "status": "Success"
#     }
# }

# importing external files
with open("config.yaml", 'r') as stream:
    try:
        SETUP = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open("classes.yaml", 'r') as stream:
    try:
        CLASS_INFO = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


def getCodeAndPass(cls):
    # select code and password of that class
    code_to_use = str(CLASS_INFO[cls]["code"])
    password_to_use = str(CLASS_INFO[cls]["password"])
    return (code_to_use, password_to_use)


def main():
    clear()

    currTime = datetime.now().strftime("%H:%M")

    cprint(f"Time: {currTime}", "cyan", attrs=["bold"], end="\r")

    for cls in CLASS_INFO.items():
        if currTime == cls[1]["time_weekday"]:
            # Uncomment to add confirmation
            # isConfirmed = pag.confirm(
            #     text=f'Join {cls[0]} class?', title=f'Confirm joining of {cls[0]} class', buttons=['OK', 'Cancel'])

            # if isConfirmed == "OK":
            code_to_use, password_to_use = getCodeAndPass(cls[0])
            print(
                f"\nUsing {cls[0]} class information \n  Code: {code_to_use} \n  Pass: {password_to_use}")

            # sending the program into execution phase
            status = launcherMain(code_to_use, password_to_use)

            # logging classes entered
            currClassInfo = {
                "time": currTime,
                "className": cls[0],
                "date": datetime.today().strftime('%Y-%m-%d'),
                "status": status["message"],
            }
            with open("log.json", "r+") as f:
                output = []
                fileData = json.loads(f.read())
                for entry in fileData:
                    output.append(entry)
                output.append(currClassInfo)

                f.seek(0)
                json.dump(output, f)


schedule.every(15).seconds.do(main)

while True:
    schedule.run_pending()
    time.sleep(5)
