from rich.table import Table
import yaml
from rich import print, box
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
from pyfiglet import Figlet
import os
import cursor
cursor.hide()

leftMdx = """##  Instructions
-   Change the default class by opening and changing the classes.yaml in the config folder
-   Update the configuration by referring to the readme on the GitHub Page"""

tableBoxLook = box.MINIMAL


def genTable(CLASS_INFO: list, leftMdx: str = leftMdx, footer: bool = True, tagline: str = ""):
    CUR_PATH = os.path.dirname(os.path.realpath(__file__))
    CURR_TIME = datetime.now().strftime("%H:%M")
    DATE_STRING = datetime.now().strftime("%H:%M - %d/%m/%y - %A")
    DATE = datetime.now().strftime("%d/%m/%y")
    DAY = datetime.now().strftime("%A")
    CURR_DAY_NUM = datetime.today().weekday()
    SETUP, _, COLORS = loadFiles()

    def genClassList():
        table = Table(style=COLORS["text-color"], box=tableBoxLook)
        table.add_column("#", justify="center",
                         style=COLORS["text-color"], no_wrap=True)
        table.add_column("Title", justify="center",
                         style=COLORS["text-color"], no_wrap=True)
        table.add_column("Code", justify="center",
                         style=COLORS["text-color"])
        table.add_column("Password", justify="center",
                         style=COLORS["text-color"])
        table.add_column("Join Time", justify="center",
                         style=COLORS["text-color"])
        table.add_column("Leave Time", justify="center",
                         style=COLORS["text-color"])
        table.add_column("Duration", justify="center",
                         style=COLORS["text-color"])

        for index, clsName in enumerate(CLASS_INFO, start=1):
            code = clsName["meeting id"]
            password = clsName["meeting password"]
            timeJoining = clsName["join time"]
            timeLeaving = clsName["leave time"]
            durationOfClass = clsName["duration"]

            # adding colors
            color = COLORS["past"] if CURR_TIME > timeJoining else COLORS["future"]
            coloredTimeJoining = Text.assemble((f"{timeJoining}", color))

            # adding colors
            color = COLORS["future"] if CURR_TIME < timeLeaving else COLORS["past"]
            coloredTimeLeaving = Text.assemble((f"{timeLeaving}", color))

            table.add_row(str(index), clsName["class"], code, password, coloredTimeJoining,
                          coloredTimeLeaving, durationOfClass)

        return table

    def genTimeData():
        table = Table(box=tableBoxLook, expand=True)
        table.add_column("Description", justify="left",
                         style=COLORS["text-color"], no_wrap=True)
        table.add_column("Setting", justify="left",
                         style=COLORS["text-color"])

        if tagline != "":
            rowText = "Choose"
            tableContent = Text.assemble((f"{tagline}", COLORS["highlight"]))
        else:
            try:
                data = getNextClass()
                nextclsName = data["class"]
                event = data["event"]
                timeTillNextEvent = data["timeTillNextEvent"]
                rowText = "Next Event"
                tableContent = Text.assemble(
                    (f"{event} {nextclsName} in {timeTillNextEvent}", COLORS["highlight"]))

            except Exception as e:
                rowText = "Status"
                tableContent = Text.assemble(f"Done with classes for today :)")

        table.add_row("Time", CURR_TIME)
        table.add_row("Date", DATE)
        table.add_row("Day", DAY)
        table.add_row(rowText, tableContent)

        return table

    def genConfig():
        table = Table(box=tableBoxLook, expand=True)
        table.add_column("Description", justify="left",
                         style=COLORS["text-color"], no_wrap=True)
        table.add_column("Setting", justify="left",
                         style=COLORS["text-color"])

        for option in SETUP:
            value = Text.assemble((str(option["value"]), COLORS["text-color"]))

            if option["value"] == True:
                value = Text.assemble(
                    (str(option["value"]), COLORS["enabled"]))
            elif option["value"] == False:
                value = Text.assemble(
                    (str(option["value"]), COLORS["disabled"]))

            table.add_row(option["description"], value)

        return table

    # generating components to render
    classListTable = genClassList()
    madeByShaheer = Text.assemble(
        "Made By Shaheer ", ("Sarfaraz", COLORS["highlight"]))

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
        Text.assemble("Made By Shaheer ", ("Sarfaraz", COLORS["highlight"])),
    )
    bottomMidComponents = Group(
        Text.assemble(("Snitches Get Stitches", COLORS["highlight"])),
    )
    bottomLeftComponents = Group(
        Text.assemble(("AutoClass")),
    )
    layout["middle"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )

    if footer:
        layout["bottom"].split_row(
            Layout(name="left"),
            Layout(name="mid"),
            Layout(name="right"),
        )

    # rendering components
    if CLASS_INFO:
        layout["top"].update(
            Group(
                Align(classListTable, align="center", vertical="middle")
            )
        )
    elif tagline:
        figRenderer = Figlet(font="smslant", width=110)
        renderText = Text.assemble(
            (f"{figRenderer.renderText(f'{tagline}')}", "green"))

        layout["top"].update(
            Group(Align(renderText, align="center", vertical="middle")))
    elif not CLASS_INFO:
        figRenderer = Figlet(font="smslant", width=110)
        renderText = Text.assemble((f"{figRenderer.renderText('Done with Classes')}", "green"))
        layout["top"].update(
            Group(Align(renderText, align="center", vertical="middle")))

    layout["middle"]["left"].update(
        Padding(
            Group(
                Align(Text.assemble(("Date & Time",
                                     "white bold underline")), align="center"),
                genTimeData()
            ), style=COLORS["text-color"]
        )
    )
    layout["middle"]["right"].update(
        Padding(
            Group(
                Align(Text.assemble(("Current Configuration",
                      "white bold underline")), align="center"),
                genConfig()
            ), (0, 0, 0, 1), style=COLORS["text-color"])
    )
    if footer:
        layout["bottom"]["left"].update(
            Align(bottomLeftComponents, align="left", vertical="bottom")
        )
        layout["bottom"]["mid"].update(
            Align(bottomMidComponents, align="center", vertical="bottom")
        )
        layout["bottom"]["right"].update(
            Align(bottomRightComponents, align="right", vertical="bottom")
        )

    clear()
    print(layout)
