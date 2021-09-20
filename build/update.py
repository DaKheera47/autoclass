from datetime import datetime
import os
import yaml
from rich import print
import tempfile
CUR_PATH = os.path.dirname(os.path.realpath(__file__))


def loadFiles():
    CURR_DAY_NUM = datetime.today().weekday()
    # importing external files
    with open(f"./scheduled-class-launcher/config/config.yaml", 'r') as stream:
        try:
            SETUP = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(f"./scheduled-class-launcher/config/classes.yaml", 'r') as stream:
        try:
            CLASS_INFO = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return SETUP, CLASS_INFO


def loadFilesTemp():
    tempPath = tempfile.gettempdir()
    os.chdir(tempPath)

    CURR_DAY_NUM = datetime.today().weekday()
    # importing external files
    with open(f"./config/config.yaml", 'r') as stream:
        try:
            SETUP = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(f"./config/classes.yaml", 'r') as stream:
        try:
            CLASS_INFO = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return SETUP, CLASS_INFO


NEW_SETUP, NEW_CLASS_INFO = loadFiles()
LOCAL_SETUP, LOCAL_CLASS_INFO = loadFilesTemp()

temp = LOCAL_CLASS_INFO | NEW_CLASS_INFO
FOREIGN_CLASS_INFO = temp | LOCAL_CLASS_INFO


def writeToTemp():
    tempPath = tempfile.gettempdir()
    os.chdir(tempPath)

    with open("./config/classes.yaml", 'w') as outfile:
        yaml.dump(FOREIGN_CLASS_INFO, outfile, default_flow_style=False)


writeToTemp()

temp = LOCAL_SETUP | NEW_SETUP
FOREIGN_SETUP = temp | LOCAL_SETUP


def writeToTemp():
    tempPath = tempfile.gettempdir()
    os.chdir(tempPath)

    with open("./config/config.yaml", 'w') as outfile:
        yaml.dump(FOREIGN_SETUP, outfile, default_flow_style=False)


writeToTemp()
print(FOREIGN_CLASS_INFO)
print(FOREIGN_SETUP)
