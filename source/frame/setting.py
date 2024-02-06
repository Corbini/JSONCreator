from tkinter import Frame, Text, Canvas, Entry, Label, END, OptionMenu, StringVar


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
                self.variable.set("RW")  # default value

                self.data = OptionMenu(self, self.variable, "RW", "R", "W", "A", "N", command=lambda event: self.update(event))
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
        match self.data.__module__:
            case OptionMenu.__module__:
                self.variable.set(value)

            case _:
                self.data.delete(0, END)
                self.data.insert(0, value)

        print(value)
        self.old_data = value

    def input(self, event):
        if self.par_parent is None:
            return
        
        parents = list()
        self.par_parent.get_parent(parents)

        match self.data.__module__:
            case OptionMenu.__module__:
                value = self.variable
            case _:
                value = self.data.get()

        name = self.name_label.cget("text")

        self.par_parent.call(parents, name, value, 'change')

    def reset(self, event):
        self.data.delete(0, END)
        self.data.insert(0, self.old_data)