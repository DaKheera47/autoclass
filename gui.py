# from rich import print
# import os
from helpers import loadFiles
# import tkinter as tk


SETUP, CLASS_INFO = loadFiles()
# window = tk.Tk()

data = list(CLASS_INFO.items())
# print(data)
# total_rows = len(data)
# total_columns = len(data[0][1].keys())
# print(total_columns)

# for i in range(total_rows):  # Rows
#     for j in range(total_columns):  # Columns
#         b = tk.Label(window, text=data[i][0])
#         b.grid(row=i, column=j)

# window.geometry("1000x500")
# window.mainloop()
from ttkwidgets import Table
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

style = ttk.Style(root)
style.theme_use('alt')
sortable = tk.BooleanVar(root, False)
drag_row = tk.BooleanVar(root, False)
drag_col = tk.BooleanVar(root, False)

columns = ["Class Title", "Class Code", "Class Password", "Class Joining Time", "Class Leaving Time", "Class Duration"]
table = Table(root, columns=columns, sortable=sortable.get(), drag_cols=drag_col.get(),
              drag_rows=drag_row.get(), height=6)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=100, stretch=False)

# for i in range(12):
#     table.insert('', 'end', iid=i,
#                  values=(i, i) + tuple(i + 10 * j for j in range(2, 7)))

for ind, cls in enumerate(CLASS_INFO):
    table.insert(f"{cls}", ind)


# add scrollbars
sx = tk.Scrollbar(root, orient='horizontal', command=table.xview)
sy = tk.Scrollbar(root, orient='vertical', command=table.yview)
table.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)

table.grid(sticky='ewns')
sx.grid(row=1, column=0, sticky='ew')
sy.grid(row=0, column=1, sticky='ns')
root.update_idletasks()


# toggle table properties
def toggle_sort():
    table.config(sortable=sortable.get())


def toggle_drag_col():
    table.config(drag_cols=drag_col.get())


def toggle_drag_row():
    table.config(drag_rows=drag_row.get())


frame = tk.Frame(root)
tk.Checkbutton(frame, text='sortable', variable=sortable, command=toggle_sort).pack(side='left')
tk.Checkbutton(frame, text='drag columns', variable=drag_col, command=toggle_drag_col).pack(side='left')
tk.Checkbutton(frame, text='drag rows', variable=drag_row, command=toggle_drag_row).pack(side='left')
frame.grid()
root.geometry('400x200')

root.mainloop()