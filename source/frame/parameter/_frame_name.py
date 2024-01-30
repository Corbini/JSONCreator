from tkinter import Frame, Button, Canvas, PhotoImage, Text, Entry


def create_frame_name(self, name):
    self.frame_name = Frame(self)

    self.frame_name_button = Button(
        self.frame_name,
        text=name,
        command=lambda: self.change_size(),
    )

    self.frame_name_text = Entry(
        self.frame_name
    )
    self.frame_name_text.propagate(False)

    self.frame_name_text.bind("<Leave>", lambda w: self.change_name())
    self.frame_name_text.bind("<Return>", lambda w: self.change_name())
    self.frame_name_text.grid(row=0, column=0, sticky='nw', ipadx=62, ipady=20)

    self.frame_name_button.bind("<Double-Button-1>", lambda w: self.configure_name())
    self.frame_name_button.grid(row=0, column=0, sticky='nw', ipadx=100, ipady=15)
    self.frame_name_button.focus_set()
    
    self.frame_name.grid(row=0, column=0, sticky='nw')


def configure_name(self):
    self.frame_name_text.focus_set()


def change_name(self):
    self.frame_name_text.event_generate('<<name_changed>>')
    self.frame_name_text.delete(0, 'end')
    self.frame_name_button.focus_set()

