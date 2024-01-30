from tkinter import Frame, Canvas, Text, Entry, Label


def create_generals(self):
    self.general_frame = Frame(
        self,
        bg="green",
    )

    self.general_type = Entry(self.general_frame, name="untyped")
    self.general_type.grid(row=0, column=0, ipadx=100, ipady=15)

    self.general_en_text = Label(self.general_frame, name="angielska nazwa")
    self.general_en_text.grid(row=1, column=0, ipadx=100, ipady=15)
    self.general_en = Entry(self.general_frame, name="untyped")
    self.general_en.grid(row=2, column=0, ipadx=100, ipady=15)

    self.general_pl_text = Label(self.general_frame, name="polska nazwa")
    self.general_pl_text.grid(row=3, column=0, ipadx=100, ipady=15)
    self.general_pl = Entry(self.general_frame, name="untyped")
    self.general_pl.grid(row=4, column=0, ipadx=100, ipady=15)

    self.general_frame.grid(row=1, column=0, sticky='nw')
