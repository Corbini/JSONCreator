from tkinter import Frame, Button, Canvas, PhotoImage, Text, Entry


def create_frame_name(self, name):
    self.frame_name = Frame(self)

    self.frame_name_text = Text(
        self.frame_name,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    self.frame_name_text.bind("<Leave>", lambda w: self.change_name())
    self.frame_name_text.bind("<Return>", lambda w: self.change_name())
    self.frame_name_text.place(
        x=10.0,
        y=10.0,
        width=100.0,
        height=18.0
    )

    self.frame_name_button = Button(
        self.frame_name,
        text=name,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: self.change_size(),
        relief="flat",
    )

    self.frame_name_button.bind("<Double-Button-1>", lambda w: self.configure_name())

    self.frame_name.grid(row=0, column=0)


def configure_name(self):
    self.frame_name_text.focus_set()


def change_name(self):
    self.frame_name_text.event_generate('<<name_changed>>')
    self.frame_name_text.delete("1.0", "end")
    self.frame_name_button.focus_set()

