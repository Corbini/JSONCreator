from tkinter import Tk, PhotoImage


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("JSON Creator")
        self.geometry("1000x800")

        self.icon = PhotoImage(file = "assets/icon.png")
        self.iconphoto(True, self.icon)


