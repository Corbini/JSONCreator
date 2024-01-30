import tkinter as tk
from tkinter import Canvas, PhotoImage, Text
from source.button import Button


class Main(tk.Frame):
    def __init__(self, window):
        super().__init__(master=window, width=1000, height=800)
        self._create_menu()
        self.grid()

        self.event_add("<<save_as>>", "<Control-S>")

    def _create_menu(self):
        self.canvas = Canvas(
            self,
            bg = "#363131",
            height = 800,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)

        self.button_1 = Button(
            master=self,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_1.load_image("assets/frame_main/button_1.png")
        self.button_1.place(
            x=779.0,
            y=50.0,
            width=187.0,
            height=50.0
        )

        button_image_2 = PhotoImage(
            file="assets/frame_main/button_2.png")
        self.button_2 = Button(
            master=self,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.event_generate("<<load>>"),
        )
        # self.button_2.event_add("<<load>>", "<Button-1>")
        self.button_2.load_image("assets/frame_main/button_2.png")
        self.button_2.place(
            x=779.0,
            y=266.66668701171875,
            width=187.0,
            height=50.0
        )

        self.button_3 = Button(
            master=self,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.event_generate("<<save_as>>"),
        )
        self.button_3.load_image("assets/frame_main/button_3.png")
        self.button_3.place(
            x=779.0,
            y=483.3333740234375,
            width=187.0,
            height=50.0
        )

        self.button_4 = Button(
            master=self,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.event_generate("<<quit>>"),
            relief="flat"
        )
        self.button_4.load_image("assets/frame_main/button_4.png")
        self.button_4.place(
            x=779.0,
            y=700.0,
            width=187.0,
            height=50.0
        )

        self.image_image_1 = PhotoImage(
            file="assets/frame_main/image_1.png")
        self.image_1 = self.canvas.create_image(
            372.0,
            400.0,
            image=self.image_image_1
        )

        self.entry_image_1 = PhotoImage(
            file="assets/frame_main/entry_1.png")
        self.entry_bg_1 = self.canvas.create_image(
            135.0,
            35.0,
            image=self.entry_image_1
        )
        self.entry_1 = Text(
            self,
            bd=0,
            bg="#AFCEA1",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=10.0,
            y=10.0,
            width=250.0,
            height=48.0
        )

    def update(self, parents, name, value=None):
        parent = self
        print(parents, name, value)
        while parents:
            parent_name = parents.pop(0)
            print("Opening: ", parent_name)
            parent = parent.settings_list[parent_name]

        if value is None:
            pass
            parent.add_child(name)
        else:
            parent.update_setting(name, value)
            