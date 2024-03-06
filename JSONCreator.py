from source.window.main import MainWindow
from source.frame.main import Main
from source.controller import Controller
from source.model.descriptor import Descriptor


if __name__ == "__main__":
    app = MainWindow()

    view = Main(app)
    model = Descriptor()
    controller = Controller(view, model)

    app.mainloop()
