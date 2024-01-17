from tkinter import Frame, Button, Canvas, PhotoImage, Text
from source.frame.setting import Setting

class Parameter(Frame):
    def __init__(self, parent, name):
        super().__init__(
            master=parent,
            width=120,
            height=40,
        )
        self.pack(side='top', anchor='nw')

        self.canvas = Canvas(
            self,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)

        self.canvas.create_rectangle(
            0.0,
            0.0,
            120.0,
            30.0,
            fill="#B0CEA1",
            outline="")


        self.canvas.create_rectangle(
            0.0,
            30.0,
            220.0,
            190.0,
            fill="#B0CEA1",
            outline="")

        self.entry_image_1 = PhotoImage(
            file="assets/parameter/entry_1.png")
        self.entry_bg_1 = self.canvas.create_image(
            110.0,
            170.0,
            image=self.entry_image_1
        )
        self.entry_1 = Text(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=10.0,
            y=160.0,
            width=200.0,
            height=18.0
        )

        self.canvas.create_text(
            10.0,
            130.0,
            anchor="nw",
            text="Angielska nazwa",
            fill="#000000",
            font=("Judson Regular", 20 * -1)
        )

        self.entry_image_2 = PhotoImage(
            file="assets/parameter/entry_2.png")
        self.entry_bg_2 = self.canvas.create_image(
            110.0,
            110.0,
            image=self.entry_image_2
        )
        self.entry_2 = Text(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_2.place(
            x=10.0,
            y=100.0,
            width=200.0,
            height=18.0
        )

        self.canvas.create_text(
            10.0,
            70.0,
            anchor="nw",
            text="Polska nazwa",
            fill="#000000",
            font=("Judson Regular", 20 * -1)
        )

        self.button_image_1 = PhotoImage(
            file="assets/parameter/button_1.png")
        self.entry_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.entry_1.place(
            x=10.0,
            y=40.0,
            width=100.0,
            height=20.0
        )

        self.entry_image_3 = PhotoImage(
            file="assets/parameter/entry_3.png")
        self.entry_bg_3 = self.canvas.create_image(
            60.0,
            20.0,
            image=self.entry_image_3
        )
        self.entry_3 = Text(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_3.bind("<Leave>", lambda w: self.change_name())
        self.entry_3.bind("<Return>", lambda w: self.change_name())
        self.entry_3.place(
            x=10.0,
            y=10.0,
            width=100.0,
            height=18.0
        )

        self.widen = False
        self.entry_2 = Button(
            self,
            text = name,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.change_size(),
            relief="flat",
        )

        self.entry_2.bind("<Double-Button-1>", lambda w: self.configure_name())

        self.entry_2.place(
            x=10.0,
            y=10.0,
            width=100.0,
            height=20.0
        )

        self.settings_view = Frame(
            self,
            height=200,
            width=200
        )
        self.settings_view.place(
            x= 220,
            y= 30
        )
        self.settings_list = list()
        self.type = "int"

    def configure_name(self):
        self.entry_2.place_forget()
        self.entry_3.focus_set()

    def change_name(self):
        self.entry_3.delete("1.0", "end")
        self.entry_2.place(
            x=10.0,
            y=10.0,
            width=100.0,
            height=20.0
        )

    def change_size(self):
        if self.widen is False:
            height = 190
            if len(self.settings_list) != 0:
                    new_h = self.settings_list[-1].winfo_rooty()
                    new_w = self.settings_list[-1].winfo_rootx(),
                    if new_h > height:
                        height = new_h

            self.configure(
                height = height,
                width=1000
            )
            self.widen = True
        else:
            self.configure(
                width=120,
                height=40
               )
            self.widen = False

    def set_type(self):
        self.type = "new_name"
        self.settings_list = list()

    def add_setting(self, setting_name, value = ""):

        if value == None:
            new_setting = Parameter(self.settings_view, setting_name)
        else:
            new_setting = Setting(self.settings_view, setting_name, value)


        self.settings_list.append(new_setting)
