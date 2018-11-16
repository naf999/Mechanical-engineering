from general_usages import *
from tkinter import *
from math import *
from tkinter import messagebox


class modified:
    def __init__(self,theory):
        self.window = Toplevel()
        self.window.title("")

        self.mohrcanvas = Canvas(self.window, bg=styles.frame_background, height=800, width=1100)
        self.scrollbar = Scrollbar(self.window, command=self.mohrcanvas.yview)
        self.mohrcanvas.config(yscrollcommand=self.scrollbar.set)
        self.mohrframe = Frame(self.mohrcanvas, bg=styles.frame_background, height=1300)
        self.mohrcanvas.create_window((0, 0), window=self.mohrframe, anchor=NW)
        self.mohrcanvas.config(scrollregion=self.mohrcanvas.bbox("all"))
##        self.labelgiven = Label(self.mohrframe, bg=styles.frame_background, text='Given', font=(styles.font, 30))
##        self.givenvar = StringVar(self.mohrframe)
##        self.givens = ['Sut, Suc, Stress X, Stress Y',
##                       'Sut, Suc, Stress X, Stress Y, Shear stress',
##                       'Sut, Suc, Stress Y, Shear stress, Safety Factor',
##                       'Sut, Suc, Stress X, Shear stress, Safety Factor', 'Sut, Suc, Stress Y, Safety Factor',
##                       'Sut, Suc, Stress X, Safety Factor']
##        self.index = 0
##        self.givenvar.set(self.givens[0])
##        self.givenmenu = OptionMenu(self.mohrframe, self.givenvar, *self.givens)
        self.labelz = Label(self.mohrframe, bg=styles.frame_background, text='factor of safety(n):',
                            font=(styles.font, 30))
        self.labelsut = Label(self.mohrframe, bg=styles.frame_background, text='Syt (kpsi):', font=(styles.font, 30))
        self.labelsuc = Label(self.mohrframe, bg=styles.frame_background, text='Syc (kpsi):', font=(styles.font, 30))
        self.labelx = Label(self.mohrframe, bg=styles.frame_background, text='non-zero principle stress A(kpsi):',
                            font=(styles.font, 30))
        self.labely = Label(self.mohrframe, bg=styles.frame_background, text='non-zero principle stress B(kpsi):',
                            font=(styles.font, 30))
        self.buttoncalc = Button(self.mohrframe, text="Calculate", font=(styles.font, 24), bg=styles.button_background,
                                 bd=styles.button_border, activebackground=styles.button_active,
                                 command=lambda: self.calc())
        
        self.entryz = Entry(self.mohrframe)

        self.entrysut = Entry(self.mohrframe)
        self.entrysuc = Entry(self.mohrframe)
        self.entryx = Entry(self.mohrframe)
        self.entryy = Entry(self.mohrframe)
        self.entryss = Entry(self.mohrframe)
        self.entryn = Entry(self.mohrframe)

        self.lblcalc = Label(self.mohrframe, bg=styles.frame_background, font=(styles.font, 30))
        self.lblresult = Label(self.mohrframe, bg=styles.frame_background, font=(styles.font, 30), justify=LEFT)
        self.lblstatus = Label(self.mohrframe, bg=styles.frame_background, font=(styles.font, 30))

        self.mohrcanvas.pack(side=LEFT)
        self.scrollbar.pack(side=LEFT, fill=Y)
        if theory == 'mohr':
            #self.givenvar.trace('w', lambda *args: self.tracer())
            #self.entryn['state'] = 'readonly'
            #self.entryss['state'] = 'readonly'
            self.formula_ductile = PhotoImage(file='images/ductile.gif')
            self.formula_brittle = PhotoImage(file='images/brittle.gif')
            self.formula_mohr = PhotoImage(file='images/mohr.gif')
            self.lblcalc['image'] = self.formula_ductile
        self.lblcalc.grid(sticky=W, padx=5)
        items = [self.labelz,self.entryz,self.labelsut,self.entrysut,
                 self.labelsuc, self.entrysuc, self.labelx, self.entryx, self.labely,
                 self.entryy, self.buttoncalc]
        easy_grid(items, 2, 1, 0)
        for item in [self.lblresult, self.lblstatus]:
            item.grid(sticky=W, padx=5)
    def calc(self):
        self.labelabc = Label(self.mohrframe, bg=styles.frame_background, text='Safety Factor: 1.60',
                        font=(styles.font, 30))
        items = [self.labelz,self.entryz,self.labelsut,self.entrysut,
                 self.labelsuc, self.entrysuc, self.labelx, self.entryx, self.labely,
                 self.entryy, self.buttoncalc, self.labelabc]
        easy_grid(items, 2, 1, 0)
                
    
