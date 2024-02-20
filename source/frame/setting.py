from tkinter import Frame, Text, Canvas, Entry, Label, END, OptionMenu, StringVar
from source.frame.call import Call


class Setting(Frame):
    def __init__(self, parent, frame, name, data=""):
        super().__init__(
            master=frame,
            height=40,
            width=300
        )

        match name:
            case 'valueAccess':
                self.variable = StringVar(self)
                self.variable.set(data)  # default value

                self.data = OptionMenu(self, self.variable, "R", "W", "A", "N", command=lambda event: self.input(event))
                self.data.config(width=15, padx=0, pady=0)

            case 'readOnOpen':
                self.variable = StringVar(self)
                if data:
                    self.variable.set("True")  # default value
                else:
                    self.variable.set("False")  # default value

                self.data = OptionMenu(self, self.variable, "True", "False", command=lambda event: self.input(event))
                self.data.config(width=15, padx=0, pady=0)

            case _:
                self.data = Entry(self)
                self.data.insert(0, data)
                self.data.bind('<Return>', self.input)
                self.data.bind('<FocusOut>', self.reset)

        self.data.pack(side='left', fill='y', expand=True)

        self.name_label = Label(self, text=name)
        self.name_label.pack(side='left', fill='y', expand=True)

        self.par_parent = parent
        
        self.pack(side='top', anchor='nw')
        self.old_data = data

    def update(self, value):
        
        if isinstance(self.data, OptionMenu):
            if isinstance(value, bool):
                if value:
                    self.variable.set('True')
                else:
                    self.variable.set('False')
            else:
                self.variable.set(value)
        else:
            self.data.delete(0, END)
            self.data.insert(0, value)

        print(value)
        self.old_data = value

    def input(self, event):
        if self.par_parent is None:
            return
        
        parents = list()
        self.par_parent.get_parent(parents)

        if isinstance(self.data, OptionMenu):
                value = self.variable.get()

                if value == 'True':
                    value = True
                if value == 'False':
                    value = False
        else:
            value = self.data.get()

        name = self.name_label.cget("text")

        Call.call(parents, name, value, 'change')

    def reset(self, event):
        self.data.delete(0, END)
        self.data.insert(0, self.old_data)