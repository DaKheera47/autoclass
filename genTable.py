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
from helpers import loadFiles, getNextClass
import os
import cursor
cursor.hide()


def genTable():
    CUR_PATH = os.path.dirname(os.path.realpath(__file__))
    CURR_TIME = datetime.now().strftime("%H:%M")
    CURR_DATE = datetime.now().strftime("%d-%m-%Y")
    CURR_DAY = datetime.now().strftime("%A")
    CURR_DAY_NUM = datetime.today().weekday()
    SETUP, CLASS_INFO = loadFiles()

    def genClassList():
        try:
            nextClassName = getNextClass()
            nextClassTime = CLASS_INFO[getNextClass()]["time_weekday"]
            timeTillNextClass = str(datetime.strptime(
                nextClassTime, "%H:%M") - datetime.strptime(CURR_TIME, "%H:%M"))[:-3]

            tableContent = Text.assemble((
                f"Last Refreshed: {CURR_TIME} \n {CURR_DATE} - {CURR_DAY} \n Next class: {getNextClass()} in {timeTillNextClass}",
                "bold green"))
        except Exception as e:
            tableContent = Text.assemble((
                f"Last Refreshed: {CURR_TIME} \n {CURR_DATE} - {CURR_DAY} \n", "bold green"))

        table = Table(title="Class List", caption=tableContent)
        table.add_column("Title", justify="left", style="cyan", no_wrap=True)
        table.add_column("Code", justify="left", style="cyan")
        table.add_column("Join Time", justify="center", style="green")
        table.add_column("Leave Time", justify="center", style="green")
        table.add_column("Class Duration", justify="center", style="cyan")

        for cls in list(CLASS_INFO.keys()):
            code = str(CLASS_INFO[cls]["code"]).replace(" ", "")

            if CURR_DAY_NUM == 4:
                # friday timings
                timeOfJoining = str(CLASS_INFO[cls]["time_friday"])
                timeOfLeaving = str(CLASS_INFO[cls]["time_of_leaving_friday"])
            else:
                # any other day
                timeOfJoining = str(CLASS_INFO[cls]["time_weekday"])
                timeOfLeaving = str(CLASS_INFO[cls]["time_of_leaving_weekday"])

            # https://stackoverflow.com/questions/3096953/how-to-calculate-the-time-interval-between-two-time-strings
            duration = datetime.strptime(
                timeOfLeaving, "%H:%M") - datetime.strptime(timeOfJoining, "%H:%M")

            if CURR_TIME > timeOfJoining:
                # if time has passed then yellow
                timeOfJoining = Text.assemble((f"{timeOfJoining}", "yellow"))
            else:
                # if time if yet to come then green
                timeOfJoining = Text.assemble((f"{timeOfJoining}", "green"))

            if CURR_TIME > timeOfLeaving:
                # if time has passed then yellow
                timeOfLeaving = Text.assemble((f"{timeOfLeaving}", "yellow"))
            else:
                # if time if yet to come then green
                timeOfLeaving = Text.assemble((f"{timeOfLeaving}", "green"))

            table.add_row(cls, code, timeOfJoining,
                          timeOfLeaving, str(duration)[:-3])

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
    instructionsMarkdown = """
#  Instructions
-   Change the default class by opening and changing the `classes.yaml` in the `config` folder
-   Update the configuration by referring to the readme on the GitHub Page
"""

    # creating UI layout
    layout = Layout()
    layout.split_column(
        Layout(name="top", ratio=2),
        Layout(name="middle", ratio=2),
        Layout(name="bottom"),
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
    layout["bottom"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )

    # rendering components
    layout["top"].update(
        Align(classListTable, align="center", vertical="middle")
    )
    layout["middle"]["left"].update(
        Markdown(instructionsMarkdown)
    )

    layout["middle"]["right"].update(
        Padding(
            Group(
                Markdown("# Current Configuration"),
                genConfig()
            ), (0, 0, 0, 1))
    )
    layout["bottom"]["left"].update(
        Align(bottomLeftComponents, align="left", vertical="bottom")
    )
    layout["bottom"]["right"].update(
        Align(bottomRightComponents, align="right", vertical="bottom")
    )

    print(layout)
