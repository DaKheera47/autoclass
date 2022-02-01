from rich.table import Table
import yaml
from rich import print
from rich.panel import Panel
import time
from rich.align import Align
from rich.layout import Layout
from rich.text import Text
from rich.console import Group
from rich.console import Console
from rich.markdown import Markdown
from rich.padding import Padding
from datetime import datetime
from helpers import loadFiles, getNextClass, clear
import os
import cursor
cursor.hide()

leftMdx = """#  Instructions
-   Change the default class by opening and changing the `classes.yaml` in the `config` folder
-   Update the configuration by referring to the readme on the GitHub Page"""

def genTable(CLASS_INFO, leftMdx=leftMdx, footer=True):
    CUR_PATH = os.path.dirname(os.path.realpath(__file__))
    CURR_TIME = datetime.now().strftime("%H:%M")
    DATE_STRING = datetime.now().strftime("%H:%M - %D - %A")
    CURR_DAY_NUM = datetime.today().weekday()
    SETUP, _ = loadFiles()

    def genClassList():
        try:
            nextclsName = getNextClass()
            if CURR_DAY_NUM in range(0, 4):
                nextClassTime = CLASS_INFO[getNextClass()]["time_weekday"]
            elif CURR_DAY_NUM == 4:
                nextClassTime = CLASS_INFO[getNextClass()]["time_friday"]

            timeTillNextClass = str(datetime.strptime(
                nextClassTime, "%H:%M") - datetime.strptime(CURR_TIME, "%H:%M"))[:-3]

            tableContent = Text.assemble((
                f"{DATE_STRING} \n Next class: {getNextClass()} in {timeTillNextClass}",
                "bold green"))
        except Exception as e:
            tableContent = Text.assemble((
                f"{DATE_STRING} \n Done with classes for today :)", "bold green"))

        table = Table(title="Class List", caption=tableContent)
        table.add_column("#", justify="center", style="cyan", no_wrap=True)
        table.add_column("Title", justify="center", style="cyan", no_wrap=True)
        table.add_column("Code", justify="center", style="cyan")
        table.add_column("Password", justify="center", style="cyan")
        table.add_column("Join Time", justify="center", style="green")
        table.add_column("Leave Time", justify="center", style="green")
        table.add_column("Duration", justify="center", style="cyan")

        for index, clsName in enumerate(list(CLASS_INFO.keys()), start=1):
            code = str(CLASS_INFO[clsName]["code"]).replace(" ", "")
            password = str(CLASS_INFO[clsName]["password"]).replace(" ", "")

            timeJoining = datetime.strptime(
                CLASS_INFO[clsName]["time_friday" if CURR_DAY_NUM == 4 else "time_weekday"],
                "%H:%M"
            )
            timeLeaving = datetime.strptime(
                CLASS_INFO[clsName]["time_of_leaving_friday" if CURR_DAY_NUM == 4 else "time_of_leaving_weekday"],
                "%H:%M"
            )

            # https://stackoverflow.com/questions/3096953/how-to-calculate-the-time-interval-between-two-time-strings
            durationOfClass = timeLeaving - timeJoining
            coloredTimeJoining = Text.assemble(
                (f"{timeJoining.strftime('%H:%M')}",
                 "green" if CURR_TIME > str(timeJoining) else "yellow")
            )
            coloredTimeLeaving = Text.assemble(
                (f"{timeLeaving.strftime('%H:%M')}",
                 "green" if CURR_TIME > str(timeLeaving) else "yellow")
            )

            table.add_row(str(index), clsName, code, password, coloredTimeJoining,
                          coloredTimeLeaving, str(durationOfClass)[:-3]
                          )

        return table

    def genConfig():
        if SETUP["requireConfirmationBeforeJoining"]:
            joinConfirmation = Text.assemble(("Enabled", "black on green"))
        else:
            joinConfirmation = Text.assemble(("Disabled", "black on red"))
        if SETUP["requireConfirmationBeforeLeaving"]:
            leaveConfirmation = Text.assemble(("Enabled", "black on green"))
        else:
            leaveConfirmation = Text.assemble(("Disabled", "black on red"))

        table = Table()
        table.add_column("Description", justify="left",
                         style="cyan", no_wrap=True)
        table.add_column("Setting", justify="left")

        table.add_row(
            "Delay between every action taken", f"{SETUP['delayBetweenActions']}s")
        table.add_row(
            "Percent of image to match", f"{SETUP['globalConfidence'] * 100}%")
        table.add_row(
            "Require confirmation before joining a class", joinConfirmation)
        table.add_row(
            "Require confirmation before leaving a class", leaveConfirmation)

        return table

    # generating components to render
    classListTable = genClassList()
    madeByShaheer = Text.assemble(
        "Made By Shaheer ", ("Sarfaraz", "bold green"))

    # creating UI layout
    layout = Layout()
    if footer:
        layout.split_column(
            Layout(name="top", ratio=2),
            Layout(name="middle", ratio=2),
            Layout(name="bottom"),
        )
    else:
        layout.split_column(
            Layout(name="top", ratio=2),
            Layout(name="middle", ratio=2),
        )
    bottomRightComponents = Group(
        Text.assemble("Made By Shaheer ", ("Sarfaraz", "bold green")),
    )
    bottomLeftComponents = Group(
        Text.assemble(("AutoClass", "bold green")),
    )
    layout["middle"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )

    if footer:
        layout["bottom"].split_row(
            Layout(name="left"),
            Layout(name="right"),
        )

    # rendering components
    layout["top"].update(
        Align(classListTable, align="center", vertical="middle")
    )
    layout["middle"]["left"].update(
        Markdown(leftMdx)
    )

    layout["middle"]["right"].update(
        Padding(
            Group(
                Markdown("# Current Configuration"),
                genConfig()
            ), (0, 0, 0, 1))
    )
    if footer:
        layout["bottom"]["left"].update(
            Align(bottomLeftComponents, align="left", vertical="bottom")
        )
        layout["bottom"]["right"].update(
            Align(bottomRightComponents, align="right", vertical="bottom")
        )

    clear()
    print(layout)
