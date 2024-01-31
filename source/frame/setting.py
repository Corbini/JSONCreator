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
        self.data.insert(0, value)

    def input(self, event):
        if self.par_parent is None:
            return
        
        self.parents = list()
        self.par_parent.get_parent(self.parents)

        self.new_value =  self.data.get()
        self.old_data = self.new_value
        self.name = self.name_label.cget("text")

        print(event)

        print(self.parents, self.name, self.new_value)
        # self.event_generate('<<input>>', data = self)

        
    def reset(self, event):
        self.data.delete(0, END)
        self.data.insert(0, self.old_data)