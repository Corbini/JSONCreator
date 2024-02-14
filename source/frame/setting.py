from tkinter import Frame, END, StringVar
from customtkinter import CTkEntry, CTkLabel, CTkOptionMenu


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

                self.data = CTkOptionMenu(master= self, variable= self.variable, values=["R", "W", "A", "N"], command=lambda event: self.input(event))

            case 'readOnOpen':
                self.variable = StringVar(self)
                if data:
                    self.variable.set("True")  # default value
                else:
                    self.variable.set("False")  # default value

                self.data = CTkOptionMenu(master=self, variable=self.variable, values=["True", "False"], command=lambda event: self.input(event))

            case _:
                self.data = CTkEntry(self)
                self.data.insert(0, data)
                self.data.bind('<Return>', self.input)
                self.data.bind('<FocusOut>', self.reset)

        self.data.pack(side='left', fill='y', expand=True)

        self.name_label = CTkLabel(self, text=name)
        self.name_label.pack(side='left', fill='y', expand=True)

        self.par_parent = parent
        
        self.pack(side='top', anchor='nw')
        self.old_data = data

    def update(self, value):
        
        if isinstance(self.data, CTkOptionMenu):
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

        if isinstance(self.data, CTkOptionMenu):
                value = self.variable.get()

                if value == 'True':
                    value = True
                if value == 'False':
                    value = False
        else:
            value = self.data.get()

        name = self.name_label.cget("text")

        self.par_parent.call(parents, name, value, 'change')

    def reset(self, event):
        self.data.delete(0, END)
        self.data.insert(0, self.old_data)