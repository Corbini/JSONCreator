from tkinter import Frame, Entry, Label, Text, Button, END, OptionMenu, StringVar


def create_generals(self, type, name):
    self.general = Frame(
        self,
        width=150
    )

    self.variable = StringVar(self.general)
    self.variable.set("Branch")  # default value
    
    self.data = OptionMenu(self.general, self.variable, 
                           'Branch','String','Boolean','DataTime','SerialPort',
                           'IP','IPv4','IPv6','UserName','password',
                           'UInt8','UInt16','UInt32','UInt64','Int8','Int16','Int32','Int64',
                           'Real32','Real64',
                           command=lambda event: self.menu_input(event))
    self.data.config(width=15, padx=0, pady=0)
    self.data.pack(side='top',fill='x', expand=True)

    self.general_en_text = Label(self.general, text="angielska nazwa")
    self.general_en_text.pack(side='top',fill='x', expand=True)
    self.general_en = Entry(self.general)
    self.general_en.pack(side='top',fill='x', expand=True)

    self.general_pl_text = Label(self.general, text="polska nazwa")
    self.general_pl_text.pack(side='top',fill='x', expand=True)

    self.general_pl = Entry(self.general)
    self.general_pl.pack(side='top',fill='x', expand=True)
    
    if self.par_parent is not None:
        self.remove_button = Button(self.general, text= 'remove')
        self.remove_button.pack(side='top',fill='x', anchor='nw')
    
        self.remove_button.configure(command=self.remove_parameter)

def remove_parameter(self):
    
    parents = []
    self.par_parent.get_parent(parents)

    name = self.name_button.cget('text')

    self.call(parents, name, None, 'remove')

def reset_value(self, event):
    parents = self.get_parent([])
    name = str(event.widget).split('.')
    name = name[-1]

    self.call(parents, name, None, 'read')

def menu_input(self, event):

    parents = []
    self.get_parent(parents)
    value = self.variable.get()
    self.call(parents, 'valueType', value, 'change')


def entry_input(self, event):
    pass


def set_type(self, value):
    if value == "Branch":
        self.add_button.pack(side='bottom', anchor='nw')
    else:
        self.add_button.pack_forget()
    
    self.variable.set(value)

def show_generals(self):
    self.general.grid(row=1, column=0, sticky='nw')

def hide_generals(self):
    self.general.grid_forget()
