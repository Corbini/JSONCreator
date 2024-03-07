from tkinter import Frame, Entry, Label, Text, Button, END, OptionMenu, StringVar
from source.frame.call import Call


class General(Frame):
    
    type_list = (
        'Branch', 'String', 'Boolean', 'DataTime', 'SerialPort',
        'IP', 'IPv4', 'IPv6', 'UserName', 'password',
        'UInt8', 'UInt16', 'UInt32', 'UInt64', 'Int8', 'Int16', 'Int32', 'Int64',
        'Real32', 'Real64', 'ReportBranch', 'Enum'
    )

    def __init__(self, frame, parents = lambda empty_list: list(empty_list), name = lambda: str('name')):
        super().__init__(
            frame,
            width=150
        )
        self.parents = parents
        self.name = name

        self.type = StringVar(self)
        self.type.set("Branch")  # default value

        self.type_menu = OptionMenu(self, self.type, *self.type_list, command=self.call_input)
        self.type_menu.config(width=15, padx=0, pady=0)
        self.type_menu.pack(side='top', fill='x', expand=True)

        empty_list = list()
        if self.parents(empty_list) is not None:
            self.removable = Button(self, text= 'remove', command=self.call_remove)
            self.removable.pack(side='top',fill='x', anchor='nw')

    def call_remove(self):
        empty_list = []
        parents = self.parents(empty_list)

        name = parents.pop(-1)
        Call.call(parents, name, None, 'remove')

    def call_input(self, event):
        parents = []
        self.parents(parents)
        value = self.type.get()
        Call.call(parents, 'valueType', value, 'update')
        
    def call_set(self, value):
        self.type.set(value)
        
    def show(self):
        self.grid(row=1, column=0, sticky='nw')

    def hide(self):
        self.grid_forget()
