from general_usages import *  # A file that contains general variables, classes and functions
from tkinter import *  # The library responsible for the GUI
import Static  # The file that has the static rules classes
import Dynamic


# TODO: Consider adjusting measuring units


class DynamicLoading:
    def __init__(self):
        self.frame_dynamic = Frame(window, bg=styles.frame_background)

    def strain_life(self):  # TODO: Continue
        pass

    def crack_growth(self):  # TODO: Continue
        pass

    def print_dynamic(self):  # Function that prints the frame responsible for dynamic loading
        MainScreen.first_frame.pack_forget()
        self.frame_dynamic.pack()
        window.title('Dynamic Loading')
        easy_grid(
            [Label(self.frame_dynamic, bg=styles.frame_background, text='Select a method', font=(styles.font, 30)),
             Button(self.frame_dynamic, text="Stress-life", font=(styles.font, 24),
                    bg=styles.button_background, bd=styles.button_border, activebackground=styles.button_active,
                    command=lambda: Dynamic.StressLife())], 1, 0, 0)


class StaticLoading:  # The class that has the static loading widgets and functions

    def __init__(self):  # Defines all the widgets in static loading
        self.conditions = []
        self.frame_static = Frame(window, bg=styles.frame_background)
        self.conditions_frame = Frame(window, bg=styles.frame_background)
        self.epsilon = Label(self.conditions_frame, bg=styles.frame_background, text='εf', font=(styles.font, 30))
        self.button_less_than_minimum = Button(self.conditions_frame, text="< 0.05", font=(styles.font, 24),
                                               bg=styles.button_background, bd=styles.button_border,
                                               activebackground=styles.button_active,
                                               command=lambda:
                                               StaticLoading.assign_conditions(self, self.button_less_than_minimum))
        self.button_more_than_minimum = Button(self.conditions_frame, text="≥ 0.05", font=(styles.font, 24),
                                               bg=styles.button_background, bd=styles.button_border,
                                               activebackground=styles.button_active,
                                               command=lambda:
                                               StaticLoading.assign_conditions(self, self.button_more_than_minimum))
        self.label_conservative = Label(self.conditions_frame, bg=styles.frame_background, text='Conservative?',
                                        font=(styles.font, 30))
        self.button_is_conservative = Button(self.conditions_frame, text="Yes", font=(styles.font, 24),
                                             bg=styles.button_background, bd=styles.button_border,
                                             activebackground=styles.button_active,
                                             command=lambda:
                                             StaticLoading.assign_conditions(self, self.button_is_conservative))
        self.button_is_not_conservative = Button(self.conditions_frame, text="No", font=(styles.font, 24),
                                                 bg=styles.button_background, bd=styles.button_border,
                                                 activebackground=styles.button_active,
                                                 command=lambda:
                                                 StaticLoading.assign_conditions(self, self.button_is_not_conservative))
        self.button_syt_equals_syc = Button(self.conditions_frame, text="Yes", font=(styles.font, 24),
                                            bg=styles.button_background, bd=styles.button_border,
                                            activebackground=styles.button_active,
                                            command=lambda:
                                            StaticLoading.assign_conditions(self, self.button_syt_equals_syc))
        self.button_syt_not_equals_syc = Button(self.conditions_frame, text="No", font=(styles.font, 24),
                                                bg=styles.button_background, bd=styles.button_border,
                                                activebackground=styles.button_active,
                                                command=lambda:
                                                StaticLoading.assign_conditions(self, self.button_syt_not_equals_syc))
        self.label_syt_equals_syc = Label(self.conditions_frame, bg=styles.frame_background, text='S(yt) = S(yc)?',
                                          font=(styles.font, 30))
        self.choice_frame = Frame(window, bg=styles.frame_background)
        self.or_label = Label(self.frame_static, bg=styles.frame_background, text="Or", font=(styles.font, 24))
        self.button_select_theory = Button(self.frame_static, text="Select a theory", font=(styles.font, 24),
                                           bg=styles.button_background, bd=styles.button_border,
                                           activebackground=styles.button_active,
                                           command=lambda: self.theory_choice())
        self.button_select_conditions = Button(self.frame_static, text="Select conditions", font=(styles.font, 24),
                                               bg=styles.button_background, bd=styles.button_border,
                                               activebackground=styles.button_active,
                                               command=lambda: self.print_conditions())

    @staticmethod
    def modified_mohr():
        brit = Static.modified('mohr')
        brit.window.title('Modified mohr')
        brit.labelsut['text'] = 'Sut (kpsi)'
        brit.labelsuc['text'] = 'Suc (kpsi)'
        brit.lblcalc['image'] = brit.formula_mohr

    @staticmethod
    def brittle_coulomb_mohr():
        # The function responsible for the Brittle Coulomb-Mohr theory, it calls the Ductile Mohr class and replaces
        # the labels accordingly
        brit = Static.Mohr('mohr')
        brit.window.title('Brittle Coulomb-Mohr')
        brit.labelsut['text'] = 'Sut (kpsi)'
        brit.labelsuc['text'] = 'Suc (kpsi)'    
        brit.lblcalc['image'] = brit.formula_brittle

    def check_conditions(self):  # Checks the conditions in the conditions list
        # If syt is not equal to syc disable the option that asks if the element is conservative
        if self.button_syt_not_equals_syc['relief'] == SUNKEN:
            self.button_is_conservative['relief'] = RAISED
            self.button_is_not_conservative['relief'] = RAISED
            self.button_is_conservative['bg'] = styles.button_background
            self.button_is_not_conservative['bg'] = styles.button_background
            # ...and remove these options from the conditions list
            for item in [self.button_is_conservative, self.button_is_not_conservative]:
                if item in self.conditions:
                    self.conditions.remove(item)

        if len(self.conditions) >= 2:
            # If the list has more than two conditions, start comparing
            if self.button_less_than_minimum in self.conditions and self.button_is_conservative in self.conditions:
                self.brittle_coulomb_mohr()
            elif self.button_less_than_minimum in self.conditions and \
                    self.button_is_not_conservative in self.conditions:
                self.modified_mohr()
            elif self.button_more_than_minimum in self.conditions and self.button_syt_equals_syc and \
                    self.button_is_conservative in self.conditions:
                Static.MaxStress()
            elif self.button_more_than_minimum in self.conditions and self.button_syt_equals_syc \
                    and self.button_is_not_conservative in self.conditions:
                Static.DistortionEnergy()
            elif self.button_more_than_minimum in self.conditions and self.button_syt_not_equals_syc in self.conditions:
                Static.Mohr('mohr')

    def assign_conditions(self, button):  # Assign the conditions to a list (conditions)
        # Put the selected button and its opposite in a list
        if button == self.button_less_than_minimum or button == self.button_more_than_minimum:
            items = [self.button_less_than_minimum, self.button_more_than_minimum]
        elif button == self.button_is_conservative or button == self.button_is_not_conservative:
            items = [self.button_is_conservative, self.button_is_not_conservative]
        else:
            items = [self.button_syt_equals_syc, self.button_syt_not_equals_syc]
        for item in items:
            if item == button:
                # Sink the selected button and add it to the conditions
                if item["relief"] == RAISED:
                    item['relief'] = SUNKEN
                    item['bg'] = styles.button_active
                    self.conditions.append(item)
            else:
                # Relief the opposite button and remove it from conditions
                if item["relief"] == SUNKEN:
                    item['relief'] = RAISED
                    item['bg'] = styles.button_background
                    self.conditions.remove(item)
        self.check_conditions()

    def print_conditions(self):  # Print the condition selection screen
        self.frame_static.pack_forget()
        self.conditions_frame.pack()
        items = [self.epsilon, self.button_less_than_minimum, self.button_more_than_minimum, self.label_conservative,
                 self.button_is_conservative, self.button_is_not_conservative, self.label_syt_equals_syc,
                 self.button_syt_equals_syc, self.button_syt_not_equals_syc]
        easy_grid(items, 3, 0, 0)

    def theory_choice(self):  # Print the theory selection screen
        window.title("Theory selection")
        self.frame_static.pack_forget()
        label_brittle = Label(self.choice_frame, bg=styles.frame_background, text='Brittle behaviour:',
                              font=(styles.font, 30))
        label_ductile = Label(self.choice_frame, bg=styles.frame_background, text='Ductile behaviour:',
                              font=(styles.font, 30))
        button_modified_mohr = Button(self.choice_frame, text="Modified Mohr theory", font=(styles.font, 24),
                                      bg=styles.button_background, bd=styles.button_border,
                                      activebackground=styles.button_active,
                                      command=lambda: self.modified_mohr())
        button_brittle_coulomb_mohr = Button(self.choice_frame,
                                             text="Brittle Coulomb-Mohr theory", font=(styles.font, 24),
                                             bg=styles.button_background, bd=styles.button_border,
                                             activebackground=styles.button_active,
                                             command=lambda: self.brittle_coulomb_mohr())
        button_ductile_coulomb_mohr = Button(self.choice_frame, text="Ductile Coulomb-Mohr theory",
                                             font=(styles.font, 24),
                                             bg=styles.button_background, bd=styles.button_border,
                                             activebackground=styles.button_active,
                                             command=lambda: Static.Mohr('mohr'))
        button_distorion_energy = Button(self.choice_frame, text="Distortion Energy theory", font=(styles.font, 24),
                                         bg=styles.button_background, bd=styles.button_border,
                                         activebackground=styles.button_active,
                                         command=lambda: Static.DistortionEnergy())
        button_mss = Button(self.choice_frame, text="Maximum Shear Stress theory",
                            font=(styles.font, 24), bg=styles.button_background, bd=styles.button_border,
                            activebackground=styles.button_active,
                            command=lambda: Static.MaxStress())

        self.choice_frame.pack()
        items = [label_brittle, button_modified_mohr, button_brittle_coulomb_mohr,
                 label_ductile, button_ductile_coulomb_mohr, button_distorion_energy, button_mss]
        for item in items:
            item.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

    def print_static(self):  # Print the general static loading screen
        window.title("Static loading")
        MainScreen.first_frame.pack_forget()
        self.frame_static.pack()
        self.button_select_theory.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        self.or_label.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        self.button_select_conditions.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)


