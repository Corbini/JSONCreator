from tkinter import Frame, Text, Canvas, Entry, Label


class Setting(Frame):
    def __init__(self, parent, frame, name, data=""):
        super().__init__(
            master=frame,
            height=40,
            width=300
        )

        self.data = Entry(self)
        self.data.insert(0, data)
        self.data.pack(side='left',fill='y', expand=True)

        self.name = Label(self, text=name)
        self.name.pack(side='left',fill='y', expand=True)

        self.par_parent = parent
        
        self.pack(side='top', anchor='nw')

    def update(self, value):
        self.data.insert(0, value)
        