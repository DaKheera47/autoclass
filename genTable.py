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
import os
import cursor
cursor.hide()


def genTable():
    CUR_PATH = os.path.dirname(os.path.realpath(__file__))
    CURR_TIME = datetime.now().strftime("%H:%M")
    CURR_DATE = datetime.now().strftime("%d-%m-%Y")
    CURR_DAY = datetime.now().strftime("%A")
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

    def genClassList():
        table = Table(title="Class List", caption=Text.assemble(
            (f"{CURR_TIME} \n {CURR_DATE} - {CURR_DAY}", "bold green")))

        table.add_column("Title", justify="left", style="cyan", no_wrap=True)
        table.add_column("Code", justify="left", style="cyan")
        table.add_column("Time", justify="left", style="green")

        for cls in list(CLASS_INFO.keys()):
            code = list(CLASS_INFO[cls].values())[1]

            if CURR_DAY_NUM == 4:
                # friday timings
                time = list(CLASS_INFO[cls].values())[3]
            else:
                # any other day
                time = list(CLASS_INFO[cls].values())[2]

            if CURR_TIME > time:
                # if time has passed then yellow
                time = Text.assemble((f"{time}", "yellow"))
            else:
                # if time if yet to come then green
                time = Text.assemble((f"{time}", "green"))

            table.add_row(cls, code, time)

        return table

    def genConfig():
        if SETUP["requireConfirmation"]:
            confirmation = Text.assemble(("Enabled", "black on green"))
        else:
            confirmation = Text.assemble(("Disabled", "black on red"))

        table = Table()

        table.add_column("Description", justify="left",
                         style="cyan", no_wrap=True)
        table.add_column("Setting", justify="left")

        if SETUP["requireConfirmation"]:
            confirmation = Text.assemble(("Enabled", "black on green"))
        else:
            confirmation = Text.assemble(("Disabled", "black on red"))
        if SETUP["recordClasses"]:
            record = Text.assemble(("Enabled", "black on green"))
        else:
            record = Text.assemble(("Disabled", "black on red"))

        table.add_row(
            "Delay between actions", str(SETUP["delayBetweenActions"]))
        table.add_row(
            "Require confirmation before joining a class", confirmation)
        table.add_row(
            "Record classes with OBS Studio", record)

        return table

    # generating components to render
    classListTable = genClassList()
    madeByShaheer = Text.assemble(
        "Made By Shaheer ", ("Sarfaraz", "bold green"))
    instructionsMarkdown = """
#  Instructions
-   Download the .zip file given in the Github repository
-   Extract the files to any folder (always keep them in the same folder structure)
-   See available features in the `build` folder 
-   You may create a shortcut of any of these files
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
        Text.assemble(("BOOM ZOOM LAUNCHER", "bold green")),
        Text.assemble(("If You Snitch You A Bitch", "bold red")),
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
    if SETUP["requireConfirmation"]:
        confirmation = Text.assemble(("Enabled", "black on green"))
    else:
        confirmation = Text.assemble(("Disabled", "black on red"))

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
