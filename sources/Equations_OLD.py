from tkinter import *


def reset():  # A function to delete all of the widgets
    forgetwidgets("all")
    my_board.__init__()
    my_board.print_board()


def yesno():  # A function to pack yes/no buttons
    my_board.buttonyes.pack(side=LEFT)
    my_board.buttonno.pack(side=LEFT)


def none():  # The most useless function that has ever existed
    print("none")


def forgetwidgets(widgets):  # A function that eases the process of deleting widgets
    if widgets == "all":
        widgets = [my_board.question, my_board.buttonless, my_board.buttonmore, my_board.labelsy, my_board.buttonyes,
                   my_board.buttonno, my_board.compare, my_board.buttonreset, my_board.bottomframe, my_board.upperframe,
                   my_board.middleframe]
    for item in widgets:
        item.pack_forget()
    boardbuttons = [my_board.buttonless, my_board.buttonmore]
    for item in boardbuttons:
        item.bind("<Button-1>", none)


def sy():  # A function that asks the user if syc = syt
    forgetwidgets([my_board.compare, my_board.buttonmore, my_board.buttonless, my_board.question])
    my_board.labelsy.pack(side=LEFT)
    yesno()
    my_board.buttonyes.bind("<Button-1>", conservative2)
    my_board.buttonno.bind("<Button-1>", ductcolmohr)


def conservative():  # A function that asks the user if the element is conservative
    forgetwidgets([my_board.compare, my_board.buttonless, my_board.buttonmore])
    my_board.question["text"] = "Conservative?"
    yesno()
    my_board.buttonyes.bind("<Button-1>", britcolmohr)
    my_board.buttonno.bind("<Button-1>", britcolmohr)


def conservative2(event):  # A function that asks the user if the element is conservative (to avoid bugs)
    forgetwidgets([my_board.compare, my_board.buttonless, my_board.buttonmore])
    my_board.labelsy["text"] = "Conservative?"
    yesno()
    my_board.buttonyes.bind("<Button-1>", maxshear)
    my_board.buttonno.bind("<Button-1>", distenergy)


def check(first, second, labelstatus, condition):
    if first > second:
        labelstatus["text"] = "Status: Ok, " + condition + " satisfied"
        labelstatus["bg"] = "green"
        labelstatus.grid(column=0, row=6, sticky=W)
    else:
        labelstatus["text"] = "Status: Not Ok, " + condition + " not satisfied"
        labelstatus["bg"] = "red"
        labelstatus.grid(column=0, row=6, sticky=W)


def britcolmohr(event):  # The main function responsible for Mohr equation for Brittle elements.
    forgetwidgets("all")
    ductilepacks("britmoh")


def ductcolmohr(event):  # The main function responsible for Mohr equation for Ductile elements.
    forgetwidgets("all")
    ductilepacks("ductmoh")


def distenergy(event):  # The main function responsible for the distortion-energy equation.
    forgetwidgets("all")
    ductilepacks("dist")


def maxshear(event):  # The main function responsible for the maximum shear stress equation
    forgetwidgets("all")
    ductilepacks("max")


def calculatemax(s1, s_y, s3, sy, labelstatus, tmax, t45, n):  # Calculates the maximum shear stress
    tmax["text"] = "T(max ,act)= " + str((s1-s3)/2)
    t45["text"] = "T(45)= " + str(s_y/2)
    tmax.grid(column=0, row=7, sticky=W)
    t45.grid(column=0, row=8, sticky=W)
    check((s1-s3)/2, sy/n, labelstatus, "(σmax) < Sy/n")


def calculatedist(s1, s2, s3, tresult):  # Calculates the distortion energy
    tresult["text"] = "σ' = " + str((((s1-s2)**2+(s2-s3)**2+(s3-s1)**2)/2)**1/2)
    tresult.grid(column=0, row=4)


def duccalculatemoh(syt, syc, tresult):  # Uses Mohr equation for ductile elements
    tresult["text"] = "S(sy) = " + str((syt*syc)/(syt+syc))
    tresult.grid(column=0, row=4)


