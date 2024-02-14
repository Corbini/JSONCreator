from tkinter import Frame, END, StringVar
from customtkinter import CTkButton, CTkOptionMenu, CTkFrame


def create_generals(self, type, name):
    self.general = CTkFrame(
        self,
        width=150
    )

    self.variable = StringVar(self.general)
    self.variable.set("Branch")  # default value
    
    self.data = CTkOptionMenu(master= self.general, variable=self.variable, 
                                values=[  'Branch','String','Boolean','DataTime','SerialPort',
                                        'IP','IPv4','IPv6','UserName','password',
                                        'UInt8','UInt16','UInt32','UInt64','Int8','Int16','Int32','Int64',
                                        'Real32','Real64'],
                                command=self.menu_input)
    self.data.pack(side='top',fill='x', expand=True, padx=2, pady=2)

    if self.par_parent is not None:
        self.remove_button = CTkButton(self.general, text= 'remove')
        self.remove_button.pack(side='top',fill='x', anchor='nw', padx=2, pady=2)
    
        self.remove_button.configure(command=self.remove_parameter)


def remove_parameter(self):
    
    parents = []
    self.par_parent.get_parent(parents)

    name = self.name.get()

    self.call(parents, name, None, 'remove')

def menu_input(self, event):

    parents = []
    self.get_parent(parents)
    value = self.variable.get()
    self.call(parents, 'valueType', value, 'change')

def set_type(self, value):
    if value == "Branch":
        self.add_button.pack(side='bottom', anchor='nw', padx=2, pady=2)
    else:
        self.add_button.pack_forget()
    
    self.variable.set(value)

def show_generals(self):
    self.general.grid(row=1, column=0, sticky='nw', padx=10, pady=10, ipadx=10, ipady=10)

def hide_generals(self):
    self.general.grid_forget()