class Mohr:
    def __init__(self, theory):
        self.window = Toplevel()
        self.window.title("Ductile Coulomb Mohr")
        self.mohrcanvas = Canvas(self.window, bg=styles.frame_background, height=800, width=1100)
        self.scrollbar = Scrollbar(self.window, command=self.mohrcanvas.yview)
        self.mohrcanvas.config(yscrollcommand=self.scrollbar.set)
        self.mohrframe = Frame(self.mohrcanvas, bg=styles.frame_background, height=1300)
        self.mohrcanvas.create_window((0, 0), window=self.mohrframe, anchor=NW)
        self.mohrcanvas.config(scrollregion=self.mohrcanvas.bbox("all"))
        self.labelgiven = Label(self.mohrframe, bg=styles.frame_background, text='Given', font=(styles.font, 30))
        self.givenvar = StringVar(self.mohrframe)
        self.givens = ['Sut, Suc, Stress X, Stress Y',
                       'Sut, Suc, Stress X, Stress Y, Shear stress',
                       'Sut, Suc, Stress Y, Shear stress, Safety Factor',
                       'Sut, Suc, Stress X, Shear stress, Safety Factor', 'Sut, Suc, Stress Y, Safety Factor',
                       'Sut, Suc, Stress X, Safety Factor']
        self.index = 0
        self.givenvar.set(self.givens[0])
        self.givenmenu = OptionMenu(self.mohrframe, self.givenvar, *self.givens)
        self.labelsut = Label(self.mohrframe, bg=styles.frame_background, text='Syt (kpsi):', font=(styles.font, 30))
        self.labelsuc = Label(self.mohrframe, bg=styles.frame_background, text='Syc (kpsi):', font=(styles.font, 30))
        self.labelx = Label(self.mohrframe, bg=styles.frame_background, text='Stress x σx(kpsi):',
                            font=(styles.font, 30))
        self.labely = Label(self.mohrframe, bg=styles.frame_background, text='Stress y σy(kpsi):',
                            font=(styles.font, 30))
        self.labelss = Label(self.mohrframe, bg=styles.frame_background, text='Shear stress τxy(kpsi):',
                             font=(styles.font, 30))
        self.labeln = Label(self.mohrframe, bg=styles.frame_background, text='Safety factor:', font=(styles.font, 30))
        self.buttoncalc = Button(self.mohrframe, text="Calculate", font=(styles.font, 24), bg=styles.button_background,
                                 bd=styles.button_border, activebackground=styles.button_active,
                                 command=lambda: self.calculate_initializer())

        self.entrysut = Entry(self.mohrframe)
        self.entrysuc = Entry(self.mohrframe)
        self.entryx = Entry(self.mohrframe)
        self.entryy = Entry(self.mohrframe)
        self.entryss = Entry(self.mohrframe)
        self.entryn = Entry(self.mohrframe)

        self.lblcalc = Label(self.mohrframe, bg=styles.frame_background, font=(styles.font, 30))
        self.lblresult = Label(self.mohrframe, bg=styles.frame_background, font=(styles.font, 30), justify=LEFT)
        self.lblstatus = Label(self.mohrframe, bg=styles.frame_background, font=(styles.font, 30))

        self.mohrcanvas.pack(side=LEFT)
        self.scrollbar.pack(side=LEFT, fill=Y)
        if theory == 'mohr':
            self.givenvar.trace('w', lambda *args: self.tracer())
            self.entryn['state'] = 'readonly'
            self.entryss['state'] = 'readonly'
            self.formula_ductile = PhotoImage(file='images/ductile.gif')
            self.formula_brittle = PhotoImage(file='images/brittle.gif')
            self.lblcalc['image'] = self.formula_ductile
        self.lblcalc.grid(sticky=W, padx=5)
        items = [self.labelgiven, self.givenmenu, self.labelsut,
                 self.entrysut, self.labelsuc, self.entrysuc, self.labelx, self.entryx, self.labely,
                 self.entryy, self.labelss, self.entryss, self.labeln, self.entryn, self.buttoncalc]
        easy_grid(items, 2, 1, 0)
        for item in [self.lblresult, self.lblstatus]:
            item.grid(sticky=W, padx=5)

    def tracer(self):
        labelenable = {0: [self.entryn, self.entryss],
                       1: [self.entryn],
                       2: [self.entryx],
                       3: [self.entryy],
                       4: [self.entryx, self.entryss],
                       5: [self.entryy, self.entryss]}
        self.index = self.givens.index(self.givenvar.get())
        for item in labelenable[self.index]:
            item['state'] = 'readonly'
        for item in [self.labelx, self.labeln, self.labelss, self.labelsuc, self.labely,
                     self.entryx, self.entryn, self.entryss, self.entrysuc, self.entryy]:
            if item not in labelenable[self.index]:
                item['state'] = 'normal'

    def calculate_initializer(self):
        try:
            sut = self.entrysut.get()
            suc = self.entrysuc.get()

            if self.index == 0 or self.index == 1:  # Safety factor is required
                stressx = float(self.entryx.get())
                stressy = float(self.entryy.get())
                if self.index == 0:
                    stressa = max((stressx, stressy))
                    stressb = min((stressx, stressy))
                else:  # If shear stress exists
                    ss = float(self.entryss.get())
                    stressa = ((stressx + stressy) / 2) + sqrt(pow(((stressx - stressy) / 2), 2) + pow(ss, 2))
                    stressb = ((stressx + stressy) / 2) - sqrt(pow(((stressx - stressy) / 2), 2) + pow(ss, 2))
                self.calculate_safety(stressa, stressb, sut, suc)
            # else:
            #     n = 0
            #     equation = 'Not available for now'
            #     status = 'To be added'
            #     # TODO: Continue
        except ValueError:
            messagebox.showerror("Error", value_message)

    def calculate_safety(self, stressa, stressb, sut, suc):
        try:
            # if stressA and stress B are positive then sut/stressA
            # if stressA is positive and stress B is negative then (StressA/sut - StressB/suc)^-1
            # If they are all negative then -suc/stressB
            if stressa >= stressb >= 0:
                n = float(sut) / stressa
                equation = str(float(sut)) + '/' + str(stressa)
                if stressa >= float(sut):
                    status = 'Fail'
                else:
                    status = 'Success'
            elif stressa >= 0 >= stressb:
                div = stressa / float(sut) - stressb / float(suc)
                n = 1 / div
                equation = '(' + str(stressa) + '/' + str(float(sut)) + '-' + \
                           '(' + str(stressb) + ')' + '/' + str(float(suc)) + ')' + '^-1'
                if div >= 1:
                    status = 'Fail'
                else:
                    status = 'Success'
            else:
                n = -float(suc) / stressb
                equation = str(-float(suc)) + '/' + str(stressb)
                if stressb <= -float(suc):
                    status = 'Fail'
                else:
                    status = 'Success'
            self.entryn['state'] = 'normal'
            self.entryn.delete(0, END)
            self.entryn.insert(0, str(n))
            self.entryn['state'] = 'readonly'
            self.result_printer(equation, status, n)
        except ValueError:
            messagebox.showerror("Error", value_message)

    def result_printer(self, equation, status, n):
        self.lblcalc["text"] = "Equation: " + equation
        self.lblresult["text"] = "Result: " + str(n) + ' Ans'
        self.lblstatus["text"] = 'Status: ' + status
        self.success_color()

    def success_color(self):
        if "Success" in self.lblstatus["text"]:
            self.lblstatus['bg'] = 'green'
        else:
            self.lblstatus['bg'] = 'red'

    @staticmethod
    def zero_setter(entry):
        if entry.get() == '':
            return 0
        else:
            return float(entry.get())


