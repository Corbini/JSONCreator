from tkinter import PhotoImage, Frame
from source.button import Button
from source.frame.main._device import Device


def create_menu(self):
        self.options = Frame(
            self,
            bg = "#363131",
            width = 250,
            height=800
        )

        # self.options.place(x = 744, y = 0)
        self.options.pack(side='right', anchor='ne', fill='y')
        
        self.button_1 = Button(
            master=self.options,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.event_generate('<<tree_new>>'),
            relief="flat"
        )
        self.button_1.load_image("assets/frame_main/button_1.png")
        self.button_1.place(
            x=35,
            y=50.0,
            width=187.0,
            height=50.0
        )


        button_image_2 = PhotoImage(
            file="assets/frame_main/button_2.png")
        self.button_2 = Button(
            master=self.options,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.event_generate("<<load>>"),
        )
        
        self.button_2.load_image("assets/frame_main/button_2.png")
        self.button_2.place(
            x=35,
            y=266.66668701171875,
            width=187.0,
            height=50.0
        )

        self.button_3 = Button(
            master=self.options,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.event_generate("<<save_as>>"),
        )
        self.button_3.load_image("assets/frame_main/button_3.png")
        self.button_3.place(
            x=35,
            y=483.3333740234375,
            width=187.0,
            height=50.0
        )

        self.button_4 = Button(
            master=self.options,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.event_generate("<<quit>>"),
            relief="flat"
        )
        self.button_4.load_image("assets/frame_main/button_4.png")
        self.button_4.place(
            x=35,
            y=700.0,
            width=187.0,
            height=50.0
        )

        self.button_5 = Button(
            master=self.options,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.event_generate("<<load_languages>>"),
            relief="flat"
        )
        self.button_5.load_image("assets/frame_main/button_5.png")
        self.button_5.place(
            x=35,
            y=375.0,
            width=187.0,
            height=50.0
        )

        self.button_6 = Button(
            master=self.options,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.event_generate("<<save_languages>>"),
            relief="flat"
        )
        self.button_6.load_image("assets/frame_main/button_6.png")
        self.button_6.place(
            x=35,
            y=592.0,
            width=187.0,
            height=50.0
        )

        self.device = Device(self)
