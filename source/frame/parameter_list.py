import tkinter as tk
from tkinter import Canvas, PhotoImage, Text
from source.button import Button
from source.frame.parameter import Parameter


class ParameterList(tk.Frame):
    def __init__(self, window):
        super().__init__(
            master=window,
            bg="#363131"
        )
        self.parameters = list()

        self._new_parameter()
        self.create_parameter()

    def _new_parameter(self):
        self.new_button = Button(
            master=self,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.create_parameter(
                "new_parameter"
            ),
            relief="flat"
        )
        self.new_button.load_image("assets/button_1.png")
        self.new_button.pack(
            side = "top",
            padx=20, 
            pady=20
        )


    def create_parameter(self, name = "", type = "branch", pl_name = "", en_name= ""):
        new_button = Button(
            master=self,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        new_button.load_image("assets/button_1.png")
        new_button.pack(
            side = "top",
            padx=20, 
            pady=20
        )
        

        self.parameters.insert(0, new_button)