class MainMenu:  # The first widgets
    def __init__(self):  # Defines the widgets
        self.first_frame = Frame(window, bg=styles.frame_background)
        self.menu_bar = Menu(window)
        window.config(menu=self.menu_bar)
        self.static_menu = Menu(self.menu_bar, tearoff=0)
        self.dynamic_menu = Menu(self.menu_bar, tearoff=0)
        self.label_header = Label(self.first_frame, bg=styles.frame_background, text='Fatigue and Failure calculator',
                                  font=(styles.font, 30))
        self.label_choose = Label(self.first_frame, bg=styles.frame_background, text='Choose an option from below',
                                  font=(styles.font, 20))
        self.button_reset = Button(window, text='reset program', bg=styles.button_background, bd=styles.button_border,
                                   activebackground=styles.button_active,
                                   command=lambda: self.reset())
        static_instance = StaticLoading()
        dynamic_instance = DynamicLoading()
        self.static_menu.add_command(label="Modified Mohr", command=static_instance.modified_mohr)
        self.static_menu.add_command(label="Brittle Coulomb-Mohr Theory",
                                     command=static_instance.brittle_coulomb_mohr)
        self.static_menu.add_command(label="Ductile Coulomb-Mohr", command=lambda: Static.Mohr('mohr'))
        self.static_menu.add_command(label="Distortion Energy Theory", command=lambda: Static.DistortionEnergy())
        self.static_menu.add_command(label="Maximum Shear Stress Theory", command=lambda: Static.MaxStress())
        self.menu_bar.add_cascade(label="Static", menu=self.static_menu)
        self.dynamic_menu.add_command(label="Stress Life", command=Dynamic.StressLife)
        self.dynamic_menu.add_command(label="Strain Life", command=dynamic_instance.strain_life)
        self.dynamic_menu.add_command(label="Crack Growth", command=dynamic_instance.crack_growth)
        self.menu_bar.add_cascade(label="Dynamic", menu=self.dynamic_menu)
        self.button_static = Button(self.first_frame, text="Static loading", font=(styles.font, 24),
                                    bg=styles.button_background, bd=styles.button_border,
                                    activebackground=styles.button_active,
                                    command=lambda: StaticLoading.print_static(static_instance))
        self.button_dynamic = Button(self.first_frame, text="Dynamic loading", font=(styles.font, 24),
                                     bg=styles.button_background, bd=styles.button_border,
                                     activebackground=styles.button_active,
                                     command=lambda: DynamicLoading.print_dynamic(dynamic_instance))

    @staticmethod
    def reset():  # Function that resets the program, it is called from the reset button
        window.destroy()
        main("reset")

    def print_first_frame(self):  # Function that prints the first frame
        self.first_frame.pack(fill=BOTH, expand=True)
        self.label_header.pack(fill=BOTH, expand=True, side=TOP, padx=10, pady=10)
        self.label_choose.pack(fill=BOTH, expand=True, side=TOP, pady=10)
        self.button_static.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        self.button_dynamic.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        self.button_reset.pack(side=BOTTOM, fill=X, expand=True)


window = Tk()
MainScreen = MainMenu()


def main(string):  # The main function responsible for running the program
    global window
    if string == "reset":  # If the main function is called from the reset button.
        window = Tk()
    window.title("Fatigue Failure Calculator")
    MainScreen.__init__()
    MainScreen.print_first_frame()


if __name__ == '__main__':
    main("none")
    window.mainloop()
