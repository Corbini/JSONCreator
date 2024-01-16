import tkinter as tk
from source.window.main import MainWindow
from source.frame.main import Main
from source.controller import Controller
from source.json_structure import JSONStructure
from source.frame.gui import Parameter


if __name__ == "__main__":
    app = MainWindow()

    # view = Main(app)
    view = Parameter()
    model = JSONStructure()
    controller = Controller(view, model)

    app.mainloop()
