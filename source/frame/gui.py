from tkinter import Frame, Button, Canvas, PhotoImage, Text


class Parameter(Frame):
    def __init__(self):
        super().__init__(
            bg="#B0CEA1",
            width=120,
            height=40
        )
        self.grid()

        self.canvas = Canvas(
            self,
            bg = "#B0CEA1",
            height = 220,
            width = 500,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.canvas.create_text(
            230.0,
            190.0,
            anchor="nw",
            text="Maksimum",
            fill="#363131",
            font=("Judson Regular", 20 * -1)
        )

        self.canvas.create_text(
            230.0,
            160.0,
            anchor="nw",
            text="Długość",
            fill="#363131",
            font=("Judson Regular", 20 * -1)
        )

        self.canvas.create_text(
            230.0,
            130.0,
            anchor="nw",
            text="Znak",
            fill="#363131",
            font=("Judson Regular", 20 * -1)
        )

        self.canvas.create_text(
            230.0,
            100.0,
            anchor="nw",
            text="Domyślnie",
            fill="#363131",
            font=("Judson Regular", 20 * -1)
        )

        self.canvas.create_text(
            230.0,
            70.0,
            anchor="nw",
            text="Dostęp",
            fill="#363131",
            font=("Judson Regular", 20 * -1)
        )

        self.canvas.create_text(
            230.0,
            40.0,
            anchor="nw",
            text="Adres",
            fill="#363131",
            font=("Judson Regular", 20 * -1)
        )

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
        self.entry_image_2 = PhotoImage(
            file="assets/parameter/button_2.png")
        self.entry_2 = Button(
            self,
            image=self.entry_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.change_size(),
            relief="flat"
        )

        self.entry_2.bind("<Double-Button-1>", lambda w: self.configure_name())

        self.entry_2.place(
            x=10.0,
            y=10.0,
            width=100.0,
            height=20.0
        )

        self.canvas.create_rectangle(
            0.0,
            190.0,
            220.0,
            220.0,
            fill="#363131",
            outline="")

        self.canvas.create_rectangle(
            120.0,
            0.0,
            500.0,
            30.0,
            fill="#363131",
            outline="")
        
        self.type = "None"

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
            if self.type != "branch":
                self.configure(
                    width=500,
                    height=220
                )
            else:
                self.configure(
                    width=220,
                    height=190
                )
            self.widen = True
        else:
            self.configure(
                width=120,
                height=40
               )
            self.widen = False