from tkinter import Frame, Text, Canvas


class Setting(Frame):
    def __init__(self, parent, name, data = ""):
        super().__init__(
            master=parent,
            height = 40,
            width = 280
        )
        print(name)
        
        self.pack(side='top', anchor='nw')

        self.canvas = Canvas(
            self,
            bg = "#B0CEA1",
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        
        entry_1 = Text(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_1.insert('1.0', data)
        entry_1.place(
            x=120.0,
            y=10.0,
            width=150.0,
            height=20.0
        )

        self.canvas.create_rectangle(
            10.0,
            10.0,
            110.0,
            30.0,
            fill="#FFFFFF",
            outline="")

        self.canvas.create_text(
            10.0,
            10.0,
            anchor="nw",
            text=name,
            fill="#000000",
            font=("Judson Regular", 20 * -1)
        )

        print(type)
        print(data)
