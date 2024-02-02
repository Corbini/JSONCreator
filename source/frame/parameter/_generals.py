from tkinter import Frame, Entry, Label, Text, Button, END


def create_generals(self, type, name):
    self.general = Frame(
        self,
        width=150
    )


    self.general_types = Entry(self.general, name='valueType')
    self.general_types.insert(0, type)
    self.general_types.pack(side='top',fill='x', expand=True)
    self.general_types.bind('<Return>', self.entry_input)
    self.general_types.bind("<FocusOut>", self.reset_value)

    self.general_en_text = Label(self.general, text="angielska nazwa")
    self.general_en_text.pack(side='top',fill='x', expand=True)
    self.general_en = Entry(self.general)
    self.general_en.pack(side='top',fill='x', expand=True)

    self.general_pl_text = Label(self.general, text="polska nazwa")
    self.general_pl_text.pack(side='top',fill='x', expand=True)

    self.general_pl = Entry(self.general)
    self.general_pl.pack(side='top',fill='x', expand=True)
    
    if self.par_parent is not None:
        self.remove_button = Button(self.general, text= 'remove')
        self.remove_button.pack(side='top',fill='x', anchor='nw')
    
        self.remove_button.configure(command=lambda: self.call(self.par_parent.get_parent(list()), name, None, 'remove'))

def reset_value(self, event):
    parents = self.get_parent(list())
    name = str(event.widget).split('.')
    name = name[-1]

    self.call(parents, name, None, 'read')

def entry_input(self, event):
    text = event.widget.get()
    parents = self.get_parent(list())
    name = str(event.widget).split('.')
    name = name[-1]

    self.call(parents, name, text, 'change')


def set_type(self, value):
    self.general_types.delete(0, END)
    self.general_types.insert(0, value)

def show_generals(self):
    self.general.grid(row=1, column=0, sticky='nw')

def hide_generals(self):
    self.general.grid_forget()
