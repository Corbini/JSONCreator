from tkinter import Frame, Text, Canvas, Entry, Label, END


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
        self.data.bind('<Return>', self.input)
        self.data.bind('<FocusOut>', self.reset)


        self.name_label = Label(self, text=name)
        self.name_label.pack(side='left',fill='y', expand=True)

        self.par_parent = parent
        
        self.pack(side='top', anchor='nw')
        self.old_data = data

    def update(self, value):
        self.data.delete(0, END)
        self.data.insert(0, value)
        self.old_data = value

    def input(self, event):
        if self.par_parent is None:
            return
        
        parents = list()
        self.par_parent.get_parent(parents)

        value =  self.data.get()
        name = self.name_label.cget("text")

        self.par_parent.call(parents, name, value)

        
    def reset(self, event):
        self.data.delete(0, END)
        self.data.insert(0, self.old_data)