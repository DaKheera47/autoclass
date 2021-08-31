from rich.console import Console
from rich.table import Table
import yaml
from rich import print
from rich.panel import Panel
import time
from rich.align import Align

# # to show preview of all classes to join
# with open("./config/classes.yaml", 'r') as stream:
#     try:
#         CLASS_INFO = yaml.safe_load(stream)
#     except yaml.YAMLError as exc:
#         print(exc)

# table = Table(title="Class List")

# table.add_column("Class Title", style="cyan", no_wrap=True)
# table.add_column("Code to join", justify="right", style="cyan")
# table.add_column("Time to Join", justify="right", style="green")

# for cls in list(CLASS_INFO.keys()):
#     table.add_row(cls, list(CLASS_INFO[cls].values())[1], list(CLASS_INFO[cls].values())[2])


# console = Console()
# print(Align(table, align="center"))
# console.print("DANGER!", style="bold red on white")

from rich import print
from rich.layout import Layout
from rich.text import Text
from rich.panel import Panel

layout = Layout()

layout.split_column(
    Layout(name="upper"),
    Layout(name="lower")
)
layout["lower"].split_row(
    Layout(name="left"),
    Layout(name="right"),
)

# to show preview of all classes to join
with open("./config/classes.yaml", 'r') as stream:
    try:
        CLASS_INFO = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

table = Table(title="Class List")

table.add_column("Title", style="cyan", no_wrap=True)
table.add_column("Code", justify="right", style="cyan")
table.add_column("Time", justify="right", style="green")

for cls in list(CLASS_INFO.keys()):
    table.add_row(cls, list(CLASS_INFO[cls].values())[
                  1], list(CLASS_INFO[cls].values())[2])


layout["lower"]["left"].update(
    Align(table, align="center", vertical="middle")
)

print(layout)
time.sleep(10)
