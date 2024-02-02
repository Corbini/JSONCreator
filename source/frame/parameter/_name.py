from tkinter import Frame, Button, Text


def create_name(self, name):
    self.name = Frame(self, width=150, height=30)

    self.name.pack_propagate(False)

    self.name_button = Button(
        self.name,
        text=name,
        command=lambda: self.change_size()
    )
    self.name_button.propagate(False)
    # self.name_button.bind("<Double-Button-1>", lambda w: self.configure_name())

    self.name_text = Text(self.name)
    self.name_text.propagate(False)
    self.name_text.bind("<Leave>", lambda w: self.change_name())
    self.name_text.bind("<Return>", lambda w: self.change_name())

    self.name_button.pack(fill='both', expand=True)
    
    self.name.grid(row=0, column=0, sticky='nw')


def configure_name(self):
    self.name_text.pack(fill='both', expand=True)
    self.name_button.pack_forget()


def change_name(self):
    name = self.name_text.get(1.0, 'end')
    result = name
    self.name_text.event_generate('<<name_changed>>')
    
    self.name_text.delete(1.0, 'end')
    self.update_name(result)

def update_name(self, name):
    self.name_button.configure(text=name)
    self.name_text.pack_forget()
    self.name_button.pack(fill='both', expand=True)
