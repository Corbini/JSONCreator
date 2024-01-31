from tkinter import Frame, Entry, Label, Text


def create_generals(self, type):
    self.general = Frame(
        self,
        width=150
    )


    self.general_types = Entry(self.general)
    self.general_types.insert(0, "untype")
    self.general_types.pack(side='top',fill='x', expand=True)

    self.general_en_text = Label(self.general, text="angielska nazwa")
    self.general_en_text.pack(side='top',fill='x', expand=True)
    self.general_en = Entry(self.general)
    self.general_en.pack(side='top',fill='x', expand=True)

    self.general_pl_text = Label(self.general, text="polska nazwa")
    self.general_pl_text.pack(side='top',fill='x', expand=True)

    self.general_pl = Entry(self.general)
    self.general_pl.pack(side='top',fill='x', expand=True)

def show_generals(self):
    self.general.grid(row=1, column=0, sticky='nw')

def hide_generals(self):
    self.general.grid_forget()