class MaxStress:
    def __init__(self):
        self.my_mss = Mohr('mss')
        self.my_mss.window.title("Maximum Shear Stress")
        for item in [self.my_mss.labelsut,
                     self.my_mss.entrysut,
                     self.my_mss.givenmenu, self.my_mss.labelgiven]:
            item.grid_forget()
        self.my_mss.labelsuc["text"] = "Yield Strength Sy(kpsi):"
        self.maximum_equation = PhotoImage(file="images/mss.gif")
        self.angle_equation = PhotoImage(file="images/mssangle.gif")
        self.my_mss.lblcalc["image"] = self.maximum_equation
        self.label_angle_calc = Label(self.my_mss.mohrframe, bg=styles.frame_background, image=self.angle_equation)
        self.label_angle_calc.grid(row=self.my_mss.lblcalc.grid_info()['row'] + 1, sticky=W, padx=5)
        self.label_explanation = Label(self.my_mss.mohrframe, bg=styles.frame_background,
                                       text="σx: Normal stress in X direction\nσy: Normal stress in Y direction\n" +
                                            "τxy: Shear stress perpendicular to X axis and in Y direction.",
                                       justify=LEFT,
                                       font=(styles.font, 23))
        self.label_explanation.grid(row=self.my_mss.lblcalc.grid_info()['row'] + 2, padx=5)
        self.my_mss.buttoncalc['command'] = lambda: self.calculate()

    def calculate(self):
        try:
            stressx = float(self.my_mss.entryx.get())
            stressy = float(self.my_mss.entryy.get())
            ss = self.my_mss.zero_setter(self.my_mss.entryss)
            sy = self.my_mss.zero_setter(self.my_mss.entrysuc)
            n = float(self.my_mss.entryn.get())
            result = sqrt((pow(((stressx - stressy) / 2), 2)) + pow(ss, 2))
            angle_above = atan(-(stressx - stressy) / (2 * ss)) / pi * 180
            angle = angle_above / 2
            self.my_mss.lblresult['text'] = 'τmax = ' + str(result) + ' kpsi' + '\nθs = ' + str(angle) + '°'
            self.my_mss.lblstatus['text'] = 'Status: ' + self.status(stressx, stressy, ss, sy, n)
            self.my_mss.success_color()
        except ValueError:
            messagebox.showerror("Error", value_message)

    @staticmethod
    def status(stressx, stressy, ss, sy, n):
        maximum = ((stressx + stressy) / 2) + sqrt(pow((stressx - stressy) / 2, 2) + pow(ss, 2))
        minimum = ((stressx + stressy) / 2) - sqrt(pow((stressx - stressy) / 2, 2) + pow(ss, 2))
        if n == 0:
            return 'n not was not inserted.'
        elif sy == 0:
            return 'Sy was not inserted.'
        elif maximum > 0 and minimum > 0 or maximum < 0 and minimum < 0:
            if abs(maximum) < sy / n and abs(minimum) < sy / n:
                return "Success"
            else:
                return "Fail"
        else:
            if abs(maximum - minimum) < sy / n:
                return "Success"
            else:
                return "Fail"


