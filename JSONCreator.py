import tkinter as tk
from source.main_window import MainWindow
from source.frame.main import Main
from source.controller import Controller
from source.json_structure import JSONStructure


if __name__ == "__main__":
    app = MainWindow()

    view = Main(app)
    model = JSONStructure()
    controller = Controller(view, model)

    app.mainloop()
    