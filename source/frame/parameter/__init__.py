from tkinter import Frame, Button, Canvas, PhotoImage, Text, Entry
from source.frame.setting import Setting


class Parameter(Frame):

    def __init__(self, parent, frame, name):
        super().__init__(
            master=frame,
            width=120,
            height=40
        )
        self.pack(side='top', anchor='nw')

        self.par_parent = parent

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
        self.entry_1_t = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )

        self.entry_1_t.place(
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
        self.entry_2_t = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_2_t.place(
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
            text=name,
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
        self.settings_view = Frame(self)

        self.settings_view.propagate(True)
        self.settings_list = dict()
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

    def get_size(self):
        height = self.settings_view.winfo_height() + 30
        width = self.settings_view.winfo_width() + 220

        for element in self.settings_list:
            if isinstance(self.settings_list[element], Parameter):
                result = self.settings_list[element].get_size()
                width += result[0]
                height += result[1]

        return [width, height]
        

    def change_size(self):
        if self.widen is False:
            self.settings_view.place(
                in_=self,
                x=220,
                y=30
            )


            self.settings_view.update()
            dimension = self.get_size()


            if dimension[1] < 190:
                dimension[1] = 190

            self.configure(
                height=dimension[1],
                width=1000
            )

            self.widen = True

        else:
            self.settings_view.place_forget()

            self.configure(
                height=40,
                width=120
            )

            self.widen = False

    def set_type(self):
        self.type = "new_name"
        self.settings_list = dict()

    def update_setting(self, name, value):

        if name == "langPl":
            self.entry_2_t.insert(0, value)
            return
        
        if name == "langEn":
            self.entry_1_t.insert(0, value)
            return
        
        if name == "valueType":
            return
        
        if name not in self.settings_list:
            print("Create setting")
            self.settings_list[name] = Setting(self, self.settings_view, name, value)
        else:
            self.settings_list[name].update(value)

    def add_child(self, name):
        if name in self.settings_list:
            return
        
        print("Create parameter", name)
        self.settings_list[name] = Parameter(self, self.settings_view, name)
