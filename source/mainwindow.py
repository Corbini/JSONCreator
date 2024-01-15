from tkinter import Tk, PhotoImage
from source.frame.main import Main


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("JSON Creator")
        self.geometry("1000x800")

        self.icon = PhotoImage(file = "assets/icon.png")
        self.iconphoto(True, self.icon)

        self.main = Main(self)

