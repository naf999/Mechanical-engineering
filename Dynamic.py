from general_usages import *
from tkinter import *
from math import *
from tkinter import messagebox


class Material:
    def __init__(self, name, material_type, elastic_modulus, ultimate_strength, f_limit, f_limit_cycles,
                 f_limit_reversals, stress_intercept, stress_slope,
                 fs_coefficient, fs_exponent, fd_coefficient, fd_exponent,
                 cs_coefficient, cs_exponent, cg_intercept, cg_exponent, cg_ratio, ts_intensity):
        self.name = name
        material_types = {1: '1. Steel', 2: '2. Aluminum', 3: '3. Nickel', 4: '4. Stainless steel', 5: '5. Other'}
        self.material_elastic = {'1. Steel': 207000, '2. Aluminum': 80000, '3. Nickel': 205000, '4. Stainless': 190000,
                                 '5. Other': 207000}
        self.material_type = material_types[material_type]
        self.su = ultimate_strength
        self._2nfl = f_limit_reversals
        self.nfl = self.value_or_default(f_limit_cycles, pow(10, 6))
        self.sf = self.value_or_default(stress_intercept, 1.6)
        self.B = self.value_or_default(stress_slope, -0.085)
        self.of = self.value_or_default(fs_coefficient, 1)
        self.b_exponent = self.value_or_default(fs_exponent, 1)
        self.ef = self.value_or_default(fd_coefficient, 1)
        self.c_exponent = self.value_or_default(fd_exponent, 1)
        self.n_exponent = self.value_or_default(cs_exponent, float(self.b_exponent) / float(self.c_exponent))
        self.K = self.value_or_default(cs_coefficient, float(self.of) / pow(float(self.ef), float(self.n_exponent)))
        self.C = cg_intercept
        self.m_exponent = cg_exponent
        self.rmat = cg_ratio
        self.kth = ts_intensity
        self.E = self.value_or_default(elastic_modulus, self.material_elastic[self.material_type])
        self.sfl = f_limit
        # TODO: Set Default for sfl later to avoid conflict with other theories

    @staticmethod
    def value_or_default(value, default):
        if value == '':
            return default
        else:
            return value


