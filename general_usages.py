from tkinter import *


value_message = "You typed letters or empty spaces in a textbox."


class WidgetStyling:
    def __init__(self):
        self.font = 'italic'
        self.button_background = 'orange'
        self.button_border = 0
        self.button_active = '#E8830C'
        self.frame_background = 'aliceblue'


styles = WidgetStyling()


def easy_grid(items, maxm, initialrow, initialcolumn):  # Function that easily grids widgets
    rowx = initialrow
    columnx = initialcolumn
    for item in items:
        item.grid(row=rowx, column=columnx, sticky=W, padx=5, pady=5)
        columnx += 1
        if columnx == maxm:
            columnx = 0
            rowx += 1