class DistortionEnergy:
    def __init__(self):
        self.my_de = Mohr("de")
        self.my_de.window.title("Distortion Energy Theory (Von Mises Theory) ")
        for item in [self.my_de.labelgiven, self.my_de.givenmenu, self.my_de.labelsut, self.my_de.entrysut]:
            item.grid_forget()
        self.my_de.labelsuc["text"] = "Yield Strength Sy(kpsi):"
        self.my_de.labelx['text'] = "Principal Stress σ1(kpsi):"
        self.my_de.labely['text'] = "Principal Stress σ2(kpsi):"
        self.my_de.labelss['text'] = "Principal Stress σ3(kpsi):"
        self.equation = PhotoImage(file="images/distortion.gif")
        self.my_de.lblcalc['image'] = self.equation
        self.my_de.lblcalc.image = self.equation
        self.my_de.buttoncalc['command'] = lambda: self.get_calculate_data()

    def get_calculate_data(self):
        try:
            s1 = float(self.my_de.entryx.get())
            s2 = float(self.my_de.entryy.get())
            s3 = float(self.my_de.entryss.get())
            sy = self.my_de.zero_setter(self.my_de.entrysuc)
            n = self.my_de.zero_setter(self.my_de.entryn)
            von_stress = self.calculate_stress(s1, s2, s3)
            status = self.status(von_stress, sy, n)
            self.my_de.lblresult['text'] = "σ' = " + str(von_stress)
            self.my_de.lblstatus['text'] = "Status: " + status
            self.my_de.success_color()
        except ValueError:
            messagebox.showerror("Error", value_message)

    @staticmethod
    def calculate_stress(s1, s2, s3):
        first_term = pow((s1 - s2), 2)
        second_term = pow((s2 - s3), 2)
        third_term = pow((s3 - s1), 2)
        return pow(((first_term + second_term + third_term)/2), 0.5)

    @staticmethod
    def status(von_stress, sy, n):
        if n == 0:
            return 'n not was not inserted.'
        elif sy == 0:
            return 'Sy was not inserted.'
        elif von_stress < sy/n:
            return "Success"
        else:
            return "Fail"