other = Material('Other', 5, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')
alu1100 = Material('Aluminum 1100', 2, 69000, 110, "", "", "", 155, -0.096, 166, -0.096, 1.643, -0.669, 154, 0.144,
                   "", 2.79, "", "")


# TODO: Store the defaults in a string


class StressLife:
    def __init__(self):

        self.window = Toplevel()
        self.window.title("Stress Life")

        self.sfcanvas = Canvas(self.window, width=880, height=800)
        self.sfscrollbar = Scrollbar(self.window, command=self.sfcanvas.yview)
        self.sfcanvas.config(yscrollcommand=self.sfscrollbar.set)
        self.sfframe = Frame(self.sfcanvas, height=1650, bg=styles.frame_background)
        self.sfcanvas.create_window((0, 0), window=self.sfframe, anchor=NW)
        self.sfcanvas.config(scrollregion=self.sfcanvas.bbox("all"))
        self.sfcanvas.pack(side=LEFT)
        self.sfscrollbar.pack(side=LEFT, fill=Y, expand=TRUE)

        self.givenvar = StringVar(self.sfframe)
        self.givens = ['Smax & Smin',
                       'Sa & Sm']
        self.givenvar.set(self.givens[0])
        self.givenvar.trace('w', lambda *args: self.given_tracer())
        self.givenmenu = OptionMenu(self.sfframe, self.givenvar, *self.givens)
        Label(self.sfframe, bg=styles.frame_background, text='Units are measured in MPA', font=(styles.font, 8)).grid(
            sticky=W)
        Label(self.sfframe, bg=styles.frame_background, text='Loading', font=(styles.font, 30)).grid(sticky=W,
                                                                                                     pady=(15, 0))
        self.givenmenu.grid(sticky=W, padx=5, pady=5)
        self.entrysmax = Entry(self.sfframe)
        self.entrysmin = Entry(self.sfframe)
        self.entrysa = Entry(self.sfframe, state='readonly')
        self.entrysm = Entry(self.sfframe, state='readonly')
        easy_grid(
            [Label(self.sfframe, bg=styles.frame_background, text='Maximum (Smax or e(max))', font=(styles.font, 20)),
             self.entrysmax,
             Label(self.sfframe, bg=styles.frame_background, text='Minimum (Smin or e(min))', font=(styles.font, 20)),
             self.entrysmin,
             Label(self.sfframe, bg=styles.frame_background, text='Alternating (Sa or e(a))', font=(styles.font, 20)),
             self.entrysa,
             Label(self.sfframe, bg=styles.frame_background, text='Mean (Sm or e(m))', font=(styles.font, 20)),
             self.entrysm], 2, 5, 0)
        Label(self.sfframe, bg=styles.frame_background, text='Material', font=(styles.font, 30)).grid(sticky=W,
                                                                                                      pady=(15, 0))

        
        self.stress_material_list = [other, alu1100]
        self.stress_display_list = []
        for item in self.stress_material_list:
            self.stress_display_list.append(item.name)
        self.material_var = StringVar(self.sfframe)
        self.material_menu = OptionMenu(self.sfframe, self.material_var, *self.stress_display_list)
        self.material_var.set(self.stress_display_list[0])
        self.material_var.trace('w', lambda *args: self.material_tracer())
        self.entryname = Entry(self.sfframe)

       

        self.entrytype = Entry(self.sfframe)
        self.entrytype.insert(0, '1. Steel')
        self.entrytype['state'] = 'readonly'
        self.typevar = StringVar(self.sfframe)
        self.types = ['1. Steel', '2. Aluminum', '3. Nickel', '4. Stainless Steel', '5. Other']
        self.typevar.set(self.types[0])
        self.typevar.trace('w', lambda *args: self.type_tracer())
        self.typemenu = OptionMenu(self.sfframe, self.typevar, *self.types)

        self.entrysu = Entry(self.sfframe)
        self.entrye_modulus = Entry(self.sfframe)
        self.entryflimit = Entry(self.sfframe)
        self.entryflimitcycles = Entry(self.sfframe)
        self.entryintercept = Entry(self.sfframe)
        self.entryslope = Entry(self.sfframe)
        easy_grid(self.grid_entries(['Material', 'Name', 'Type', 'Ultimate Strength', 'Elastic Modulus',
                                     'Fatigue Limit', 'Fatigue Limit Cycles', 'Intercept',
                                     'Slope'], [self.material_menu, self.entryname, self.entrytype,
                                                self.entrysu, self.entrye_modulus, self.entryflimit,
                                                self.entryflimitcycles, self.entryintercept,
                                                self.entryslope]), 2, 10, 0)
        self.typemenu.grid(row=12, column=3)
        Label(self.sfframe, bg=styles.frame_background, text='Modifying Factors', font=(styles.font, 30)).grid(sticky=W,
                                                                                                               pady=(
                                                                                                                   15,
                                                                                                                   0))
       




        
        self.entryksf = Entry(self.sfframe)
        self.entrykl = Entry(self.sfframe)
        self.size_or_d_var = StringVar(self.sfframe)
        self.size_or_d_lst = ['Ksize',
                              'Diameter']
        self.size_or_d_menu = OptionMenu(self.sfframe, self.size_or_d_var, *self.size_or_d_lst)
        self.size_or_d_var.set(self.size_or_d_lst[0])
        self.size_or_d_var.trace('w', lambda *args: self.size_or_diameter_tracer())
        self.entryksize = Entry(self.sfframe)
        self.entrydiameter = Entry(self.sfframe, state='readonly')
        easy_grid(self.grid_entries(['Surface Factor', 'Loading Factor', 'Use Diameter or size factor?',
                                     'Size Factor', 'Diameter (mm)'],
                                    [self.entryksf, self.entrykl, self.size_or_d_menu,
                                     self.entryksize, self.entrydiameter]), 2, 20, 0)
        Label(self.sfframe, bg=styles.frame_background, text='Stress Concentration Factor',
              font=(styles.font, 30)).grid(sticky=W, pady=(15, 0))
        self.sc_var = StringVar(self.sfframe)
        self.sc_lst = ['Stress Concentration Factor and radius',
                       'Fatigue Notch Factor',
                       'None']
        self.sc_menu = OptionMenu(self.sfframe, self.sc_var, *self.sc_lst)
        self.sc_var.set(self.sc_lst[0])
        self.sc_var.trace('w', lambda *args: self.sc_factor_tracer())
        self.entrykt = Entry(self.sfframe)
        self.entrykf = Entry(self.sfframe, state='readonly')
        self.entryradius = Entry(self.sfframe)
        # print(self.entrydiameter.grid_info())
        easy_grid(self.grid_entries(['Use:', 'Stress Concentration Factor', 'Fatigue Notch Factor', 'Radius (mm)'],
                                    [self.sc_menu, self.entrykt, self.entrykf, self.entryradius], ),
                  2, 26, 0)
        self.buttoncalculate = Button(self.sfframe, text="Calculate", font=(styles.font, 24),
                                      bg=styles.button_background, bd=styles.button_border,
                                      activebackground=styles.button_active,
                                      command=lambda: self.get_calculate_data())
        self.buttoncalculate.grid(column=0, row=self.entryradius.grid_info()['row'] + 1, sticky=W, padx=5, pady=(20, 0))

        self.surface_var = StringVar(self.sfframe)
        self.surface_lst = ['None', 'Ground', 'Machined', 'Cold Drawn', 'Hot Rolled', 'As Forged']
        self.surface_menu = OptionMenu(self.sfframe, self.surface_var, *self.surface_lst)
        self.surface_var.set(self.surface_lst[0])
        self.surface_var.trace('w', lambda *args: self.surface_tracer())




    def grid_entries(self, label_texts, entries):
        grid_list = []
        i = 0
        while i < len(label_texts):
            grid_list.append(
                Label(self.sfframe, bg=styles.frame_background, text=label_texts[i], font=(styles.font, 20)))
            grid_list.append(entries[i])
            i += 1
        return grid_list

    def given_tracer(self):
        smax_smin = [self.entrysmax, self.entrysmin]
        sa_sm = [self.entrysa, self.entrysm]
        if self.givens.index(self.givenvar.get()) == 0:
            for item in smax_smin:
                item['state'] = 'normal'
            for item in sa_sm:
                item.delete(0, END)
                item['state'] = 'readonly'
        else:
            for item in smax_smin:
                item.delete(0, END)
                item['state'] = 'readonly'
            for item in sa_sm:
                item['state'] = 'normal'

    def material_tracer(self):
        # Sets material to an instance of a class that contains properties (name, material_type, material.su,
        # material.E, material.sfl, material.nfl and material.sf)
        material = self.stress_material_list[self.stress_display_list.index(self.material_var.get())]
        # The keys are entries and the values are properties to assign to the entries
        entry_property = {self.entryname: material.name, self.entrytype: material.material_type,
                          self.entrysu: material.su, self.entrye_modulus: material.E, self.entryflimit: material.sfl,
                          self.entryflimitcycles: material.nfl, self.entryintercept: material.sf,
                          self.entryslope: material.B}
        for item in entry_property.keys():
            item['state'] = 'normal'
            item.delete(0, END)
            item.insert(0, entry_property[item])
        self.entrytype['state'] = 'readonly'
        # TODO: Move last line to calculate function

    def size_or_diameter_tracer(self):
        if self.size_or_d_lst.index(self.size_or_d_var.get()) == 0:
            self.entryksize['state'] = 'normal'
            self.entrydiameter.delete(0, END)
            self.entrydiameter['state'] = 'readonly'
        else:
            self.entrydiameter['state'] = 'normal'
            self.entryksize.delete(0, END)
            self.entryksize['state'] = 'readonly'

    def sc_factor_tracer(self):
        enable_disable = {0: [self.entrykf],
                          1: [self.entrykt, self.entryradius],
                          2: [self.entrykf, self.entrykt, self.entryradius]}
        index = self.sc_lst.index(self.sc_var.get())
        entries = enable_disable[index]
        for lists in enable_disable.values():
            for entry in lists:
                entry['state'] = 'normal'
        for item in entries:
            item.delete(0, END)
            item['state'] = 'readonly'

    def type_tracer(self):
        self.entrytype['state'] = 'normal'
        self.entrytype.delete(0, END)
        self.entrytype.insert(0, self.typevar.get())
        self.entrytype['state'] = 'readonly'

    def surface_tracer(self):
        pass

    # TODO: Continue

    def get_sa_sm(self):
        if self.givens.index(self.givenvar.get()) == 0:
            if float(self.entrysmax.get()) < float(self.entrysmin.get()):
                messagebox.showinfo("Edit", 'The maximum and minimum values were swapped.')
            smax = max([float(self.entrysmax.get()), float(self.entrysmin.get())])
            smin = min([float(self.entrysmax.get()), float(self.entrysmin.get())])
            return (smax - smin) / 2, (smax + smin) / 2
        else:
            return float(self.entrysa.get()), float(self.entrysm.get())

    def assign_defaults(self):
        string_material = Material(self.entryname.get(), int(self.entrytype.get()[0]), self.entrye_modulus.get(),
                                   self.entrysu.get(), self.entryflimit.get(),
                                   self.entryflimitcycles.get(), '', self.entryintercept.get(),
                                   self.entryslope.get(), '', '', '', '', '', '', '', '', '', '')
        if self.entryflimit.get() == '':
            self.entryflimit.insert(0, string_material.value_or_default(self.entryflimit.get(),
                                                                        float(string_material.sf) *
                                                                        pow(float(string_material.nfl),
                                                                            float(string_material.B))))
            # Default suspended till get_floats
        return string_material

    def get_floats(self, string_material):
        used_material = Material(string_material.name, int(string_material.material_type[0]),
                                 float(string_material.E),
                                 float(string_material.su), string_material.sfl,
                                 float(string_material.nfl), '', float(string_material.sf),
                                 float(string_material.B), '', '', '', '', '', '', '', '', '', '')
        used_material.sfl = float(self.entryflimit.get())
        return used_material

    def get_modifying_factors(self):
        ksf = float(Material.value_or_default(self.entryksf.get(), 1))
        kl = float(Material.value_or_default(self.entrykl.get(), 1))
        if self.entryksize['state'] == 'readonly':
            d = float(Material.value_or_default(self.entrydiameter.get(), 1))
            ksize = pow(d / 7.62, -0.1133)
        else:
            ksize = float(Material.value_or_default(self.entryksize.get(), 1))

        return ksf, kl, ksize

    def get_notch_factor(self, material):
        if self.entrykf['state'] == 'normal':
            kf = float(Material.value_or_default(self.entrykf.get(), 1))
        else:
            kt = float(Material.value_or_default(self.entrykt.get(), 1))
            r = float(Material.value_or_default(self.entryradius.get(), 1))
            a = 0.025 * pow((2070 / material.su), 1.8)
            kf = 1 + (kt - 1) / (1 + (a / r))
        return kf

    def get_calculate_data(self):
            root =Tk()

            label_11 = Label(root, bg="orange", text="Safety Factor = 1.6", font=(styles.font, 30))
            label_11.grid(row=0)
            root.mainloop()
            
            
        # If from this class calc using sa, sm else calc using stress factor
    

