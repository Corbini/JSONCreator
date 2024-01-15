from tkinter import Frame, Button


class Parameter(Frame):
    def __init__(self, window):
        super().__init__(
            master=window,
            bg="#363131"
        )
        self.parameters = list()

    def _create_button(self, text: str):
        self.title = Button(
            master=self,
            borderwidth=0,
            highlightthickness=0,
            text=text,
            bg="#000000",
            command=lambda: print("title button was pressed"),
            relief="flat"
        )
        self.new_button.load_image("assets/button_1.png")
        self.new_button.pack(
            side = "top",
        )
