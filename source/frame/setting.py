from tkinter import Frame, Text, Canvas, Entry, Label, END, OptionMenu, StringVar
from source.frame.call import Call
from source.frame.warning import WarningPopUp


class Setting(Frame):
    def __init__(self, parent, frame, name, data="", call=None, label=True):
        super().__init__(
            master=frame,
            height=40,
            width=300
        )

        self.call = call

        true_false = ["Is Float", "Is Ordered", 'readOnOpen']

        if name in true_false:
            self.variable = StringVar(self)
            if data:
                self.variable.set("True")  # default value
            else:
                self.variable.set("False")  # default value

            if call is not None:
                self.data = OptionMenu(self, self.variable, "True", "False", command=lambda event: call(event))
            else:
                self.data = OptionMenu(self, self.variable, "True", "False", command=lambda event: self.input(event))
            self.data.config(width=15, padx=0, pady=0)

        elif name in 'valueAccess':
            self.variable = StringVar(self)
            self.variable.set(data)  # default value

            if call is not None:
                self.data = OptionMenu(self, self.variable, "R", "W", "A", "N", command=lambda event: call(event))
            else:
                self.data = OptionMenu(self, self.variable, "R", "W", "A", "N", command=lambda event: self.input(event))
            self.data.config(width=15, padx=0, pady=0)
        else:
            self.data = Entry(self)
            self.data.insert(0, data)

            if call is not None:
                self.data.bind('<Return>', call)
            else:
                self.data.bind('<Return>', self.input)

            self.data.bind('<FocusOut>', lambda e: self.data.unbind('<Leave>'))

            if call is not None:
                self.data.bind('<FocusIn>', lambda e: self.data.bind('<Leave>', call))
            else:
                self.data.bind('<FocusIn>', lambda e: self.data.bind('<Leave>', self.input))

        self.data.pack(side='left', fill='y', expand=True)

        self.name = name
        if label:
            self.name_label = Label(self, text=name)
            self.name_label.pack(side='left', fill='y', expand=True)

        self.par_parent = parent
        
        self.pack(side='top', anchor='nw')
        self.old_data = data

        self.warning = WarningPopUp([self.data])

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

        self.old_data = value

    def get(self) -> str:
        if isinstance(self.data, OptionMenu):
            return self.variable.get()
        else:
            return self.data.get()

    def input(self, event):
        if isinstance(self.data, OptionMenu):
                value = self.variable.get()

                if value == 'True':
                    value = True
                if value == 'False':
                    value = False
        else:
            value = self.data.get()

        if self.par_parent is None:
            return

        self.clear_warn()

        parents = list()
        self.par_parent.get_parent(parents)

        Call.call(parents, self.name, value, 'update')

    def clear_warn(self):
        self.warning.clear()

    def set_warn(self, text):
        self.warning.warn(text)