def britcalculatemohr(suc, n, tresult):  # Uses Mohr equation for brittle elements
    tresult["text"] = "σ(B) = " + str((-suc)/n)
    tresult.grid(column=0, row=4)


def ductilepacks(string):  # Prepares to receive the inputs
    labels1 = Label(window, text="Enter σ1: ", font=("courrier", 24))
    labels2 = Label(window, text="Enter σy: ", font=("courrier", 24))
    labels3 = Label(window, text="Enter σ3: ", font=("courrier", 24))
    tresult = Label(window, text="", font=("courrier", 24))
    entrys1 = Entry(window)
    entrys2 = Entry(window)
    entrys3 = Entry(window)

    labels1.grid(column=0, row=0, sticky=W)
    labels2.grid(column=0, row=1, sticky=W)
    labels3.grid(column=0, row=2, sticky=W)
    entrys1.grid(column=1, row=0)
    entrys2.grid(column=1, row=1)
    entrys3.grid(column=1, row=2)

    if string == "max":
        labels1["text"] = "Normal stress (σx)"
        labels2["text"] = "Normal stress (σy)"
        labels3["text"] = "Shear stress (τxy) "
        buttoncalc = Button(window, text="Calculate", font=("courrier", 24),
                            command=lambda: calculatemax(float(entrys1.get()),
                                                              float(entrys2.get()), tresult))

    elif string == "dist":
        buttoncalc = Button(window, text="Calculate", font=("courrier", 24),
                            command=lambda: calculatedist(float(entrys1.get()),
                                                          float(entrys2.get()), float(entrys3.get()), tresult))
        labels2["text"] = "Enter σ2: "
    elif string == "ductmoh":
        buttoncalc = Button(window, text="Calculate", font=("courrier", 24),
                            command=lambda: duccalculatemoh(float(entrys1.get()),
                                                            float(entrys2.get()), tresult))
        labels1["text"] = "Enter S(yt): "
        labels2["text"] = "Enter S(yc): "
        labels3.grid_forget()
        entrys3.grid_forget()
    else:
        buttoncalc = Button(window, text="Calculate", font=("courrier", 24),
                            command=lambda: britcalculatemohr(float(entrys1.get()),
                                                              float(entrys2.get()), tresult))
        labels1["text"] = "Enter S(uc): "
        labels2["text"] = "Enter n: "
        labels3.grid_forget()
        entrys3.grid_forget()

    buttoncalc.grid(column=0, columnspan=2, row=5)


window = Tk()
window.title("Failure theories")


class Board(object):
    def __init__(self):  # Defines the widgets
        self.middleframe = Frame(window)
        self.upperframe = Frame(window)
        self.bottomframe = Frame(window)
        self.question = Label(self.middleframe, text="εf", font=("courrier", 24))
        self.buttonless = Button(self.middleframe, text="<", height=5, width=7, command=lambda: conservative())
        self.buttonmore = Button(self.middleframe, text="≥", height=5, width=7, command=lambda: sy())
        self.buttonyes = Button(self.middleframe, text="Yes", height=5, width=7)
        self.buttonno = Button(self.middleframe, text="No", height=5, width=7)
        self.buttonreset = Button(self.bottomframe, text="Reset", command=lambda: reset())
        self.compare = Label(self.middleframe, text="0.05", font=("courrier", 24))
        self.labelsy = Label(self.middleframe, text="Syt = Syc?", font=("courrier", 24))

    def print_board(self):  # Prints the widgets
        self.upperframe.pack(side=TOP)
        self.middleframe.pack(side=TOP)
        self.bottomframe.pack(side=TOP, expand=True, fill=BOTH)
        self.question.pack(side=LEFT)
        self.buttonless.pack(side=LEFT)
        self.buttonmore.pack(side=LEFT)
        self.compare.pack(side=LEFT)
        self.buttonreset.pack(side=BOTTOM, expand=True, fill=BOTH)


my_board = Board()
my_board.__init__()
my_board.print_board()
window.mainloop()
