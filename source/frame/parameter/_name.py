from tkinter import Frame, Button, Text, Entry


def create_name(self, name):
    self.name = Frame(self, width=150, height=30)

    self.name.pack_propagate(False)

    self.name_button = Button(
        self.name,
        text=name
    )
    self.name_button.propagate(False)
    self.name_button.bind("<Button-1>", lambda w: self.change_size())
    self.name_button.bind("<Double-Button-1>", lambda w: self.configure_name())

    self.name_text = Entry(self.name)
    self.name_text.propagate(False)

    self.name_button.pack(fill='both', expand=True)
    
    self.name.grid(row=0, column=0, sticky='nw')


def configure_name(self):
    self.name_text.pack(fill='both', expand=True)
    self.name_text.bind("<Leave>", lambda w: self.show_name_button())
    self.name_text.bind("<FocusOut>", lambda w: self.show_name_button())
    self.name_text.bind("<Return>", lambda w: self.change_name())
    self.name_button.pack_forget()


def change_name(self):
    name = self.name_text.get()

    if name == '':
        self.show_name_button()
        return
    
    new_list = list()
    self.par_parent.get_parent(new_list)

    text = self.name_button.cget('text')

    self.call(new_list, text, name, 'change')
    

def update_name(self, name):
    self.show_name_button()

    self.name_button.configure(text=name)
    self.name_button.update()
    

def show_name_button(self):
    self.name_text.pack_forget()
    self.name_text.delete(0, 'end')
    self.name_text.unbind('<Leave>')
    self.name_text.unbind('<FocusOut>')
    self.name_text.unbind('<Return>')
    self.name_button.pack(fill='both', expand=True)
